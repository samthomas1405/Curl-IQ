# Development Setup Guide

This guide will help you set up the CurlLabs project for local development.

## Prerequisites

Before you begin, make sure you have the following installed:

- **Node.js 18+** and npm
- **Python 3.12** (⚠️ **Important**: Python 3.13 is not yet supported due to package compatibility issues)
- **Docker Desktop** (for PostgreSQL and Redis)
- **Git**

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Curl-IQ
```

### 2. Start Database Services

Start PostgreSQL and Redis using Docker:

```bash
docker-compose up -d
```

**Note**: If you have a local PostgreSQL running on port 5432, Docker will use port 5433 instead. Make sure your `.env` file uses the correct port (see step 3).

Verify containers are running:
```bash
docker ps
```

You should see `curliq-postgres` and `curliq-redis` containers.

### 3. Backend Setup

```bash
cd backend

# Create virtual environment with Python 3.12
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

**Create `.env` file** in the `backend/` directory:

```env
# Database - Use port 5433 if you have local PostgreSQL on 5432
DATABASE_URL=postgresql://curliq:curliq_dev_password@localhost:5433/curliq

# Redis
REDIS_URL=redis://localhost:6379/0

# Security - Generate a new secret key for each developer
SECRET_KEY=your-secret-key-here-min-32-chars

# Algorithm
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Weather API (optional - get free key from https://openweathermap.org/api)
WEATHER_API_KEY=
WEATHER_API_URL=https://api.openweathermap.org/data/2.5

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
```

**Generate a SECRET_KEY**:
```bash
python3 -c 'import secrets; print(secrets.token_urlsafe(32))'
```

**Start the backend server**:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

### 4. Frontend Setup

Open a **new terminal** (keep backend running):

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Port Configuration

### Default Ports

- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **PostgreSQL (Docker)**: `5433` (or `5432` if no local PostgreSQL)
- **Redis (Docker)**: `6379`

### If You Have Local PostgreSQL

If you have PostgreSQL installed locally on port 5432, Docker will automatically use port 5433. Make sure your `backend/.env` file uses:

```env
DATABASE_URL=postgresql://curliq:curliq_dev_password@localhost:5433/curliq
```

## Environment Variables Summary

### Backend (`backend/.env`)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | ✅ | PostgreSQL connection string (port 5433 if local PG exists) |
| `SECRET_KEY` | ✅ | JWT secret key (generate with Python secrets module) |
| `REDIS_URL` | ✅ | Redis connection string |
| `WEATHER_API_KEY` | ❌ | Optional OpenWeatherMap API key |

### Frontend (`frontend/.env.local`)

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | ✅ | Backend API URL (default: http://localhost:8000) |

## Common Issues and Solutions

### Issue: Python 3.13 Compatibility Errors

**Problem**: Packages fail to install with Python 3.13

**Solution**: Use Python 3.12
```bash
# Check Python version
python3 --version

# If you have Python 3.13, install 3.12
brew install python@3.12

# Create venv with Python 3.12
python3.12 -m venv venv
```

### Issue: Port 5432 Already in Use

**Problem**: Docker can't bind to port 5432

**Solution**: Docker will automatically use port 5433. Update your `DATABASE_URL`:
```env
DATABASE_URL=postgresql://curliq:curliq_dev_password@localhost:5433/curliq
```

### Issue: Missing `email-validator`

**Problem**: `ImportError: email-validator is not installed`

**Solution**: Install it:
```bash
pip install email-validator
```

### Issue: Docker Containers Not Starting

**Problem**: `Cannot connect to the Docker daemon`

**Solution**: 
1. Make sure Docker Desktop is running
2. Wait for Docker Desktop to fully start (check menu bar icon)
3. Try again: `docker-compose up -d`

### Issue: Database Connection Failed

**Problem**: `password authentication failed`

**Solution**: 
1. Check that Docker containers are running: `docker ps`
2. Verify `DATABASE_URL` in `.env` matches docker-compose.yml credentials
3. Check the port (5433 if local PostgreSQL exists)

## Development Workflow

### Starting Development

1. **Terminal 1 - Database**:
   ```bash
   docker-compose up -d
   ```

2. **Terminal 2 - Backend**:
   ```bash
   cd backend
   source venv/bin/activate
   uvicorn main:app --reload
   ```

3. **Terminal 3 - Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

### Stopping Development

- **Backend/Frontend**: Press `Ctrl+C` in respective terminals
- **Database**: `docker-compose down` (or leave running)

### Database Migrations

The app auto-creates tables on first run. For manual migrations:

```bash
cd backend
source venv/bin/activate
alembic upgrade head
```

## Testing the Setup

1. **Check Backend**: Visit `http://localhost:8000/docs` - you should see the API documentation
2. **Check Frontend**: Visit `http://localhost:3000` - you should see the login page
3. **Test Registration**: Create an account and verify you can log in

## Project Structure

```
CurlLabs/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/v1/      # API endpoints
│   │   ├── core/        # Config, database, security
│   │   ├── models/      # SQLAlchemy models
│   │   └── schemas/     # Pydantic schemas
│   ├── .env             # Backend environment variables
│   └── requirements.txt
├── frontend/            # Next.js frontend
│   ├── app/             # Next.js pages
│   ├── components/      # React components
│   ├── lib/             # API client, utilities
│   └── .env.local       # Frontend environment variables
└── docker-compose.yml   # Docker services
```

## Additional Resources

- **API Documentation**: `http://localhost:8000/docs` (when backend is running)
- **Backend README**: See `README.md` for architecture details
- **Setup Troubleshooting**: See `SETUP.md` for more detailed setup instructions

## Getting Help

If you encounter issues:

1. Check this guide's "Common Issues" section
2. Verify all prerequisites are installed
3. Ensure Docker containers are running
4. Check that environment variables are set correctly
5. Review the error messages in terminal output

## Next Steps

Once setup is complete:

1. ✅ Backend running on port 8000
2. ✅ Frontend running on port 3000
3. ✅ Database containers running
4. ✅ Can access API docs at `/docs`
5. ✅ Can register/login in the frontend

You're ready to start developing! 🎉
