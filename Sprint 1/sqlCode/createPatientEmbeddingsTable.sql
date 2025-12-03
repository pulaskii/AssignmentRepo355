CREATE TABLE patient_embeddings (
    email VARCHAR(50) PRIMARY KEY,
    age_embedding BLOB,
    sex_embedding BLOB,
    weight_embedding BLOB,
    height_embedding BLOB,
    medications_embedding BLOB,
    allergies_embedding BLOB,
    active_problems_embedding BLOB,
    medical_history_embedding BLOB,
    family_history_embedding BLOB,
    full_record_embedding BLOB
);