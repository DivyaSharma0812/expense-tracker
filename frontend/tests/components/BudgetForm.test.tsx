import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { BudgetForm } from "../../src/components/budgets/BudgetForm";
import { mockCategories } from "../mocks/data";

function renderForm(overrides = {}) {
  const onSubmit = vi.fn();
  const props = {
    categories: mockCategories,
    onSubmit,
    isLoading: false,
    error: null,
    ...overrides,
  };
  render(<BudgetForm {...props} />);
  return { onSubmit };
}

describe("BudgetForm", () => {
  it("renders category, year, month, and amount fields", () => {
    renderForm();
    expect(screen.getByLabelText(/category/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/year/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/month/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/budget amount/i)).toBeInTheDocument();
  });

  it("shows error when amount is 0", async () => {
    renderForm();
    await userEvent.type(screen.getByLabelText(/budget amount/i), "0");
    await userEvent.click(screen.getByRole("button", { name: /save/i }));
    await waitFor(() => {
      expect(screen.getByText(/greater than 0/i)).toBeInTheDocument();
    });
  });

  it("displays API conflict error", () => {
    renderForm({ error: { code: "CONFLICT", message: "Budget already exists" } });
    expect(screen.getByRole("alert")).toHaveTextContent("Budget already exists");
  });

  it("disables submit while loading", () => {
    renderForm({ isLoading: true });
    expect(screen.getByRole("button", { name: /save/i })).toBeDisabled();
  });
});
