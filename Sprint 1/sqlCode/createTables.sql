CREATE TABLE Users (
    Email VARCHAR(50) PRIMARY KEY,
    IsRegistered BOOLEAN,

    FirstName VARCHAR(50) NOT NULL,
    MiddleNameOrInitial VARCHAR(50) NOT NULL,
    LastName VARCHAR(50),

    PasswordHash VARCHAR(100) NOT NULL,

    Age INT CHECK(Age >= 18 AND Age <= 99),
    Phone INT(10),
    PatientOrDoctor VARCHAR(7) CHECK(PatientOrDoctor == 'patient' or PatientOrDoctor == 'doctor')
)


