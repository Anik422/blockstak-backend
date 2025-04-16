from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app import auth
from app.routes import news
from app.database import Base, engine


app = FastAPI() # Create FastAPI instance

app.include_router(news.router) # Include the news router

Base.metadata.create_all(bind=engine) # Create the database tables


# Define the root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}

# Define the token endpoint for client authentication
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not auth.authenticate_client(form_data.username, form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid client credentials")

    access_token = auth.create_access_token(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}
