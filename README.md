# 📱 MobiCompare — Full Stack Setup Guide

India's best mobile price comparison platform.  
**Stack:** FastAPI · MongoDB · Vanilla JS frontend · Python 3.12

---

## 📁 Project Structure

```
mobicompare/
├── backend/               ← FastAPI Python API
│   ├── main.py            ← App entry point
│   ├── config.py          ← Settings / env vars
│   ├── database.py        ← MongoDB connection
│   ├── models.py          ← Pydantic schemas
│   ├── auth_utils.py      ← JWT + bcrypt helpers
│   ├── routes/
│   │   ├── mobiles.py     ← GET/POST/PUT/DELETE phones
│   │   ├── search.py      ← Full-text search + autocomplete
│   │   ├── compare.py     ← Side-by-side comparison
│   │   ├── filters.py     ← Dynamic filter options
│   │   ├── prices.py      ← Seller prices + price alerts
│   │   ├── auth.py        ← Register / login / wishlist
│   │   └── admin.py       ← Admin dashboard stats
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   └── index.html         ← Full frontend (single file)
├── database/
│   └── seed.py            ← Seed 31 phones + all seller prices
├── docker-compose.yml
└── README.md              ← This file
```

---

## 🚀 Option A — Run Locally (Recommended for Development)

### Prerequisites
- Python 3.10+ → https://python.org/downloads
- MongoDB 6+ → https://www.mongodb.com/try/download/community
- Git (optional)

---

### Step 1 — Install & Start MongoDB

**Windows:**
1. Download MongoDB Community from https://www.mongodb.com/try/download/community
2. Run the installer, choose "Complete"
3. MongoDB starts automatically as a Windows Service
4. Verify: open Command Prompt → `mongosh` → you should see a prompt

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

Verify MongoDB is running:
```bash
mongosh --eval "db.adminCommand('ping')"
# Should print: { ok: 1 }
```

---

### Step 2 — Set Up Python Environment

Open a terminal in the `mobicompare/` folder:

```bash
# Create virtual environment
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

---

### Step 3 — Configure Environment

```bash
cd backend
cp .env.example .env
```

Open `.env` in any text editor. The defaults work for local development:
```
MONGO_URI=mongodb://localhost:27017
MONGO_DB=mobicompare
SECRET_KEY=change-this-in-production-use-openssl-rand-hex-32
DEBUG=True
```

> ⚠️ **For production** — generate a secure key:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```
> Paste the output as your SECRET_KEY.

---

### Step 4 — Seed the Database

This inserts all 31 phones + seller prices + admin account:

```bash
# From the mobicompare/ root folder (with venv activated):
cd database
python seed.py
```

Expected output:
```
🗑️  Cleared existing mobiles & prices collections
  ✅ Samsung Galaxy S25 Ultra — ₹1,33,999 — 5 sellers
  ✅ Samsung Galaxy S25+ — ₹99,999 — 5 sellers
  ... (31 phones total)
👤 Admin user created: admin@mobicompare.in / admin1234
📊 Indexes created
🎉 Seed complete! 31 phones, 155 price entries inserted.
```

---

### Step 5 — Start the Backend

```bash
# From the mobicompare/ root folder (with venv activated):
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
✅ MongoDB connected
```

---

### Step 6 — Open the Website

The backend also serves the frontend automatically.

Open your browser:
```
http://localhost:8000
```

🎉 **Your MobiCompare website is live!**

---

### Bonus — API Documentation

FastAPI auto-generates interactive docs:
```
http://localhost:8000/docs        ← Swagger UI (test all endpoints)
http://localhost:8000/redoc       ← ReDoc (readable API docs)
http://localhost:8000/api/health  ← Health check
```

---

## 🐳 Option B — Run with Docker (One Command)

### Prerequisites
- Docker Desktop → https://www.docker.com/products/docker-desktop

### Steps

```bash
# 1. Start everything (MongoDB + API + Frontend)
docker-compose up --build

# 2. Seed the database (run in a NEW terminal while containers are running)
docker exec -it mobicompare_api python ../database/seed.py

# 3. Open browser
# http://localhost:8000
```

To stop:
```bash
docker-compose down
```

To stop and delete all data:
```bash
docker-compose down -v
```

---

## 🔑 Admin Access

| Field    | Value                       |
|----------|-----------------------------|
| Email    | admin@mobicompare.in        |
| Password | admin1234                   |

The admin account is created by `seed.py`. Admin endpoints are protected by JWT and require the `is_admin: true` flag.

To get an admin token:
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@mobicompare.in","password":"admin1234"}'
```

Use the returned `access_token` as a Bearer token for admin API calls.

---

## 📡 API Endpoints Reference

| Method | Endpoint                          | Description                        |
|--------|-----------------------------------|------------------------------------|
| GET    | `/api/mobiles`                    | List all phones (paginated+filtered)|
| GET    | `/api/mobiles/trending`           | Trending phones (filterable)       |
| GET    | `/api/mobiles/latest`             | Newest launches                    |
| GET    | `/api/mobiles/budget`             | Budget phones (≤₹20k)              |
| GET    | `/api/mobiles/brands`             | Brand list with phone counts       |
| GET    | `/api/mobiles/ticker`             | Price ticker data                  |
| GET    | `/api/mobiles/{id}`               | Full phone detail + sellers        |
| POST   | `/api/mobiles` *(admin)*          | Add a new phone                    |
| PUT    | `/api/mobiles/{id}` *(admin)*     | Update a phone                     |
| DELETE | `/api/mobiles/{id}` *(admin)*     | Delete a phone                     |
| GET    | `/api/search?q=samsung`           | Full-text search                   |
| GET    | `/api/search/suggestions?q=ip`    | Autocomplete suggestions           |
| POST   | `/api/compare`                    | Compare 2–3 phones                 |
| GET    | `/api/filters`                    | Dynamic filter options from DB     |
| GET    | `/api/prices/{mobile_id}`         | All seller prices for a phone      |
| POST   | `/api/prices/alert`               | Set a price drop alert             |
| GET    | `/api/prices/alerts/{email}`      | Get alerts for an email            |
| POST   | `/api/auth/register`              | Create account                     |
| POST   | `/api/auth/login`                 | Login → JWT token                  |
| GET    | `/api/auth/me`                    | Current user info                  |
| POST   | `/api/auth/wishlist/{mobile_id}`  | Toggle wishlist                    |
| GET    | `/api/auth/wishlist`              | Get user wishlist                  |
| GET    | `/api/admin/stats` *(admin)*      | Dashboard statistics               |
| POST   | `/api/admin/trigger-alerts` *(admin)* | Check & trigger price alerts  |
| GET    | `/api/health`                     | API + DB health check              |

---

## ❓ Troubleshooting

**"MongoDB connection refused"**
→ Make sure MongoDB is running: `mongosh` should open a shell.
→ Check it's on port 27017: `netstat -an | grep 27017`

**"ModuleNotFoundError"**
→ Make sure your virtual environment is activated: `source venv/bin/activate` (or `venv\Scripts\activate` on Windows)
→ Run `pip install -r backend/requirements.txt` again

**"Port 8000 already in use"**
→ Change the port: `uvicorn main:app --reload --port 8001`
→ Then open `http://localhost:8001`

**Seed script says "already seeded"**
→ The seed drops & recreates collections each run — safe to run multiple times.

**Frontend shows no phones**
→ Check the browser console (F12) for errors
→ Make sure the backend is running at `http://localhost:8000`
→ Run the seed script if you haven't

---

## 🌐 Deploying to Production

Quick options:

| Platform       | Steps                                                         |
|----------------|---------------------------------------------------------------|
| **Railway**    | Connect GitHub repo → set env vars → deploy (free tier)      |
| **Render**     | New Web Service → Python → start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **DigitalOcean** | Use Docker Compose on a $6/mo Droplet                      |
| **MongoDB Atlas** | Use free M0 cluster → replace MONGO_URI with Atlas string |

For production, always:
- Change `SECRET_KEY` to a random 64-char hex string
- Set `DEBUG=False`
- Use MongoDB Atlas or a secured MongoDB instance
- Restrict CORS `allow_origins` to your domain

---

*Built with ❤️ — MobiCompare v2.0*
