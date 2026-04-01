import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { ExpenseForm } from "../../src/components/expenses/ExpenseForm";
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
  render(<ExpenseForm {...props} />);
  return { onSubmit };
}

describe("ExpenseForm", () => {
  it("renders all fields", () => {
    renderForm();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/amount/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/date/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/category/i)).toBeInTheDocument();
  });

  it("shows error when description is empty", async () => {
    renderForm();
    await userEvent.click(screen.getByRole("button", { name: /save/i }));
    await waitFor(() => {
      expect(screen.getByText(/description is required/i)).toBeInTheDocument();
    });
  });

  it("shows error when amount is 0", async () => {
    renderForm();
    await userEvent.type(screen.getByLabelText(/description/i), "Coffee");
    await userEvent.clear(screen.getByLabelText(/amount/i));
    await userEvent.type(screen.getByLabelText(/amount/i), "0");
    await userEvent.click(screen.getByRole("button", { name: /save/i }));
    await waitFor(() => {
      expect(screen.getByText(/greater than 0/i)).toBeInTheDocument();
    });
  });

  it("rejects a future date", async () => {
    renderForm();
    const futureDate = new Date();
    futureDate.setDate(futureDate.getDate() + 1);
    const futureDateStr = futureDate.toISOString().split("T")[0];

    await userEvent.type(screen.getByLabelText(/description/i), "Test");
    await userEvent.type(screen.getByLabelText(/amount/i), "10");

    const dateInput = screen.getByLabelText(/date/i);
    await userEvent.clear(dateInput);
    await userEvent.type(dateInput, futureDateStr);
    await userEvent.click(screen.getByRole("button", { name: /save/i }));

    await waitFor(() => {
      expect(screen.getByText(/cannot be in the future/i)).toBeInTheDocument();
    });
  });

  it("displays API error", () => {
    renderForm({ error: { code: "BUSINESS_RULE_VIOLATION", message: "Future date not allowed" } });
    expect(screen.getByRole("alert")).toHaveTextContent("Future date not allowed");
  });
});
