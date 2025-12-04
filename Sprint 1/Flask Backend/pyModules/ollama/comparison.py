import ollama
import json
import numpy as np
import logging
from pyModules.sqlpy.fetchEmbedding import fetch_embedding

logger = logging.getLogger(__name__)

# === Config ===
AVAILABLE_FIELDS = [
    "Age", "Sex", "Weight", "Height",
    "Medications", "Allergies", "Active_Problems",
    "Medical_History", "Family_History", "Full_Record"
] # TODO Get from database so not hardcoded?

LLM_MODEL = "gpt-oss:20b-cloud"
NUM_SIMILAR_PATIENTS = 5
seed = 69


# ===============================
# COSINE SIMILARITY
# ===============================

def cosine_similarity(a: np.ndarray, b: np.ndarray):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# ===============================
# FIELD SELECTION
# ===============================

def select_fields_from_prompt(prompt: str, available_fields: list[str]):
    system_message = (
        "You identify which fields of a patient record are relevant to a user's query. "
        "Return a JSON list with only fields provided in the field list."
        "If the prompt does not specify any particular fields, return null (an empty list)."
    )

    user_message = (
        f"Available fields: {available_fields}\n"
        f"User prompt: {prompt}\n"
        "Return JSON array like [\"Age\", \"Weight\"]."
    )

    try:
        response = ollama.chat(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            format="json",
            options={"temperature": 0.0, "seed": seed}
        )

        selected_fields = json.loads(response.message.content)

        return [
            f for f in selected_fields
            if f in available_fields
        ]

    except Exception:
        logger.exception("Field selection failed. Using all fields.")
        return AVAILABLE_FIELDS


# ===============================
# LOAD ALL EMAILS FROM DB
# ===============================

def load_all_emails(dbConnection):
    cursor = dbConnection.cursor()
    cursor.execute("SELECT email FROM patient_embeddings")
    emails = [row[0] for row in cursor.fetchall()]
    cursor.close()
    return emails


# ===============================
# FETCH TARGET + OTHER PATIENT EMBEDDINGS
# ===============================

def load_patient_field_embeddings(dbConnection, email, fields):
    """Returns dict: field_name → embedding vector or None"""
    vectors = {}

    for f in fields:
        vec = fetch_embedding(dbConnection, email, f)
        vectors[f] = vec

    return vectors


# ===============================
# MAIN SEARCH FUNCTION
# ===============================

def find_similar_patients(dbConnection, target_email: str, prompt: str = "", num_similar: int = NUM_SIMILAR_PATIENTS):
    
    # 1. Load list of all patients
    all_emails = load_all_emails(dbConnection)

    if target_email not in all_emails:
        return [], []

    # 2. Use AI to pick which fields are relevant
    fields_to_compare = select_fields_from_prompt(prompt, AVAILABLE_FIELDS)

    if not fields_to_compare:
        print("original fields:")
        print(fields_to_compare)
        return [], []

    # 3. Load target patient's embeddings
    target_vecs = load_patient_field_embeddings(dbConnection, target_email, fields_to_compare)

    # Fusion: average all NON-None embeddings
    valid = [v for v in target_vecs.values() if v is not None]
    if not valid:
        return [], fields_to_compare  # No data → nothing to compare

    target_embedding = np.mean(valid, axis=0)

    # 4. Compute similarity with all other patients
    similarities = []

    for other_email in all_emails:
        if other_email == target_email:
            continue

        other_vecs = load_patient_field_embeddings(dbConnection, other_email, fields_to_compare)
        other_valid = [v for v in other_vecs.values() if v is not None]

        if not other_valid:
            continue

        other_embedding = np.mean(other_valid, axis=0)

        sim = cosine_similarity(target_embedding, other_embedding)
        similarities.append((other_email, sim))

    # 5. Sort by similarity
    similarities.sort(key=lambda x: x[1], reverse=True)

    top_matches = [email for email, _ in similarities[:num_similar]]

    return top_matches, fields_to_compare