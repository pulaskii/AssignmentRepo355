from mysql import connector


def connectDatabase(user = "test", 
                    password = "r39Cfz1BE%n&al", 
                    host = "127.0.0.1", 
                    database = "medicalrecords", 
                    raiseOnWarnings = True
                    ):

    connectionConfig = {
    'user': user,
    'password': password,
    'host': host,
    'database': database,
    'raise_on_warnings': raiseOnWarnings
    }

    dbConnection = connector.connect(**connectionConfig)
    # dbConnection = connector.connect(
    #     host = "localhost"
    #     user = 
    # )

    return dbConnection


def disconnectDatabase(connectionToClose):
    connectionToClose.close()