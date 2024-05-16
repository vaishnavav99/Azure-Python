mysql = {
    "host": "mysql-server.mysql.database.azure.com",
    "user": "admin",
    "db": "db",
}

from azure.identity import DefaultAzureCredential,ManagedIdentityCredential
import mysql.connector as connection

# Authenticate with Managed Identity
# managed_identity_client_id='0xxxx-xxxxx-xxxxx-xxx'
# cred = ManagedIdentityCredential(client_id=managed_identity_client_id)

# Authenticate with AD
cred = DefaultAzureCredential()

# Obtain an access token for a specific Azure resource
# Replace 'https://ossrdbms-aad.database.windows.net/' with the resource you want to access
accessToken = cred.get_token('https://ossrdbms-aad.database.windows.net/.default')
#print(accessToken)
try:
    mydb = connection.connect(host=mysql["host"], database =mysql["db"] ,user=mysql["user"], passwd=accessToken.token)
    # Create a cursor object
    cursor = mydb.cursor()
    
    # Execute the query
    cursor.execute('SELECT *  FROM table')
    
    # Fetch all the rows
    results = cursor.fetchall()

    # Print the results
    for row in results:
      print(row)
    cursor.close()
    mydb.close()
