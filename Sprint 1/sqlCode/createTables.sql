CREATE TABLE Users (
    Email VARCHAR(50) PRIMARY KEY,
        IsRegistered BOOLEAN,

    FirstName VARCHAR(50),
    MiddleNameOrInitial VARCHAR(50),
    LastName VARCHAR(50),

    PasswordHash VARCHAR(100) NOT NULL,

    Age INT,
    
    Phone VARCHAR(15),
    
    PatientOrProvider VARCHAR(8)
)