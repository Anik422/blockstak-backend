import os
from dotenv import load_dotenv

# Add this line to be explicit about pat
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'), override=True)


CLIENT_ID = os.getenv("CLIENT_ID", "fallback-id")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "fallback-secret")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
SECRET_KEY = "blockstak-secret-key"
ALGORITHM = "HS256"
print("CLIENT_ID from .env =", CLIENT_ID)
