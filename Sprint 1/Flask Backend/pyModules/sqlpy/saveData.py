from mysql import connector

def saveUserData(userEmail,
                 dbConnection,
                 columnToSet,
                 valueToSet
                 ):
    

        # 1. WHITELIST columns (CRITICALLY IMPORTANT)
    allowed_columns = {"First_Name", "Last_Name", "Phone_Number", "Age", "Address", "PasswordHash", "Sex", "Weight", "Height", 
                       "Medications", "Allergies", "Active_Problems", "Medical_History", "Family_History", "Date_Updated"}
    if columnToSet not in allowed_columns:
        raise ValueError(f"Invalid or unsafe column name: {columnToSet}")
    

    cursor = dbConnection.cursor() # make cursor

    query = ("UPDATE users " 
            f"SET {columnToSet} = %(changeVal)s "
            "WHERE Email = %(emailVal)s") # sql update stmt
    
    queryData = {
        'changeVal': valueToSet,
        'emailVal': userEmail
    } # sql updata vals
    
    try:
        cursor.execute(query, queryData) # execute stmt
    except:
        return 2
    
    if cursor.rowcount == 0:
        print("no rows")
        return {"status": 4, "error": "No user with that email"}


    try:
        dbConnection.commit()
    except:
        return 3

    cursor.close() # close cursor
    dbConnection.close() # close connection


    return 1

