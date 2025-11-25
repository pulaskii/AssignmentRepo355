import numpy as np

def get_embedding(dbConnection, email, field_name):
    """Retrieve a single embedding from MySQL."""
    
    column_map = {
        "Age": "age_embedding",
        "Sex": "sex_embedding",
        "Weight": "weight_embedding",
        "Height": "height_embedding",
        "Medications": "medications_embedding",
        "Allergies": "allergies_embedding",
        "Active_Problems": "active_problems_embedding",
        "Medical_History": "medical_history_embedding",
        "Family_History": "family_history_embedding",
        "Full_Record": "full_record_embedding"
    }

    column = column_map.get(field_name)
    if column is None:
        raise ValueError(f"Unknown field: {field_name}")

    cursor = dbConnection.cursor(prepared=True)

    query = f"SELECT {column} FROM patient_embeddings WHERE email=%s"
    cursor.execute(query, (email.encode("utf-8"),))

    row = cursor.fetchone()
    cursor.close()
    dbConnection.close()

    # No row or NULL field → return None
    if row is None or row[0] is None:
        return None

    # Convert BLOB → float32 numpy array
    try:
        return np.frombuffer(row[0], dtype=np.float32)
    except Exception as e:
        print(f"[ERROR] Failed to parse embedding for {field_name} ({email}): {e}")
        return None