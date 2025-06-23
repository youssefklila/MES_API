"""JWT configuration settings."""

# JWT Settings
SECRET_KEY = "your-secret-key-keep-it-secret"  # In production, use a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 525600  # 365 days (365 * 24 * 60 = 525,600 minutes)