# 🚀 Blockstak Backend Evaluation Project

A FastAPI-based backend application integrating NewsAPI with OAuth2 Client Credentials authentication, built for the Blockstak backend developer evaluation.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Installation](#installation)
- [Running the Server](#running-the-server)
- [Docker Setup](#docker-setup)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
  - [Root Endpoint](#root-endpoint)
  - [Authentication Endpoint](#authentication-endpoint)
  - [News Endpoints](#news-endpoints)
  - [Headlines Endpoints](#headlines-endpoints)
- [Running Tests](#running-tests)
- [Development](#development)

## 🔍 Project Overview

This project is a backend service built with FastAPI that integrates with the NewsAPI to fetch and manage news articles. It implements OAuth2 Client Credentials authentication to secure all endpoints.

## ✨ Features

- OAuth2 Client Credentials authentication
- Integration with NewsAPI
- FastAPI for high-performance API development
- SQLAlchemy ORM for database operations
- Comprehensive test suite with pytest
- Docker containerization
- Pagination for news retrieval
- Filtering options for headlines
- Ability to save news articles to the database

## 📁 Project Structure

```
├── app/
│   ├── __init__.py
│   ├── auth.py           # Authentication functionality
│   ├── config.py         # Configuration management
│   ├── database.py       # Database connection
│   ├── models.py         # SQLAlchemy models
│   └── routes/           # API routes
│       ├── __init__.py
│       ├── headlines.py  # Headlines endpoints
│       └── news.py       # News endpoints
├── tests/                # Test files
├── .env.example          # Example environment variables
├── Dockerfile            # Docker configuration
├── main.py               # Application entry point
├── pytest.ini            # Pytest configuration
├── requirements.txt      # Dependencies
└── README.md             # Project documentation
```

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.12+
- NewsAPI key (get one at [newsapi.org](https://newsapi.org))
- Git

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
NEWS_API_KEY=your_news_api_key
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./news_app.db
```

You can use the provided `.env.example` as a template:

```bash
cp .env.example .env
```

Then edit the `.env` file with your actual values.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/blockstak-backend.git
   cd blockstak-backend
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Running the Server

Start the application with Uvicorn:

```bash
uvicorn main:app --reload
```

Visit:
- API Documentation: http://localhost:8000/docs
- Root Endpoint: http://localhost:8000

## 🐳 Docker Setup

To build and run the application using Docker:

1. Build the Docker image:
   ```bash
   docker build -t blockstak-backend .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env blockstak-backend
   ```

The API will be available at http://localhost:8000.

## 🔐 Authentication

This API uses OAuth2 Client Credentials flow for authentication:

1. **Get an access token:**

   ```bash
   curl -X POST "http://localhost:8000/token" \
     -d "username=your_client_id&password=your_client_secret" \
     -H "Content-Type: application/x-www-form-urlencoded"
   ```

   The response will include an access token:
   ```json
   {
     "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
     "token_type": "bearer"
   }
   ```

2. **Use the token to access protected endpoints:**

   ```bash
   curl -X GET "http://localhost:8000/news/" \
     -H "Authorization: Bearer your_access_token"
   ```

## 📚 API Endpoints

### Root Endpoint

- **GET /**
  - Redirects to API documentation
  - No authentication required
  - Response: `{"message": "Welcome to the API. Visit /docs for documentation."}`

### Authentication Endpoint

- **POST /token**
  - Get access token using client credentials
  - Request body: `username` (client_id) and `password` (client_secret)
  - Response: Access token and token type

### News Endpoints

- **GET /news/**
  - Fetch all news with pagination
  - Query parameters:
    - `page`: Page number (default: 1)
    - `page_size`: Items per page (default: 10)
  - Authentication required
  - Response: News articles with pagination info

- **POST /news/save-latest**
  - Fetch and save latest news articles to database
  - Authentication required
  - Response: Summary of saved articles

### Headlines Endpoints

- **GET /news/headlines/country/{country_code}**
  - Fetch top headlines by country code
  - Path parameters:
    - `country_code`: Two-letter country code (e.g., "us", "gb")
  - Authentication required
  - Response: Headlines from specified country

- **GET /news/headlines/source/{source_id}**
  - Fetch top headlines by source ID
  - Path parameters:
    - `source_id`: News source ID (e.g., "bbc-news")
  - Authentication required
  - Response: Headlines from specified source

- **GET /news/headlines/filter**
  - Filter headlines by country and/or source
  - Query parameters:
    - `country`: Two-letter country code (optional)
    - `source`: Source ID (optional)
  - Authentication required
  - Response: Filtered headlines

## 🧪 Running Tests

Run tests with pytest:

```bash
pytest
```

For test coverage report:

```bash
pytest --cov=app --cov-report=term-missing
```

## 👨‍💻 Development

### Code Formatting

This project uses `ruff` for code formatting. To format your code:

```bash
ruff --fix .
```

### Adding New Routes

To add new endpoints:

1. Create a new file in `app/routes/`
2. Define your router and endpoints
3. Import and include your router in `main.py` or an existing router