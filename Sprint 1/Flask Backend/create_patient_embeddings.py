import datetime
import ollama
from pyModules.sqlpy.connectToDB import connectDatabase
from pyModules.sqlpy.fetchUserEmails import fetchUserEmails
from pyModules.sqlpy.fetchData import fetchUserData
from pyModules.sqlpy.saveEmbedding import save_embedding
import numpy as np

EXCLUDED_FIELDS = ["First_Name", "Last_Name", "Email", "Phone_Number", "Date_Updated"]  # fields to skip for per-field embeddings
EMBEDDING_MODEL = "embeddinggemma"
db = connectDatabase()

# Get all patient emails
rows = fetchUserEmails(db)
patientEmails = []

for row in rows:
    rowMap = {item["field"]: item["value"] for item in row}
    if rowMap.get("PatientOrProvider").lower() == "patient":
        patientEmails.append(rowMap.get("Email"))

print("Patients:", patientEmails)

# Call the Flask API for each patient
for email in patientEmails:
    def embed(text: str):
        """Generate embedding using Ollama."""
        batch = ollama.embed(model=EMBEDDING_MODEL, input=[text])
        return np.array(batch["embeddings"][0], dtype=np.float32)


    def build_full_record_text(patient: dict) -> str:
        """Concatenate all patient fields into a single string, excluding Email."""
        return " ".join(str(v) for k, v in patient.items() if k not in EXCLUDED_FIELDS)
    
    db = connectDatabase()
    userDataList = fetchUserData(email, db)  # returns list of {"field","value"}

    # Convert list of field/value pairs into a normal dict
    userDataDict = {}
    for item in userDataList:
        field = item["field"]
        value = item["value"]

        # Convert datetime -> string
        if isinstance(value, (datetime.datetime, datetime.date)):
            value = value.isoformat()

        userDataDict[field] = value

    # --- Create embeddings for updated patient record ---
    patient_record = {**userDataDict, "Email": email}

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