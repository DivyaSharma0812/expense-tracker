import { http, HttpResponse } from "msw";
import { mockCategories, mockExpenses, mockBudgets } from "./data";

export const handlers = [
  http.get("/api/categories", () =>
    HttpResponse.json({ data: mockCategories })
  ),
  http.post("/api/categories", async ({ request }) => {
    const body = (await request.json()) as Record<string, unknown>;
    const created = { id: 99, ...body, created_at: "2025-01-01T00:00:00Z", updated_at: "2025-01-01T00:00:00Z" };
    return HttpResponse.json({ data: created }, { status: 201 });
  }),
  http.put("/api/categories/:id", async ({ request }) => {
    const body = (await request.json()) as Record<string, unknown>;
    const updated = { ...mockCategories[0], ...body };
    return HttpResponse.json({ data: updated });
  }),
  http.delete("/api/categories/:id", () => new HttpResponse(null, { status: 204 })),

  http.get("/api/expenses", () =>
    HttpResponse.json({
      data: mockExpenses,
      meta: { total: 1, page: 1, per_page: 20, pages: 1 },
    })
  ),
  http.post("/api/expenses", async ({ request }) => {
    const body = (await request.json()) as Record<string, unknown>;
    const created = { id: 99, category: mockCategories[0], ...body, created_at: "2025-03-10T10:00:00Z", updated_at: "2025-03-10T10:00:00Z" };
    return HttpResponse.json({ data: created }, { status: 201 });
  }),
  http.delete("/api/expenses/:id", () => new HttpResponse(null, { status: 204 })),

  http.get("/api/budgets", () =>
    HttpResponse.json({ data: mockBudgets })
  ),
  http.post("/api/budgets", async ({ request }) => {
    const body = (await request.json()) as Record<string, unknown>;
    const created = { id: 99, category: mockCategories[0], ...body, created_at: "2025-01-01T00:00:00Z", updated_at: "2025-01-01T00:00:00Z" };
    return HttpResponse.json({ data: created }, { status: 201 });
  }),
  http.delete("/api/budgets/:id", () => new HttpResponse(null, { status: 204 })),

  http.get("/api/dashboard/summary", () =>
    HttpResponse.json({
      data: {
        year: 2025, month: 3,
        total_spent: "45.99", total_budgeted: "500.00",
        remaining: "454.01", percent_used: 9.2,
        categories: [
          {
            category_id: 1, category_name: "Groceries", color: "#6366f1", icon: "🛒",
            budgeted: "500.00", spent: "45.99", remaining: "454.01",
            percent_used: 9.2, is_over_budget: false, expense_count: 1,
          },
        ],
        unbudgeted_spending: "0", categories_over_budget: 0,
      },
    })
  ),

  http.get("/api/dashboard/trends", () =>
    HttpResponse.json({ data: [] })
  ),
];
