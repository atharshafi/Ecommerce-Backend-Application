import secrets

# Generate a random URL-safe string with 32 bytes
new_secret_key = secrets.token_urlsafe(32)
print(new_secret_key) 