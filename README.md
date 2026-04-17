# Foreign Trade Decision System

## Quick Run

### 1) Install dependencies

```bash
poetry install
```

### 2) Configure API key

Create and edit `.env` in project root:

```bash
cp .env.example .env
```

Set at least one model provider key, for example:

```bash
OPENAI_API_KEY=your-openai-api-key
```

### 3) Run from CLI

```bash
poetry run python -m src.main --question "我要不要做LED灯出口"
```

Optional:

```bash
poetry run python -m src.main --question "我要不要做手机壳出口" --ollama
poetry run python -m src.main --question "我要不要做工业设备出口" --analysts market,customer,product,supply,profit,data_analysis,case_analysis
```

## Run Web App

```bash
cd app
run.bat
```

Or manual start:

```bash
cd app/backend
poetry run uvicorn main:app --reload
```

```bash
cd app/frontend
npm install
npm run dev
```

Access:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- API docs: `http://localhost:8000/docs`
