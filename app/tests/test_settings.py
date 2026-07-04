from app.config.settings import settings

print("Database URL:", settings.DATABASE_URL)
print("Algorithm:", settings.ALGORITHM)
print("Token Expiry:", settings.ACCESS_TOKEN_EXPIRE_MINUTES)
print("Secret Key:", settings.SECRET_KEY[:8] + "...")