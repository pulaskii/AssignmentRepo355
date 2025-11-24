from mysql import connector

def fetchUserData(userEmail,
                  dbConnection
                  ):

    cursor = dbConnection.cursor()

    query = ("SELECT First_Name, Last_Name, Age, Phone_Number, Sex, Weight, Height, Medications, Allergies, Active_Problems, "
    "Medical_History, Family_History, Date_Updated  FROM users "
         "WHERE Email = %(emailVal)s") # fetch user data
    
    queryData = {
      'emailVal': userEmail 
    } # user primary key
    
    try:
        cursor.execute(query, queryData) # execute the changes
    except:
        return 2 #errorval
    
    returnMap = {}
    for (First_Name, Last_Name, Age, Phone_Number, Sex, Weight, Height, Medications, Allergies, Active_Problems, Medical_History, 
         Family_History, Date_Updated) in cursor:
        # iterate through a set of tuples
        # the tuples are the rows, but we only fetched one
        returnMap = {
            'First_Name': First_Name,
            'Last_Name': Last_Name,
            'Age': Age,
            'Phone_Number': Phone_Number,
            'Sex' : Sex,
            'Weight': Weight,
            'Height': Height,
            'Medications': Medications,
            'Allergies': Allergies,
            'Active_Problems': Active_Problems,
            'Medical_History': Medical_History,
            'Family_History': Family_History,
            'Date_Updated': Date_Updated
        } # make a return map for the row


    cursor.close() # close cursor
    dbConnection.close() # close connection

    # Updated to stop it from sorting alphabetically
    return [{"field": k, "value": v} for k, v in returnMap.items()]