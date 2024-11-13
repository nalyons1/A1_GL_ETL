import os
import requests
from requests_oauthlib import OAuth2Session
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

# Intuit Developer credentials
client_id = 'ABxsLRJiGkDrk40adSycRTCvs7B0Jdd1xhai4GA5m5HNj08woe'
client_secret = 'OYRKW4Zncf6gzTa4ANOoiOACoahhSUjNp55f7XPj'
redirect_uri = 'https://a1-gl-etl.herokuapp.com/callback'  # Update for your Heroku URL

# QuickBooks Online API details
scope = ['com.intuit.quickbooks.accounting']
auth_base_url = "https://appcenter.intuit.com/connect/oauth2"
token_url = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
company_id = '9341453379108250'

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
                    # Send a response to the client
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"Authorization complete. Token received.")
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

# Heroku dynamically assigns the port
PORT = int(os.environ.get("PORT", 8000))

# Set up and start the HTTP server with custom handler
with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
