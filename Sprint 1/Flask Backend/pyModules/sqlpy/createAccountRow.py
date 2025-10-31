from mysql import connector

def addNewUser( firstName,
                lastName,
                userEmail,
                phoneNumber,
                password,
                PatientOrProvider,
                dbConnection 
                ):
    
    addUser = ("INSERT INTO Users"
                 "(Email, FirstName, LastName, PasswordHash, Phone, PatientOrProvider)"
                 "VALUES ((%(EmailVal)s)," \
                 "(%(FirstNameVal)s)," \
                 "(%(LastNameVal)s)," \
                 "(%(PasswordVal)s)," \
                 "(%(PhoneVal)s)," \
                 "(%(PatientOrProviderVal)s))" #PatientOrDocotorVal will be equal to either "option_patient" or "option_provider"
    )   
    
    if PatientOrProvider == "option_patient":
        PatientOrProvider = "Patient"
    elif PatientOrProvider == "option_Provider":
        PatientOrProvider = "Provider"



    dataUser = {
    'EmailVal': userEmail,
    'FirstNameVal': firstName,
    'LastNameVal': lastName,
    'PasswordVal': password,
    'PhoneVal': phoneNumber,
    'PatientOrProviderVal': PatientOrProvider
    }


    cursor = dbConnection.cursor()

    cursor.execute(addUser, dataUser)
    cursor.commit()

    cursor.close()

    dbConnection.close()

    return 1


def addNewUserTest():
    print("import successful! :)")