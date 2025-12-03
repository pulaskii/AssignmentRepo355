from mysql import connector

def fetchAccessMap(userEmail,
                   dbConnection,
                   patientOrDoctor # "doctor" or "patient"
                   ):
    
    cursor = dbConnection.cursor()

    if patientOrDoctor == "doctor":
        query = ("SELECT u.First_Name, u.Last_Name, u.Email FROM users u "
                 "JOIN accessMap AM " 
                 "ON AM.patient = u.Email "
                 "WHERE AM.doctor = %(EmailVal)s"
                )
    else:
        query = ("SELECT u.First_Name, u.Last_Name, u.Email FROM users u " 
                 "JOIN accessMap AM "
                 "ON AM.doctor = u.Email "
                 "WHERE AM.patient = %(EmailVal)s"
                )


    queryData = {
      'EmailVal': userEmail 
    } # user primary key
    
    try:
        cursor.execute(query, queryData) # execute the changes
    except:
        return 2 #errorval


    returnList = []
    for (First_Name, Last_Name, Email) in cursor:
        # iterate through a set of tuples
        # the tuples are the rows
        returnList.append((First_Name, Last_Name, Email)) 


    cursor.close() # close cursor
    dbConnection.close() # close connection

    return returnList #return the map

