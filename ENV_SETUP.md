# Environment Variables Setup Guide

## Backend Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

### Required for Basic Functionality

```env
# Database - Use the default if running docker-compose
DATABASE_URL=postgresql://curliq:curliq_dev_password@localhost:5432/curliq

# Redis - Use the default if running docker-compose
REDIS_URL=redis://localhost:6379/0

# Security - CHANGE THIS IN PRODUCTION!
SECRET_KEY=your-secret-key-change-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS - Add your frontend URLs
CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]
```

### Optional (for Weather Features)

```env
# Weather API - Get free key from https://openweathermap.org/api
WEATHER_API_KEY=your-openweather-api-key-here
WEATHER_API_URL=https://api.openweathermap.org/data/2.5
```

**Note**: Weather features are optional. The app works without this, but weather correlation insights won't be available.

### Optional (for Photo Uploads - Future Feature)

```env
# AWS S3 for photo storage (not implemented yet)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
AWS_S3_BUCKET=
```

## Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Quick Setup

### Backend `.env` file

```bash
cd backend
cat > .env << EOF
DATABASE_URL=postgresql://curliq:curliq_dev_password@localhost:5432/curliq
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
WEATHER_API_KEY=
WEATHER_API_URL=https://api.openweathermap.org/data/2.5
CORS_ORIGINS=["http://localhost:3000"]
EOF
```

### Frontend `.env.local` file

```bash
cd frontend
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

## Getting a Weather API Key (Optional)

1. Go to https://openweathermap.org/api
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add it to `backend/.env` as `WEATHER_API_KEY=your-key-here`

The free tier allows 60 calls/minute and 1,000,000 calls/month, which is plenty for development.

## Security Notes

- **SECRET_KEY**: Generate a strong random string for production
  - You can generate one with: `python3 -c 'import secrets; print(secrets.token_urlsafe(32))'`
- **Never commit `.env` files** to git (they're in `.gitignore`)
- Use different keys for development and production

## Default Values

If you don't set these variables, the app uses these defaults:
- `DATABASE_URL`: `postgresql://curliq:curliq_dev_password@localhost:5432/curliq`
- `REDIS_URL`: `redis://localhost:6379/0`
- `SECRET_KEY`: `your-secret-key-change-in-production` (⚠️ Change this!)
- `WEATHER_API_KEY`: Empty string (weather features disabled)
- `CORS_ORIGINS`: `["http://localhost:3000", "http://localhost:3001"]`

## Minimum Setup for Development

For basic development, you only need:

**Backend `.env`:**
```env
SECRET_KEY=dev-secret-key-change-in-production
```

**Frontend `.env.local`:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Everything else will use defaults that work with `docker-compose up -d`.
