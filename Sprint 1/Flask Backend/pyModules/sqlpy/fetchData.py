from mysql import connector

def fetchUserData(userEmail,
                  dbConnection
                  ):

    cursor = dbConnection.cursor()

    query = ("SELECT FirstName, LastName, Age, Phone,  FROM users "
         "WHERE Email EQUALS %(emailVal)s") # fetch user data
    
    queryData = {
      'emailVal': userEmail 
    } # user primary key
    
    try:
        cursor.execute(query, queryData) # execute the changes
    except:
        return 2 #errorval
    try:
        dbConnection.commit() #save the changes
    except:
        return 3 #errorval
    
    returnMap = {}
    for (FirstName, LastName, Age, Phone,) in cursor:
        # iterate through a set of tuples
        # the tuples are the rows, but we only fetched one
        returnMap = {
            'FirstNameVal': FirstName,
            'LastNameVal': LastName,
            'AgeVal': Age,
            'PhoneVal': Phone
        } # make a return map for the row




    cursor.close() # close cursor
    dbConnection.close() # close connection

    return returnMap #return the map

