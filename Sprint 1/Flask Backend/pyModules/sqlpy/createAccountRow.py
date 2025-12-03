from mysql import connector
from mysql.connector import errorcode
import mysql


def addNewUser( firstName,
                lastName,
                userEmail,
                phoneNumber,
                password,
                PatientOrProvider,
                dbConnection 
                ):
    
    returnVal = 1

    addUser = ("INSERT INTO users"
                 "(Email, First_Name, Last_Name, PasswordHash, Phone_Number, PatientOrProvider)"
                 "VALUES ((%(EmailVal)s)," \
                 "(%(First_NameVal)s)," \
                 "(%(Last_NameVal)s)," \
                 "(%(PasswordVal)s)," \
                 "(%(Phone_NumberVal)s)," \
                 "(%(PatientOrProviderVal)s))"
    )   
    




    dataUser = {
    'EmailVal': userEmail,
    'First_NameVal': firstName,
    'Last_NameVal': lastName,
    'PasswordVal': password,
    'Phone_NumberVal': phoneNumber,
    'PatientOrProviderVal': PatientOrProvider
    }


    cursor = dbConnection.cursor()

    try:
        cursor.execute(addUser, dataUser)
    except  mysql.connector.Error as err:
        if err.errno == 1062:
            returnVal = 2
    
    try:
        dbConnection.commit()
    except  mysql.connector.Error as err:
        if err.errno == 1062:
            returnVal = 3

    cursor.close() # close cursor
    dbConnection.close() # close connection

    return returnVal


def addNewUserTest():
    print("import successful! :)")