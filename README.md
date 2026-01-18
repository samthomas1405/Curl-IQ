# CurlLabs - Curly Hair Routine Optimizer

A full-stack app that helps people with curly hair track routines, products, weather, and results, then turns that data into personalized recommendations and explainable "what works for me" insights.

## 🚀 Quick Start

See [SETUP.md](./SETUP.md) for detailed setup instructions.

```bash
# Start database services
docker-compose up -d

# Backend (in one terminal)
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (in another terminal)
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` to see the app!

## 📋 Project Status

See [PROJECT_STATUS.md](./PROJECT_STATUS.md) for detailed status of all features.

## Project Overview

**Target Users**: Curly/coily hair (2A to 4C), beginners to experienced users experimenting with products and routines.

## Architecture Recommendations

### Tech Stack Refinements

**Frontend**
- ✅ Next.js 14+ (App Router) with TypeScript
- ✅ Tailwind CSS + shadcn/ui
- ✅ Recharts for visualizations
- ✅ React Hook Form + Zod
- 💡 **Add**: TanStack Query for server state management
- 💡 **Add**: Zustand or Jotai for client state (simpler than Redux)

**Backend**
- ✅ FastAPI (excellent choice for ML/data work)
- ✅ JWT auth (access + refresh tokens)
- 💡 **Consider**: tRPC for type-safe API (if you want tighter frontend-backend coupling)
- ✅ Celery + Redis for background jobs
- 💡 **Add**: FastAPI BackgroundTasks for lightweight async work (weather fetching)

**Database**
- ✅ PostgreSQL
- ✅ SQLAlchemy + Alembic (standard for FastAPI)
- 💡 **Add**: pgvector extension for routine similarity search (embeddings)
- 💡 **Consider**: TimescaleDB extension if you want time-series optimizations for trend analysis

**Storage**
- ✅ S3-compatible (or Supabase Storage)
- 💡 **Add**: Image optimization pipeline (Sharp/ImageMagick) before upload

**ML/AI**
- ✅ pandas + scikit-learn
- 💡 **Add**: Feature engineering pipeline (weather normalization, product encoding)
- 💡 **Consider**: LightGBM over Random Forest (faster, often better)
- 💡 **Add**: Model versioning (MLflow or simple S3-based versioning)

### Architecture Improvements

1. **API Design**
   - Use OpenAPI/Swagger (FastAPI auto-generates this)
   - Version your API (`/api/v1/`)
   - Implement rate limiting (slowapi or FastAPI-limiter)

2. **Caching Strategy**
   - Redis for:
     - Weather data (cache for 1-2 hours)
     - Popular routines (community section)
     - User recommendations (refresh daily)
   - Consider CDN for static assets and images

3. **Background Jobs**
   - Weather fetching: Daily cron for all users (batch)
   - ML model retraining: Weekly, triggered by Celery beat
   - Insight generation: On-demand or nightly batch

4. **Data Pipeline**
   ```
   User Log → Validation → Store in DB → Trigger Insight Recalc → Update Recommendations
   ```

## Feature Recommendations

### High Priority (MVP)
1. ✅ Accounts + Hair Profile
2. ✅ Product Library (basic CRUD)
3. ✅ Routine Builder (templates)
4. ✅ Routine Logging (core feature)
5. ✅ Outcome Tracking (ratings)
6. ✅ Weather Integration (automatic)
7. ✅ Basic Dashboard (trends, best routines)

### Medium Priority (Post-MVP)
8. ✅ Personal Recommendations
9. ✅ Insight Engine (data-first)
10. ⚠️ **Refine**: Predictive Model (start simple - linear regression, add complexity later)

### Lower Priority (V2)
11. Community Sharing
12. Collaborative Filtering
13. GenAI Explanations (nice-to-have, but can be manual templates initially)

### Feature Additions to Consider

1. **Photo Analysis** (Future)
   - Use computer vision to auto-detect frizz/definition from photos
   - Could use a pre-trained model or fine-tune on user-labeled images

2. **Routine Templates Library**
   - Pre-built routines for common scenarios (wash day, refresh, deep condition)
   - Curated by hair type

3. **Product Ingredient Analysis**
   - Ingredient parsing and flagging (sulfates, silicones, etc.)
   - Ingredient-based recommendations

4. **Export/Import**
   - Export logs as CSV/JSON
   - Import from other apps

5. **Mobile App** (Future)
   - React Native or PWA first
   - Quick logging on the go

## Data Model Considerations

### Core Tables

**Users**
- id, email, password_hash, created_at, updated_at
- hair_profile (JSONB or separate table)

**Products**
- id, user_id (nullable for community), brand, name, type, ingredients (array), notes
- usage_count, success_rate (computed)

**Routines**
- id, user_id, name, is_template, is_public
- steps (JSONB array: {step_type, product_id, order, notes})
- method_tags (array), drying_method

**Routine Logs**
- id, user_id, routine_id, date, time
- products_used (JSONB: step → product mapping)
- wash_day (boolean), styling_method, drying_method
- time_spent, notes, photo_urls (array)

**Outcomes**
- id, routine_log_id, rated_at (timestamp)
- frizz, definition, softness, hold_hours
- overall_score (computed), notes

**Weather Data**
- id, user_id, date, location
- humidity, dew_point, temperature, wind_speed
- (Consider separate table or JSONB in logs)

**Insights** (computed/cached)
- id, user_id, insight_type, statement, confidence, sample_size
- created_at, expires_at

### Indexing Strategy
- Index on `routine_logs(user_id, date)` for dashboard queries
- Index on `outcomes(routine_log_id)` for joins
- Index on `weather_data(user_id, date)`
- Consider partial indexes for active users

## AI/ML Recommendations

### Insight Engine
- **Minimum sample size**: 10 logs per group (good threshold)
- **Statistical significance**: Use p-values or confidence intervals
- **Avoid overfitting**: Don't create insights from <5 data points
- **Caching**: Pre-compute insights nightly, invalidate on new logs

### Predictive Model
- **Start simple**: Linear regression with feature engineering
- **Features**:
  - Hair profile (one-hot encoded)
  - Weather (normalized: humidity, dew_point, temp)
  - Routine attributes (product types, method, drying)
  - Historical averages (user's baseline)
- **Evaluation**: Cross-validation, track MAE/RMSE
- **Retraining**: Weekly or when user has 10+ new logs

### Recommendation System
1. **Content-based** (easier to start)
   - Match routines by hair profile similarity
   - Weight by user's historical preferences
2. **Collaborative filtering** (add later)
   - Requires sufficient user base
   - Use matrix factorization or k-nearest neighbors
3. **Hybrid approach** (best)
   - Combine both methods
   - Fallback to content-based if not enough similar users

### GenAI Explanations
- **Use responsibly**: Only explain computed insights, never invent data
- **Prompt engineering**: 
  - "Explain why [insight] based on [data points]"
  - Include confidence levels and sample sizes
- **Cost consideration**: Cache explanations, use cheaper models (Claude Haiku, GPT-3.5-turbo)

## Security & Privacy

1. **Data Privacy**
   - Photos: Private by default, opt-in for sharing
   - Personal routines: Private by default
   - Anonymize data used for collaborative filtering

2. **Security**
   - Rate limiting on auth endpoints
   - Input validation (Zod on frontend, Pydantic on backend)
   - SQL injection prevention (use ORM)
   - XSS prevention (sanitize user inputs)

3. **Compliance**
   - GDPR considerations (data export, deletion)
   - Terms of service for community features

## Performance Optimizations

1. **Database**
   - Use connection pooling (SQLAlchemy pool)
   - Read replicas for dashboard queries (if scale requires)
   - Materialized views for aggregated insights

2. **API**
   - Pagination for logs/routines
   - Field selection (GraphQL-style or query params)
   - Compression (gzip)

3. **Frontend**
   - Code splitting (Next.js automatic)
   - Image optimization (Next.js Image component)
   - Lazy loading for charts

## MVP Scope (Week 1-2)

### Week 1: Core Foundation
- [ ] Auth (email/password + JWT)
- [ ] Hair profile creation
- [ ] Product CRUD
- [ ] Basic routine builder
- [ ] Routine logging (simple form)
- [ ] Outcome tracking (ratings)
- [ ] Weather API integration (basic)

### Week 2: Insights & Dashboard
- [ ] Dashboard with basic charts (Recharts)
- [ ] Simple insights ("Best routine", "Best products")
- [ ] Weather correlation (basic: "High humidity = higher frizz")
- [ ] Personal recommendations (content-based, simple)
- [ ] Basic predictive model (linear regression)

### Post-MVP
- Community features
- Advanced ML models
- GenAI explanations
- Photo upload/analysis

## Deployment Strategy

### Recommended Setup
- **Frontend**: Vercel (Next.js native)
- **Backend**: Render or Fly.io (FastAPI)
- **Database**: Supabase (PostgreSQL + Storage) or Neon (serverless Postgres)
- **Redis**: Upstash (serverless Redis)
- **Background Jobs**: Render Cron or Fly.io Machines

### CI/CD
- GitHub Actions:
  - Lint + type check
  - Run tests
  - Deploy on merge to main

### Monitoring
- **Errors**: Sentry (free tier)
- **Logs**: Structured logging (JSON) → CloudWatch or Logtail
- **Metrics**: Basic health endpoints + Uptime monitoring

## What to Build Next (Post-Interview)

1. **Mobile App** (React Native or PWA)
2. **Advanced Analytics**
   - A/B testing framework for recommendations
   - Cohort analysis
3. **Social Features**
   - Follow other users
   - Routine reviews/ratings
4. **Product Database**
   - Community-contributed product database
   - Ingredient analysis API integration
5. **Subscription Tiers**
   - Free: Basic tracking
   - Pro: Advanced insights, unlimited photos, export

## Questions to Consider

1. **Monetization**: Freemium? One-time purchase? Subscription?
2. **Community Moderation**: How to handle bad routines? User reports + admin review?
3. **Data Retention**: How long to keep logs? Allow deletion?
4. **Offline Support**: PWA with service workers for offline logging?

## Final Recommendations

### Strengths of Your Plan
✅ Clear target users
✅ Data-first AI approach (responsible)
✅ Modern, deployable tech stack
✅ Comprehensive feature set

### Suggested Changes
1. **Start smaller**: Focus on MVP (Week 1-2) first, add complexity later
2. **Simplify ML initially**: Linear regression → Random Forest → Gradient Boosting (progressive complexity)
3. **Defer GenAI**: Manual templates work fine initially, add LLM later
4. **Weather batching**: Don't fetch per-user, batch by location
5. **Add analytics**: Track which insights users engage with most

### Risk Mitigation
- **Cold start problem**: Pre-seed with example routines for each hair type
- **Low data**: Show "need more data" messages until thresholds met
- **Model accuracy**: Always show confidence intervals, not just predictions

---

## Getting Started

```bash
# Frontend
cd frontend
npm install
npm run dev

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## License

[Your License Here]
