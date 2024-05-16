from azure.identity import ManagedIdentityCredential
#from azure.identity import DefaultAzureCredential
managed_identity_client_id='0xxxx-xxxxx-xxxxx-xxx'
cred = ManagedIdentityCredential(client_id=managed_identity_client_id)
#cred = DefaultAzureCredential()
# acquire token
accessToken = cred.get_token('https://ossrdbms-aad.database.windows.net/.default')
print(accessToken)
