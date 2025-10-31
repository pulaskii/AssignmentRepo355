from mysql import connector

def addNewUser( firstName,
                lastName,
                userEmail,
                phoneNumber,
                password,
                patientOrDoctor,
                dbConnection 
                ):
    
    addUser = ("INSERT INTO Users"
                 "(Email, FirstName, LastName, Password, Phone, PatientOrDoctor)"
                 "VALUES ((%(EmailVal)s)," \
                 "(%(FirstNameVal)s)," \
                 "(%(LastNameVal)s)," \
                 "(%(PasswordVal)s)," \
                 "(%(PhoneVal)s)," \
                 "(%(PatientOrDoctorVal)s))" #PatientOrDocotorVal will be equal to either "option_patient" or "option_provider"
    )

    dataUser = {
    'EmailVal': userEmail,
    'FirstNameVal': firstName,
    'LastNameVal': lastName,
    'PasswordVal': password,
    'PhoneVal': phoneNumber,
    'PatientOrDoctorVal': patientOrDoctor
    }


    cursor = dbConnection.cursor()

    cursor.execute(addUser, dataUser)
    cursor.commit()

    cursor.close()

    dbConnection.close()

    return 1


def addNewUserTest():
    print("import successful! :)")