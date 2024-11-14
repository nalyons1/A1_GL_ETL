import os
import requests
from requests_oauthlib import OAuth2Session
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
import pandas as pd

# Intuit Developer credentials
client_id = 'ABRJTQ4dR43hWwyTSTiwC1n8E7suExD0XpwVoQsvdu7MPfqLtW'
client_secret = '2pChmqkYU1wM6jVFxtHRzJwGoMejYQ45r8WWFbKo'
redirect_uri = 'https://a1-gl-etl.herokuapp.com/callback'  # Update for your Heroku URL

# QuickBooks Online API details
scope = ['com.intuit.quickbooks.accounting']
auth_base_url = "https://appcenter.intuit.com/connect/oauth2"
token_url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
sandbox_company_id = '9341453379095730'

# Start OAuth2 session
oauth_session = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
authorization_url, state = oauth_session.authorization_url(auth_base_url)
print("Visit this URL to authorize the app:", authorization_url)

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse URL path
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/callback':
            # Handle the callback and exchange for token
            query_params = parse_qs(parsed_path.query)
            if 'code' in query_params:
                code = query_params['code'][0]
                try:
                    # Exchange authorization code for token
                    token = oauth_session.fetch_token(
                        token_url,
                        client_secret=client_secret,
                        code=code
                    )
                    print("Access token received:", token)

                    # Fetch and display customer data
                    customer_data = self.get_customer_data(token)
                    html_data = customer_data.to_html() if customer_data is not None else "Error fetching data."

                    # Send a response with HTML table
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(html_data.encode())
                except Exception as e:
                    print("Error exchanging token:", e)
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(b"Error during token exchange.")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Authorization code not found in the callback.")
        else:
            super().do_GET()

    def get_customer_data(self, token):
        url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{sandbox_company_id}/query?query=SELECT * FROM Customer"
        headers = {
            'Authorization': f"Bearer {token['access_token']}",
            'Content-Type': 'application/json'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            customers = data['QueryResponse']['Customer']
            return pd.DataFrame(customers)
        else:
            print(f"Failed to retrieve data: {response.status_code}")
            return None

# Heroku dynamically assigns the port
PORT = int(os.environ.get("PORT", 8000))

# Set up and start the HTTP server with custom handler
with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
