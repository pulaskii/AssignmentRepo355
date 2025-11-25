from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_bcrypt import Bcrypt
from wtforms import StringField, PasswordField, SubmitField, RadioField, validators
from flask_wtf import FlaskForm, CSRFProtect
from wtforms.validators import EqualTo, InputRequired
import jinja2
import mysql
from pyModules.sqlpy.connectToDB import connectDatabase
from pyModules.sqlpy.createAccountRow import addNewUser
from pyModules.sqlpy.fetchData import fetchUserData
from pyModules.sqlpy.saveData import saveUserData
from pyModules.sqlpy.fetchAccessMap import fetchAccessMap
from pyModules.sqlpy.saveEmbedding import save_embedding
import os
from dotenv import load_dotenv
import numpy as np
import ollama
from typing import Dict
from pyModules.ollama.summarization import call_llm_summary
from pyModules.ollama.comparison import find_similar_patients

app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("CONFIG_KEY")
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

EMBEDDING_MODEL = "embeddinggemma"
EXCLUDED_FIELDS = ["First_Name", "Last_Name", "Email", "Phone_Number", "Date_Updated"]  # fields to skip for per-field embeddings

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup_page", methods = ['GET', 'POST'])
def signup():
    patient_or_provider = None
    first_name = None
    last_name = None
    phone_number = None
    user_email = None
    password = None

    sign_up_form = SignUp()
    if request.method == "POST":
        if sign_up_form.validate_on_submit():
            patient_or_provider = sign_up_form.patient_or_provider.data
            first_name = sign_up_form.first_name.data
            last_name = sign_up_form.last_name.data
            phone_number = sign_up_form.phone_number.data
            user_email = sign_up_form.user_email.data
            password = sign_up_form.password.data
            hashed_password = bcrypt.generate_password_hash(sign_up_form.password.data).decode('utf-8')
            password = hashed_password


            addNewUser(first_name,
                       last_name,
                       user_email,
                       phone_number,
                       password,
                       patient_or_provider,
                       connectDatabase()
                       )

    return render_template("signup_page.html", patient_or_provider = patient_or_provider, first_name = first_name, last_name = last_name,
                        user_email = user_email, phone_number = phone_number, password = password, 
                           form = sign_up_form)

@app.route("/login_page", methods = ['GET', 'POST'])
def login():
    email_login = None
    password_login = None

    login_form = LogIn()
    if request.method == "POST":
        if login_form.validate_on_submit():
            email_login = login_form.email_login.data
            password_login = login_form.password_login.data

            #TODO: We need to validate the email and password against the database here
            #If validated and the user is a doctor, redirect to doctor page
            #If validated and the user is a patient, redirect to patient page
            #Jo work your magic

            return redirect(url_for("provider", email=email_login))
        
    return render_template("login_page.html", email_login = email_login, password_login = password_login,
                           form = login_form)

@app.route("/edit_record_page")
def edit_record_page():
    return render_template("edit_record_page.html")

# Get patient data for edit_record_page
@app.route("/api/get_patient")
def api_get_patient():
    email = request.args.get("email")

    db = connectDatabase()
    result = fetchUserData(email, db)

    if result:
        return jsonify(result)

    return jsonify({"error": "Could not fetch user"}), 400

# Save updated patient data and embeddings from edit_record_page
@app.route("/api/update_record", methods=["POST"])
def api_update_record():
    data = request.get_json()
    updated_fields = data.get("updated_fields")
    email = data.get("email")

    # --- Save updated fields to user table ---
    for column, value in updated_fields.items():
        saveUserData(
            userEmail=email,
            dbConnection=connectDatabase(),
            columnToSet=column,
            valueToSet=value
        )

    # --- Create embeddings for updated patient record ---
    patient_record = {**updated_fields, "Email": email}

    # Per-field embeddings
    for field, value in patient_record.items():
        if field in EXCLUDED_FIELDS:
            continue

        # If the value is empty, save None (NULL)
        if value is None or str(value).strip() == "":
            vec = None
        else:
            vec = embed(str(value))
        
        save_embedding(connectDatabase(), email, field, vec)


    # Full record embedding
    full_text = build_full_record_text(patient_record)
    full_vec = embed(full_text)

    save_embedding(connectDatabase(), email, "Full_Record", full_vec)

    return jsonify({"message": "Record saved and embeddings updated"})

def embed(text: str):
    """Generate embedding using Ollama."""
    batch = ollama.embed(model=EMBEDDING_MODEL, input=[text])
    return np.array(batch["embeddings"][0], dtype=np.float32)


def build_full_record_text(patient: dict) -> str:
    """Concatenate all patient fields into a single string, excluding Email."""
    return " ".join(str(v) for k, v in patient.items() if k not in EXCLUDED_FIELDS)

@app.route('/provider_portal')
def provider():
    doctor_email = request.args.get("email")
    return render_template('provider_homepage.html', doctor_email=doctor_email)

# Fetch patients or doctors from accessMap
@app.route("/api/fetch_access_map")
def api_fetch_access_map():
    user_email = request.args.get("email")
    user_type = request.args.get("type", "doctor").lower()   # default to doctor

    # Validate type
    if user_type not in ["doctor", "patient"]:
        return jsonify({"error": "Invalid type. Use 'doctor' or 'patient'."}), 400

    db = connectDatabase()

    try:
        result = fetchAccessMap(user_email, db, user_type)

        # Expecting a list of tuples: [("First","Last","email"), ...]
        return jsonify(result)

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": "Failed to fetch access map"}), 500

# === Flask endpoints ===
@app.route("/summarize", methods=["POST"])
def summarize():
    payload = request.get_json(force=True)
    record: Dict = payload.get("record", {})
    prompt: str = payload.get("prompt", "")

    if not isinstance(record, dict):
        return jsonify({"error": "record must be an object/dict"}), 400
    if not isinstance(prompt, str):
        return jsonify({"error": "prompt must be a string"}), 400

    summaries = call_llm_summary(record, prompt)
    requested_fields = [s.field for s in summaries]
    missing_fields = [f for f in record.keys() if f not in requested_fields]

    response_json = {
        "requested_fields": requested_fields,
        "missing_fields": missing_fields,
        "summaries": [s.model_dump() for s in summaries],
        "error": None,
        "summary_text": "\n".join(s.summary for s in summaries)
    }
    return jsonify(response_json), 200

@app.route("/similar_patients", methods=["POST"])
def similar_patients():
    payload = request.get_json(force=True)
    email = payload.get("email")
    prompt = payload.get("prompt", "")

    if not isinstance(email, str):
        return jsonify({"error": "email must be a string"}), 400

    top_emails, fields_used = find_similar_patients(email, prompt)
    return jsonify({
        "target_email": email,
        "similar_patients": top_emails,
        "fields_compared": fields_used
    }), 200

class SignUp(FlaskForm):
    patient_or_provider = RadioField("Are you a patient or a provider?", choices=[('patient', 'Patient'), ('provider', 'Provider')], validators=[InputRequired()])

    first_name = StringField("Enter your first name", validators = [validators.DataRequired(message = "First name is required")], render_kw = {'placeholder': "John"})
    
    last_name = StringField("Enter your last name", validators = [validators.DataRequired(message = "Last name is required")], render_kw = {'placeholder': "Doe"})
    
    phone_number = StringField("Phone number", validators = [validators.DataRequired(message = "Phone number is required"),
                                                               validators.Length(min = 10, message = "Must be at least 10 characters"),
                                                               validators.Regexp(r'^\(\d{3}\)\s?\d{3}-\d{4}$', 
                                                            message="Invalid phone number format. Use (123) 456-7890")
                                                             ], render_kw = {'placeholder': "(000) 000-0000"})
    user_email = StringField("Email", validators = [validators.DataRequired(), validators.Email("Must be a valid email")], render_kw = {'placeholder': "example@email.com"})
    
    password = PasswordField("Create a unique password.", validators = [validators.DataRequired(message = "Please enter a password"),
                validators.Length(min = 8, max = 20, message = "Please enter a password between 8 and 20 characters"),
                validators.Regexp(r'^(?=.*[A-Z])(?=.*[!@#$%^+=-])(?=.{8,20}$)[^{}[\]<|*&"()]*$', message = "Please enter a valid password. Valid special characters are @, #, !, $, -, or _"),
                EqualTo('confirm_password', message="Passwords must match")],
                           render_kw = {'placeholder': "8-20 characters long, one capital letter, one special character"})
    
    confirm_password = PasswordField("Confirm your password", validators = [validators.DataRequired(message="Please confirm your password")
    ], render_kw={'placeholder': "Re-enter your password"})

    submit_button = SubmitField("Submit")

class LogIn(FlaskForm):
    email_login = StringField("Email", validators=[validators.DataRequired(message="Please enter your email"),validators.Email("Must be a valid email")],
                             render_kw={'placeholder': "Enter your email"})
    password_login = PasswordField("Password.", validators = [validators.DataRequired(message = "Please enter your password"),
                validators.Length(min = 8, max = 20, message = "Must be between 8 and 20 characters"),
                validators.Regexp(r'^(?=.*[A-Z])(?=.*[!@#$%^+=-])(?=.{8,20}$)[^{}[\]<|*&"()]*$', message = "Invalid format.")], render_kw={'placeholder': "Enter your password"})

    submit_button = SubmitField("Submit")

if __name__ == "__main__":
    app.run(debug = True)