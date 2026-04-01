import type { Category } from "../../src/types/category";
import type { Expense } from "../../src/types/expense";
import type { Budget } from "../../src/types/budget";

export const mockCategories: Category[] = [
  { id: 1, name: "Groceries", color: "#6366f1", icon: "🛒", created_at: "2025-01-01T00:00:00Z", updated_at: "2025-01-01T00:00:00Z" },
  { id: 2, name: "Transport", color: "#f59e0b", icon: "🚗", created_at: "2025-01-01T00:00:00Z", updated_at: "2025-01-01T00:00:00Z" },
];

export const mockExpenses: Expense[] = [
  {
    id: 1,
    category_id: 1,
    category: mockCategories[0],
    amount: "45.99",
    description: "Weekly shopping",
    date: "2025-03-10",
    notes: null,
    created_at: "2025-03-10T10:00:00Z",
    updated_at: "2025-03-10T10:00:00Z",
  },
];

export const mockBudgets: Budget[] = [
  {
    id: 1,
    category_id: 1,
    category: mockCategories[0],
    year: 2025,
    month: 3,
    amount: "500.00",
    created_at: "2025-01-01T00:00:00Z",
    updated_at: "2025-01-01T00:00:00Z",
  },
];
