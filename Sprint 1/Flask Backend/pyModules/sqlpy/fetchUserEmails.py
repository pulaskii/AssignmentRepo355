from mysql import connector

def fetchUserEmails(dbConnection):

    cursor = dbConnection.cursor()

    query = "SELECT Email, PatientOrProvider FROM users"

    try:
        cursor.execute(query)
    except:
        return 2  # error
    
    results = []   # <-- store ALL rows here

    for (Email, PatientOrProvider) in cursor:
        rowMap = {
            'Email': Email,
            'PatientOrProvider': PatientOrProvider
        }

        # Keep your custom return format
        formatted = [{"field": k, "value": v} for k, v in rowMap.items()]
        results.append(formatted)

    cursor.close()
    dbConnection.close()

    return results