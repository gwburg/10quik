import onedrivesdk_fork as onedrivesdk

def upload():
    redirect_uri = 'http://localhost:8080/'
    client_id = None # add client id here
    client_secret = None # add client secret here
    api_base_url = 'https://api.onedrive.com/v1.0/'
    scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

    http_provider = onedrivesdk.HttpProvider()
    auth_provider = onedrivesdk.AuthProvider(
        http_provider=http_provider,
        client_id=client_id,
        scopes=scopes)

    auth_provider.load_session()
    auth_provider.refresh_token()
    client = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)

    path = None # add path to excel file here
    returned_item = client.item(drive='me', id='root').children['table.xlsx'].upload(path)
