import ollama
import json
import numpy as np
import logging

logger = logging.getLogger(__name__)

# === Config ===
EXCLUDED_FIELDS = ["First_Name", "Last_Name", "Email", "Phone_Number", "Date_Updated"] # I MAY HAVE TO REMOVE THE UNDERSCORES
AVAILABLE_FIELDS = ["Age", "Sex", "Weight", "Height", "Medications", "Allergies", "Active_Problems", "Medical_History", "Family_History"] #TODO Actually get the fields from DB?
LLM_MODEL = "gpt-oss:20b-cloud"
NUM_SIMILAR_PATIENTS = 3 # TODO Make configurable later
seed = 69

# ============================
#  LOAD + VECTORIZE EMBEDDINGS
# ============================

data = np.load("patient_embeddings.npz", allow_pickle=True)

emails = list(data["emails"])
field_names = list(data["fields"])

# Reconstruct dictionary of matrices per field
field_matrices = {
    field: data[f"{field}_matrix"]
    for field in field_names
}

email_to_index = {email: i for i, email in enumerate(emails)}

logger.info(f"Loaded {len(emails)} patients / {len(field_names)} fields")


# ============================
#      COSINE SIMILARITY
# ============================

def cosine_similarity_matrix(target_vec: np.ndarray, matrix: np.ndarray):
    # target_vec: (D,)
    # matrix: (N, D)
    dot = matrix @ target_vec
    denom = (np.linalg.norm(matrix, axis=1) * np.linalg.norm(target_vec))
    return dot / denom


# ============================
#   PROMPT FIELD SELECTION
# ============================

def select_fields_from_prompt(prompt: str, available_fields: list[str]) -> list[str]:
    if available_fields is None:
        available_fields = AVAILABLE_FIELDS

    system_message = (
        "You are an assistant that identifies which fields of a patient record are relevant "
        "to a user's query. Return a JSON list of field names from the patient record "
        "that are most relevant to compare for similarity. Only include fields from the provided list."
    )
    user_message = (
        f"Available fields: {available_fields}\n"
        f"User prompt: {prompt}\n"
        "Return JSON array of field names, e.g., [\"Age\", \"Weight\", \"Height\"]."
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
        return [f for f in selected_fields if f in available_fields and f not in EXCLUDED_FIELDS]
    except Exception:
        logger.exception("LLM field selection failed, falling back to default fields")
        return AVAILABLE_FIELDS


# ============================
#     MAIN SEARCH FUNCTION
# ============================

def find_similar_patients(target_email: str, prompt: str = ""):
    if target_email not in email_to_index:
        return [], []

    idx = email_to_index[target_email]
    fields_to_compare = select_fields_from_prompt(prompt, field_names)

    # Fallback if no fields selected
    if not fields_to_compare:
        fields_to_compare = AVAILABLE_FIELDS

    # -------- Vectorize embedding fusion --------
    target_vec = np.mean(
        np.vstack([field_matrices[f][idx] for f in fields_to_compare]),
        axis=0
    ).astype(np.float32)

    combined_matrix = np.mean(
        np.stack([field_matrices[f] for f in fields_to_compare]),
        axis=0
    )

    sims = cosine_similarity_matrix(target_vec, combined_matrix)
    sims[idx] = -np.inf  # Remove self-match

    top_indices = np.argsort(sims)[-NUM_SIMILAR_PATIENTS:][::-1]
    top_emails = [emails[i] for i in top_indices]

    return top_emails, fields_to_compare