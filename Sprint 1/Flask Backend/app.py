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
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("CONFIG_KEY")
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

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

    if isinstance(result, dict):
        return jsonify(result)

    return jsonify({"error": "Could not fetch user"}), 400

# Save updated patient data from edit_record_page
@app.route("/api/update_record", methods=["POST"])
@csrf.exempt
def api_update_record():
    print("test")
    
    data = request.get_json()
    updated_fields = data.get("updated_fields")
    email = data.get("email")

    for column, value in updated_fields.items():
        saveUserData(userEmail=email,
                     dbConnection=connectDatabase(),
                     columnToSet=column,
                     valueToSet=value)

    return jsonify({"message": "Record saved"})

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

class SignUp(FlaskForm):
    patient_or_provider = RadioField("Are you a patient or a provider?", choices=[('Patient', 'Patient'), ('Provider', 'Provider')], validators=[InputRequired()])

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