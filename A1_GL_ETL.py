import requests
from requests_oauthlib import OAuth2Session
import pandas as pd
import json

# Replace these with your Intuit Developer credentials
client_id = 'ABxsLRJiGkDrk40adSycRTCvs7B0Jdd1xhai4GA5m5HNj08woe'
client_secret = 'OYRKW4Zncf6gzTa4ANOoiOACoahhSUjNp55f7XPj'
redirect_uri = 'http://localhost:8000/callback'

# Define the scope for QuickBooks Online API
scope = ['com.intuit.quickbooks.accounting']
auth_base_url = "https://appcenter.intuit.com/connect/oauth2"
token_url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
company_id = '9341453379108250'  # Find this ID on your QBO account

# Start the OAuth2 session
oauth_session = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
authorization_url, state = oauth_session.authorization_url(auth_base_url)
print("Visit this URL to authorize the app:", authorization_url)

