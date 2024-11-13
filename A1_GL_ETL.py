import os
import requests
from requests_oauthlib import OAuth2Session
import pandas as pd
import http.server
import socketserver

# Intuit Developer credentials
client_id = 'ABxsLRJiGkDrk40adSycRTCvs7B0Jdd1xhai4GA5m5HNj08woe'
client_secret = 'OYRKW4Zncf6gzTa4ANOoiOACoahhSUjNp55f7XPj'
redirect_uri = 'http://localhost/callback'  # Update this as needed for Heroku

# QuickBooks Online API details
scope = ['com.intuit.quickbooks.accounting']
auth_base_url = "https://appcenter.intuit.com/connect/oauth2"
token_url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
company_id = '9341453379108250'

# Start OAuth2 session
oauth_session = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
authorization_url, state = oauth_session.authorization_url(auth_base_url)
print("Visit this URL to authorize the app:", authorization_url)

# Heroku assigns a dynamic port
PORT = int(os.environ.get("PORT", 8000))

# Set up and start the HTTP server
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
