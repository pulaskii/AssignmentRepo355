from mysql import connector


def connectDatabase(user = "root", 
                    password = "password", 
                    host = "127.0.0.1", 
                    database = "medicalrecords", 
                    raiseOnWarnings = True
                    ):

    connectionConfig = {
    'user': '{user}',
    'password': '{password}',
    'host': '{host}',
    'database': '{database}',
    'raise_on_warnings': raiseOnWarnings
    }

    dbConnection = connector.connect(**connectionConfig)

    return dbConnection


def disconnectDatabase(connectionToClose):
    connectionToClose.close()