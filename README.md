# Expense Tracker

A personal expense tracking web application built as an engineering assessment. Track spending by category, set monthly budgets, and view spending-vs-budget summaries.

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+

### Backend
```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
flask --app app run --debug        # API on http://localhost:5000
```

### Backend (Windows PowerShell)
```powershell
cd backend
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
copy .env.example .env
flask --app app run --debug
```

### Frontend
```bash
cd frontend
npm install
npm run dev                        # SPA on http://localhost:5173 (proxies /api → :5000)
```

### Tests
```bash
# Backend (78 tests, 90%+ coverage)
cd backend && pytest

# Frontend (21 tests)
cd frontend && npm test
```

---

## Features

- **Categories** — Create named categories; backend assigns a random color automatically
- **Expenses** — Log expenses with amount, description, date, and notes; paginated list with year/month/category filters
- **Budgets** — Set a monthly spending limit per category; one budget per category/month enforced
- **Dashboard** — Summary cards (spent / budgeted / remaining), per-category budget progress bars, 6-month spending trend chart
- **Confirmation dialogs** — All destructive deletes require explicit confirmation
- **Toast notifications** — Success and error feedback on every create/update/delete action
- **Sidebar navigation** — Persistent sidebar with icon links to all sections

---

## Architecture

### Module-Based Backend

```
Request → Blueprint (HTTP) → Service (Business Logic) → Repository (Data Access) → SQLAlchemy Model → SQLite
```

Code is co-located by domain, not by layer type:

```
app/
├── application/          shared foundation
│   ├── base_model.py     id/created_at/updated_at mixin for all models
│   ├── base_repository.py  generic find_by_id/find_all/save/delete
│   └── errors.py         AppError hierarchy
└── modules/
    ├── category/         {model, repository, schema, service, types, errors, rest_api/}
    ├── expense/          same
    ├── budget/           same
    └── dashboard/        service + rest_api/ (no model of its own)
```

Each module layer has a single responsibility:
- **`rest_api/`** — parse request, construct params, call service, serialize response, return HTTP status
- **`*_service.py`** — ALL business rules; calls repository methods, never `db.session` directly
- **`*_repository.py`** — ALL database access; wraps SQLAlchemy queries
- **`*_schema.py`** — Marshmallow: input validation on load, serialization on dump
- **`*_model.py`** — SQLAlchemy table definitions and relationships only
- **`types.py`** — `@dataclass` param objects passed from blueprint to service
- **`errors.py`** — domain-specific error subclasses (e.g. `CategoryNotFoundError`)

### Frontend State Layers

```
React Query (server state) ←→ Zustand (UI state: modals, filters)
```

- **`src/api/`** — Pure HTTP functions; no state
- **`src/hooks/`** — React Query wrappers; own all cache invalidation
- **`src/store/ui.ts`** — Modal open/close, active month selector (UI only)
- **`src/components/`** — Receive props, display data, fire callbacks

---

## Database Schema

```sql
categories (id, name UNIQUE, color, icon, created_at, updated_at)
expenses   (id, category_id FK→categories, amount NUMERIC(10,2), description, date, notes, ...)
budgets    (id, category_id FK→categories, year, month, amount NUMERIC(10,2), ...)
           UNIQUE (category_id, year, month)
```

`ON DELETE RESTRICT` on `expenses.category_id` — prevents orphaned expenses.
`ON DELETE CASCADE` on `budgets.category_id` — budgets are configuration, not data.

---

## Business Rules

Enforced exclusively in the service layer. Passing schema validation does not mean a request is valid.

| Rule | Behavior |
|------|----------|
| BR-CAT-01 | Category name unique (case-insensitive) |
| BR-CAT-02 | Cannot delete category with expenses → 409 |
| BR-CAT-03 | Color must be a 6-digit hex → 422 |
| BR-EXP-01 | Amount > 0 → 422 |
| BR-EXP-02 | Date not in future → 422 |
| BR-EXP-03 | Category must exist → 404 |
| BR-EXP-04 | Description non-blank → 422 |
| BR-EXP-05 | Soft warning if over budget (does not block creation) |
| BR-BUD-01 | Budget amount > 0 → 422 |
| BR-BUD-02 | Month 1–12 (schema) → 400 |
| BR-BUD-03 | Year 2000–2100 (schema) → 400 |
| BR-BUD-04 | One budget per category/month → 409 |

---

## API

All endpoints under `/api`. Standard JSON envelope:

```json
{ "data": <payload> }          // success
{ "error": { "code", "message", "details" } }  // failure
```

| Resource | Endpoints |
|----------|-----------|
| Categories | `GET/POST /api/categories`, `GET/PUT/DELETE /api/categories/:id` |
| Expenses | `GET/POST /api/expenses?page&per_page&category_id&year&month`, `GET/PUT/DELETE /api/expenses/:id` |
| Budgets | `GET/POST /api/budgets?year&month&category_id`, `GET/PUT/DELETE /api/budgets/:id` |
| Dashboard | `GET /api/dashboard/summary?year&month`, `GET /api/dashboard/trends?months` |

---

## Key Technical Decisions

| Decision | Choice | Reasoning |
|----------|--------|-----------|
| Database | SQLite | Zero setup; sufficient for assessment scope. Swap URL in `.env` for Postgres |
| Amounts | `Numeric(10,2)` | Float is unsuitable for money; `Decimal` avoids precision errors |
| Validation | Marshmallow (BE) + Zod (FE) | Schema-first; TypeScript types derived from schemas via `z.infer<>` |
| Server state | React Query | Eliminates manual loading/error state; cache invalidation is explicit |
| UI state | Zustand | Minimal; modal open/close and active month only |
| Forms | react-hook-form + zodResolver | Uncontrolled inputs = minimal re-renders; reuses Zod schemas |
| Error hierarchy | Custom `AppError` subclasses | Keeps route handlers thin; error → HTTP status mapping is centralized |
| Logging | `python-json-logger` | Structured JSON output; grep-able in any log aggregator |
| API mocking | MSW | Network-level interception; tests are realistic, no module mocking |
| Test naming | `test_BR_EXP_02_future_date_rejected` | Each business rule has an explicit test |
| Toasts | `sonner` | Zero-config, rich colors, works with React 18 |
| Confirm dialogs | Custom `ConfirmDialog` wrapping `Modal` | No extra overlay logic; reuses existing backdrop/blur |

---

## Trade-offs and Weaknesses

**Authentication:** There is no auth. Every endpoint is public. Adding auth would require a users table, JWT middleware in the blueprints layer, and user-scoped queries in services. The service layer is already isolated, so this change would not cascade widely.

**Migrations:** `db.create_all()` is used for schema creation. This is suitable for greenfield development but not for production schema evolution. Adding Flask-Migrate would require one `flask db init` command; the models are already compatible.

**SQLite concurrency:** SQLite has write contention under concurrent load. Replacing `DATABASE_URL` with a PostgreSQL URL in `.env` is the only required change; no code modifications needed.

**Amount storage:** Amounts are stored as `NUMERIC(10,2)` and serialized as strings (e.g. `"45.99"`). The frontend parses these with `parseFloat()`. For a production app, a dedicated money library (e.g. `dinero.js`) would be safer.

**Frontend error messages:** Validation errors from the backend's `details` field are not currently surfaced field-by-field in forms. The error envelope is displayed at the top of the form, which covers all server errors.

---

## Extension Approach

To add a new feature (e.g. recurring expenses):

1. **Model** — add `recurrence` column to `app/modules/expense/expense_model.py` (nullable)
2. **Schema** — add optional `recurrence` field to `ExpenseCreateSchema` in `expense_schema.py`
3. **Types** — add `recurrence` to `ExpenseCreateParams` in `types.py`
4. **Repository** — add any new queries to `expense_repository.py` if needed
5. **Service** — add recurrence business rules in `expense_service.py`
6. **Blueprint** — no changes needed (existing CRUD passes through)
7. **Frontend types** — add field to `expenseCreateSchema` in `src/types/expense.ts`
8. **Frontend form** — add field to `ExpenseForm.tsx`
9. **Tests** — add `test_BR_EXP_<N>_*` tests in `tests/modules/expense/test_expense_service.py`

The module architecture keeps all expense-related code in one folder. Only the vertical slice for that feature needs updating.

---

## AI Usage

This project was built using Claude Code (Sonnet 4.6) as the primary implementation assistant.

**How AI was used:**
- Generating the full project structure, all models, schemas, services, blueprints, and tests from the plan
- Writing MSW mock handlers and Vitest component tests
- Fixing test failures (logging key collision, Decimal formatting in test assertions, SQLAlchemy session isolation in factory-boy)
- Iterative UI/UX enhancements: indigo navbar → sidebar layout, card polish, striped tables
- Enterprise upgrade: `sonner` toasts, `ConfirmDialog`, `Sidebar` component, polished Input/Select/Button primitives

**How AI was constrained (see `CLAUDE.md`):**
- `CLAUDE.md` specifies exact layer responsibilities — AI cannot move business logic into blueprints
- Business rule naming convention (`BR-EXP-01`) ensures each rule has a test and is traceable
- Explicit type rules (`Numeric` not `Float`, Zod schemas for all API responses) prevent common mistakes
- Test naming convention enforces coverage of each business rule

**AI output verification:**
- All 78 backend tests passed before moving to frontend
- All 21 frontend tests passed before finalizing
- TypeScript strict mode caught type errors in generated code
- Coverage reports confirmed service layer is fully exercised
- Every destructive change reviewed before execution; no `--no-verify` bypasses
