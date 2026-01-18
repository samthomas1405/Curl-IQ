# CurlLabs Setup Instructions

## Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- Docker and Docker Compose (for PostgreSQL and Redis)
- OpenWeatherMap API key (optional, for weather features)

## Quick Start

### 1. Start Database Services

```bash
docker-compose up -d
```

This starts PostgreSQL and Redis in the background.

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp ../.env.example .env
# Edit .env and add your WEATHER_API_KEY if you have one

# Run database migrations (creates tables)
# The app will auto-create tables on first run, or use Alembic:
# alembic upgrade head

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

### 3. Frontend Setup

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

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://curliq:curliq_dev_password@localhost:5432/curliq
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
WEATHER_API_KEY=your-openweather-api-key
WEATHER_API_URL=https://api.openweathermap.org/data/2.5
CORS_ORIGINS=["http://localhost:3000"]
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Database Schema

The app uses the following main tables:
- `users` - User accounts and hair profiles
- `products` - Hair care products
- `routines` - Routine templates
- `routine_logs` - Logged routine sessions
- `outcomes` - Outcome ratings (frizz, definition, etc.)
- `weather_data` - Weather data for correlation

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update user
- `PUT /api/v1/users/me/profile` - Update hair profile

### Products
- `GET /api/v1/products` - List products
- `POST /api/v1/products` - Create product
- `GET /api/v1/products/{id}` - Get product
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product

### Routines
- `GET /api/v1/routines` - List routines
- `POST /api/v1/routines` - Create routine
- `GET /api/v1/routines/{id}` - Get routine
- `PUT /api/v1/routines/{id}` - Update routine
- `DELETE /api/v1/routines/{id}` - Delete routine

### Routine Logs
- `GET /api/v1/routine-logs` - List logs
- `POST /api/v1/routine-logs` - Create log
- `GET /api/v1/routine-logs/{id}` - Get log
- `PUT /api/v1/routine-logs/{id}` - Update log
- `DELETE /api/v1/routine-logs/{id}` - Delete log

### Outcomes
- `GET /api/v1/outcomes` - List outcomes
- `POST /api/v1/outcomes` - Create outcome
- `GET /api/v1/outcomes/{id}` - Get outcome
- `PUT /api/v1/outcomes/{id}` - Update outcome
- `DELETE /api/v1/outcomes/{id}` - Delete outcome

### Weather
- `GET /api/v1/weather` - List weather data
- `POST /api/v1/weather/fetch` - Fetch and save weather

### Dashboard
- `GET /api/v1/dashboard/stats` - Get dashboard statistics
- `GET /api/v1/dashboard/trends` - Get trends over time
- `GET /api/v1/dashboard/insights` - Get insights

## Testing the Setup

1. Start all services (database, backend, frontend)
2. Open `http://localhost:3000`
3. Register a new account
4. You'll be redirected to the dashboard
5. Try creating a product or routine

## Troubleshooting

### Database Connection Issues
- Ensure Docker is running
- Check that PostgreSQL is up: `docker ps`
- Verify DATABASE_URL in .env matches docker-compose.yml

### Backend Won't Start
- Check Python version: `python3 --version` (need 3.10+)
- Ensure virtual environment is activated
- Check if port 8000 is already in use

### Frontend Won't Connect to Backend
- Verify NEXT_PUBLIC_API_URL in .env.local
- Check CORS_ORIGINS in backend .env includes frontend URL
- Ensure backend is running on port 8000

### Weather API Not Working
- Weather features are optional
- Get a free API key from https://openweathermap.org/api
- Add it to backend .env as WEATHER_API_KEY

## Next Steps

- Add more products and routines
- Log your first routine
- Rate outcomes to see insights
- Check the dashboard for trends

## Development Notes

- Backend auto-reloads on file changes (--reload flag)
- Frontend hot-reloads automatically
- Database tables are created automatically on first run
- Use FastAPI docs at `/docs` for API testing
