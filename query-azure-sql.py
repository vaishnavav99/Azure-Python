import pyodbc
from azure.identity import ManagedIdentityCredential,DefaultAzureCredential
import struct

def get_access_token_bytes(token):
    token_bytes = token.encode('utf-16-le')
    token_struct = struct.pack('=i', len(token_bytes)) + token_bytes
    return token_struct

try:
    # Obtain the managed identity credential
    #credential = ManagedIdentityCredential(client_id='065a3f5d-e575-48bf-adf0-e39e38d191d1')
    credential=DefaultAzureCredential()

    # Acquire the token for the SQL Database
    token = credential.get_token("https://database.windows.net/.default")

    # Extract the token string
    access_token = get_access_token_bytes(token.token)

    # Database connection details
    server = 'csprod004fg.database.windows.net'
    database = 'csprod004'

    # Create the connection string
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};ApplicationIntent=readonly"

    # Establish the connection
    with pyodbc.connect(connection_string, attrs_before={1256: access_token}) as conn:
        with conn.cursor() as cursor:
            # Execute a sample query
            cursor.execute("SELECT TOP 10 * FROM sys.dm_db_resource_stats")
            rows = cursor.fetchall()
            for row in rows:
                print(row)

except Exception as e:
    print(f"An error occurred: {e}")
