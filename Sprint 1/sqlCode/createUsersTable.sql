CREATE TABLE users (
    Email VARCHAR(50) PRIMARY KEY,
        IsRegistered BOOLEAN,

    First_Name VARCHAR(50),
    MiddleNameOrInitial VARCHAR(50),
    Last_Name VARCHAR(50),

    PasswordHash VARCHAR(100) NOT NULL,

    Age INT,
    
    Phone_Number VARCHAR(15),
    
    PatientOrProvider VARCHAR(8),

    Sex VARCHAR(20),

    Weight VARCHAR(20),
    Height VARCHAR(20),

    Medications TEXT,
    Allergies TEXT,
    Active_Problems TEXT,
    Medical_History TEXT,
    Family_History TEXT,

    Date_Updated DATETIME
)