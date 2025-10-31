from mysql import connector
from mysql.connector import errorcode

def addNewUser( firstName,
                lastName,
                userEmail,
                phoneNumber,
                password,
                PatientOrProvider,
                dbConnection 
                ):
    
    returnVal = 1

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

    try:
        cursor.execute(addUser, dataUser)
    except  mysql.connector.Error as err:
        if err.errno == 1062:
            returnVal = 2
    
    try:
        cursor.commit()
    except  mysql.connector.Error as err:
        if err.errno == 1062:
            returnVal = 3

    cursor.close()
    dbConnection.close()

    return returnVal


def addNewUserTest():
    print("import successful! :)")