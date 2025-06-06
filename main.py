from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from app import auth
from app.routes import news
from app.database import Base, engine


app = FastAPI()  # Create FastAPI instance


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(news.router)  # Include the news router

Base.metadata.create_all(bind=engine)  # Create the database tables


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    """
    Redirect to the API documentation.
    """
    return {"message": "Welcome to the API. Visit /docs for documentation."}


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate the client and return an access token.
    """
    # Check if the client credentials are valid
    if not auth.authenticate_client(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid client credentials",
        )

    access_token = auth.create_access_token(
        data={"sub": form_data.username}
    )  # Create the access token
    return {"access_token": access_token, "token_type": "bearer"}
