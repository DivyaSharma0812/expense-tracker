import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import { BudgetProgress } from "../../src/components/dashboard/BudgetProgress";
import type { CategorySummary } from "../../src/types/dashboard";

const baseCategory: CategorySummary = {
  category_id: 1,
  category_name: "Groceries",
  color: "#6366f1",
  icon: "🛒",
  budgeted: "500.00",
  spent: "200.00",
  remaining: "300.00",
  percent_used: 40,
  is_over_budget: false,
  expense_count: 3,
};

describe("BudgetProgress", () => {
  it("renders category name", () => {
    render(<BudgetProgress categories={[baseCategory]} />);
    expect(screen.getByText("Groceries")).toBeInTheDocument();
  });

  it("shows spent and budgeted amounts", () => {
    render(<BudgetProgress categories={[baseCategory]} />);
    expect(screen.getByText(/200.00/)).toBeInTheDocument();
    expect(screen.getByText(/500.00/)).toBeInTheDocument();
  });

  it("progress bar is not red when under budget", () => {
    render(<BudgetProgress categories={[baseCategory]} />);
    const bar = screen.getByRole("progressbar");
    expect(bar.className).not.toContain("bg-red-500");
    expect(bar.className).toContain("bg-indigo-500");
  });

  it("progress bar is red when over budget", () => {
    const overBudgetCategory: CategorySummary = { ...baseCategory, is_over_budget: true, spent: "600.00", remaining: "-100.00" };
    render(<BudgetProgress categories={[overBudgetCategory]} />);
    const bar = screen.getByRole("progressbar");
    expect(bar.className).toContain("bg-red-500");
  });

  it("shows empty state when no categories", () => {
    render(<BudgetProgress categories={[]} />);
    expect(screen.getByText(/no spending data/i)).toBeInTheDocument();
  });

  it("shows the correct progressbar width for 40%", () => {
    render(<BudgetProgress categories={[baseCategory]} />);
    const bar = screen.getByRole("progressbar");
    expect(bar.style.width).toBe("40%");
  });
});
