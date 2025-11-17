from mysql import connector

def saveUserData(userEmail,
                 dbConnection,
                 columnToSet,
                 valueToSet
                 ):
    
    returnVal = 1 #baseCase
    cursor = dbConnection.cursor() # make cursor

    query = ("UPDATE users SET " \
            "%(columnToSetVal)s = %(changeVal)s"
            "WHERE Email EQUALS %(emailVal)s") # sql update stmt
    
    queryData = {
        'columnToSetVal': columnToSet,
        'changeVal': valueToSet,
        'emailVal': userEmail
    } # sql updata vals
    
    try:
        cursor.execute(query, queryData) # execute stmt
    except:
        return 2


    cursor.close() # close cursor
    dbConnection.close() # close connection


    return returnVal

