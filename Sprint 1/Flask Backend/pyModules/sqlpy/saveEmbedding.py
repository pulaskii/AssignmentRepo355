import numpy as np
import mysql.connector

def save_embedding(dbConnection, email, field_name, embedding):
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

    # If embedding is empty or None, save as NULL
    if embedding is None:
        embedding_bytes = None  # this will be stored as NULL
    else:
        embedding_bytes = mysql.connector.Binary(embedding.astype(np.float32).tobytes())


    cursor = dbConnection.cursor(prepared=True)
    
    query = f"""
    INSERT INTO patient_embeddings (email, {column})
    VALUES (%s, %s)
    ON DUPLICATE KEY UPDATE {column} = %s
    """

    try:
        cursor.execute(query, (email.encode('utf-8'), embedding_bytes, embedding_bytes))
    except Exception as e:
        print("[ERROR] Failed to execute query:")
        print(query)
        print(f"Parameters: {(email, embedding_bytes[:16] if embedding_bytes else None)} ...")
        raise e
    
    dbConnection.commit()
    cursor.close()
    dbConnection.close()