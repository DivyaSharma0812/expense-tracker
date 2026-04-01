# CLAUDE.md — AI Coding Standards for expense-tracker

This file constrains AI-generated code. Follow every rule here. Do not deviate without explicit user instruction.

---

## Project Overview

**Product:** Personal Expense Tracker
**Backend:** Python 3.11+, Flask 3, SQLAlchemy 2, Marshmallow
**Frontend:** React 18, TypeScript (strict), Vite, React Query, Zod
**Database:** SQLite (via SQLAlchemy)

---

## Backend Architecture Rules (MUST follow)

### Module Structure

Code is organized by domain. Each domain lives under `app/modules/<domain>/`:

```
app/modules/<domain>/
  <domain>_model.py       → DB columns, relationships, __repr__ only
  <domain>_repository.py  → ALL db.session calls. No business logic.
  <domain>_schema.py      → Input validation (load) and output serialization (dump)
  <domain>_service.py     → ALL business logic, ALL business rules
  types.py                → @dataclass param objects (e.g. CategoryCreateParams)
  errors.py               → Domain-specific AppError subclasses
  rest_api/
    <domain>_blueprint.py → HTTP only: parse, construct params, call service, return status

app/application/
  base_model.py           → Shared id/created_at/updated_at mixin
  base_repository.py      → Generic find_by_id/find_all/save/delete
  errors.py               → AppError hierarchy (NotFoundError, ConflictError, etc.)
```

**Rule 1:** Business logic lives ONLY in `<domain>_service.py`. Route handlers call services and return responses. Never put `if/else` domain logic in route handlers.

**Rule 2:** Route handlers do exactly five things: parse the request body → construct a params dataclass → call the service → serialize the result → return the HTTP response. Nothing more.

**Rule 3:** Models define columns, relationships, and `__repr__`. They contain no methods with business logic.

**Rule 4:** Schemas define: what fields are accepted on input (load) and what is returned on output (dump). They contain no business logic.

**Rule 4a:** Repositories contain ALL `db.session` calls. Services must never call `db.session` directly, except for the one special case in `ExpenseService.create_expense` where a `flush()` is needed mid-transaction before the budget warning check.

### Error Handling

**Rule 5:** Services raise domain-specific error subclasses only. Never raise plain `Exception`. Each module's `errors.py` defines domain errors that extend the base classes in `app/application/errors.py`:
- `NotFoundError` → 404 (e.g. `CategoryNotFoundError`)
- `ConflictError` → 409 (e.g. `DuplicateBudgetError`)
- `ValidationError` → 400
- `BusinessRuleError` → 422 (e.g. `ExpenseAmountError`)

**Rule 6:** Route handlers do NOT catch errors. The global error handler in `create_app()` catches all `AppError` subclasses and formats them into the JSON envelope.

**Rule 7:** Log 5xx errors with `logger.exception()` (captures stack trace). Log 4xx errors with `logger.warning()`.

**Rule 8:** Never use `"name"` as a key in `extra={}` passed to the logger — it is a reserved `LogRecord` field. Use `category_name`, `resource_name`, etc.

### Data Types

**Rule 9:** Use `Numeric(10, 2)` for ALL monetary amounts. Never use `Float`. Float causes precision errors in financial calculations.

**Rule 10:** Always use `db.session` from Flask-SQLAlchemy via repository methods. Never instantiate raw SQLAlchemy sessions.

### Naming

- Service classes: `<Resource>Service` (e.g. `CategoryService`)
- Service methods: `get_<resource>`, `create_<resource>`, `update_<resource>`, `delete_<resource>`
- Repository classes: `<Resource>Repository` (e.g. `CategoryRepository`)
- Schema classes: `<Resource>Schema` (output), `<Resource>CreateSchema` (POST input), `<Resource>UpdateSchema` (PUT input)
- Params dataclasses: `<Resource>CreateParams`, `<Resource>UpdateParams`
- Domain error classes: `<Resource><Problem>Error` (e.g. `CategoryNotFoundError`, `BudgetAmountError`)
- Blueprint files: `<domain>_blueprint.py` inside `rest_api/`

---

## Business Rules (backend)

All rules enforced in services only. Never enforce in blueprints or models.

| Code | Domain | Rule |
|------|--------|------|
| BR-CAT-01 | Category | Name must be unique (case-insensitive) |
| BR-CAT-02 | Category | Cannot delete if it has expenses (409) |
| BR-CAT-03 | Category | Color must match `#[0-9a-fA-F]{6}` |
| BR-EXP-01 | Expense | Amount must be > 0 |
| BR-EXP-02 | Expense | Date must not be in the future |
| BR-EXP-03 | Expense | category_id must reference an existing category |
| BR-EXP-04 | Expense | Description must not be blank after strip |
| BR-EXP-05 | Expense | Soft warning if spending exceeds budget (do NOT block) |
| BR-BUD-01 | Budget | Amount must be > 0 |
| BR-BUD-02 | Budget | Month must be 1–12 (schema validates) |
| BR-BUD-03 | Budget | Year must be 2000–2100 (schema validates) |
| BR-BUD-04 | Budget | Only one budget per (category, year, month) → 409 |

---

## Backend Testing Rules

**Rule 11:** Every business rule gets a dedicated test named `test_<RULE_CODE>_<description>`. Example: `test_BR_EXP_02_future_date_rejected`.

**Rule 12:** Use `factory-boy` factories for test data. Never use raw dicts or manually construct model instances in tests.

**Rule 13:** Tests that involve `date.today()` comparisons MUST use `@freeze_time("YYYY-MM-DD")` from `freezegun`.

**Rule 14:** The `clean_tables` fixture must call `db.session.remove()` after deleting rows to prevent session state leaking between tests.

**Rule 15:** Coverage target: ≥80% overall, 100% on each `app/modules/<domain>/<domain>_service.py`. Tests live in `tests/modules/<domain>/`.

---

## Frontend Architecture Rules (MUST follow)

### Layer Responsibilities

```
src/api/          → HTTP calls only. No state, no side effects.
src/hooks/        → Server state (React Query). Cache invalidation lives here.
src/store/        → UI state only (modals, active filters). Never server data.
src/pages/        → Thin orchestrators. Compose hooks + components.
src/components/   → Pure functions of props. May call one hook.
```

**Rule 16:** API functions in `src/api/` only make HTTP calls. No state mutations, no toast notifications, nothing else.

**Rule 17:** React Query hooks in `src/hooks/` own all server-side caching. Invalidate related keys on mutations (`expenses` mutations invalidate `dashboard`).

**Rule 18:** Zustand in `src/store/ui.ts` stores ONLY UI state (which modal is open, active month filter). Never store server data in Zustand.

### Type Safety

**Rule 19:** Every API response MUST be parsed through a Zod schema before use. No `as` type assertions on API responses.

**Rule 20:** Form types MUST be derived from Zod schemas via `z.infer<typeof schema>`. No separate type definitions for form values.

**Rule 21:** `strict: true` is enabled in `tsconfig.app.json`. Never use `any`. Use `unknown` when the type is genuinely unknown.

### Forms

**Rule 22:** All forms use `react-hook-form` with `zodResolver`. No manual `useState` for form fields. No manual validation logic outside the Zod schema.

### Testing

**Rule 23:** Test user behavior, not implementation. Use `screen.getByRole` and `screen.getByLabelText` over `getByTestId`.

**Rule 24:** API mocking uses MSW (`tests/mocks/handlers.ts`). Never mock at the module level (no `vi.mock("../api/...")`).

**Rule 25:** Components under test must not call real APIs. MSW intercepts at the network level.

---

## API Response Envelope

All responses follow this envelope:

```json
// Success
{ "data": <payload>, "meta": { ... } }

// Error
{ "error": { "code": "ERROR_CODE", "message": "...", "details": { ... } } }
```

Never break this contract. The frontend Axios interceptor depends on this shape.

---

## Git Conventions

- Branch naming: `feature/`, `fix/`, `refactor/`
- Commit style: imperative mood ("Add expense validation", not "Added")
- Never commit: `.env`, `*.db`, `__pycache__/`, `node_modules/`, `.venv/`

---

## Running the Project

```bash
# Backend
cd backend && python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
flask --app app run --debug

# Frontend
cd frontend && npm install
cp .env.example .env
npm run dev

# Tests
cd backend && pytest
cd frontend && npm test
```
