"""
This script will generate a JSON Web Token (JWT) for a GitHub App using app_id and
private key content. It is adopted from official GitHub Apps [documentation](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-json-web-token-jwt-for-a-github-app)
Usage: generate_jwt.py <app-id> <app-private-key>
"""
#!/usr/bin/env python3

import os
import sys
import time
import jwt

# Get the App ID
app_id = sys.argv[1]

# Get the private key
private_key = sys.argv[2]

# Write private key to pem
with open("pr-app.private.pem", "w") as file:
    file.write(private_key)

# Open PEM
with open("pr-app.private.pem", "rb") as pem_file:
    signing_key = jwt.jwk_from_pem(pem_file.read())

payload = {
    # Issued at time
    "iat": int(time.time()),
    # JWT expiration time (10 minutes maximum)
    "exp": int(time.time()) + 300,
    # GitHub App's identifier
    "iss": app_id,
}

# Create JWT using PEM
jwt_instance = jwt.JWT()
encoded_jwt = jwt_instance.encode(payload, signing_key, alg="RS256")

# Remove PEM file
os.remove("pr-app.private.pem")

print(f"{encoded_jwt}")