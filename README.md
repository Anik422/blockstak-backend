# 🚀 Blockstak Backend Evaluation Project

A FastAPI-based backend application integrating NewsAPI with OAuth2 Client Credentials authentication.  
Built for the Blockstak backend developer evaluation.

---

## 📁 Project Structure


---

## ✅ Step 1: Project Setup

### 🛠️ Dependencies Installed

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/) - ASGI server
- [python-dotenv](https://pypi.org/project/python-dotenv/) - For loading `.env` config

### 🌐 How to Run the Server

1. Install the dependencies:

```bash
pip install -r requirements.txt
```
2. Run the server:

```bash
uvicorn main:app --reload

```
3. Visit in browser:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Root Endpoint: http://localhost:8000
