from mysql import connector

def fetchAnonymizedUserData(userEmail,
                  dbConnection
                  ):

    cursor = dbConnection.cursor()

    query = ("SELECT Age, Sex, Weight, Height, Medications, Allergies, Active_Problems, "
    "Medical_History, Family_History  FROM users "
         "WHERE Email = %(emailVal)s") # fetch user data
    
    queryData = {
      'emailVal': userEmail 
    } # user primary key
    
    try:
        cursor.execute(query, queryData) # execute the changes
    except:
        return 2 #errorval
    
    returnMap = {}
    for (Age, Sex, Weight, Height, Medications, Allergies, Active_Problems, Medical_History, 
         Family_History) in cursor:
        # iterate through a set of tuples
        # the tuples are the rows, but we only fetched one
        returnMap = {
            'Age': Age,
            'Sex' : Sex,
            'Weight': Weight,
            'Height': Height,
            'Medications': Medications,
            'Allergies': Allergies,
            'Active_Problems': Active_Problems,
            'Medical_History': Medical_History,
            'Family_History': Family_History,
        } # make a return map for the row


    cursor.close() # close cursor
    dbConnection.close() # close connection

    # Updated to stop it from sorting alphabetically
    return [{"field": k, "value": v} for k, v in returnMap.items()]