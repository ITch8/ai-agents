# Web Application

## Quick Run

From project root:

```bash
cd app
run.bat
```

## Manual Run

### Backend

```bash
cd app/backend
poetry run uvicorn main:app --reload
```

### Frontend

```bash
cd app/frontend
npm install
npm run dev
```

## Access

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
