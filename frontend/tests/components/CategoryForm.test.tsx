import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";
import { CategoryForm } from "../../src/components/categories/CategoryForm";

function renderForm(overrides = {}) {
  const onSubmit = vi.fn();
  const props = {
    onSubmit,
    isLoading: false,
    error: null,
    ...overrides,
  };
  render(<CategoryForm {...props} />);
  return { onSubmit };
}

describe("CategoryForm", () => {
  it("renders name field only", () => {
    renderForm();
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.queryByLabelText(/color/i)).not.toBeInTheDocument();
    expect(screen.queryByLabelText(/icon/i)).not.toBeInTheDocument();
  });

  it("shows validation error when name is empty", async () => {
    renderForm();
    await userEvent.click(screen.getByRole("button", { name: /save/i }));
    await waitFor(() => {
      expect(screen.getByText(/name is required/i)).toBeInTheDocument();
    });
  });

  it("calls onSubmit with valid data", async () => {
    const { onSubmit } = renderForm();
    await userEvent.type(screen.getByLabelText(/name/i), "Groceries");
    await userEvent.click(screen.getByRole("button", { name: /save/i }));
    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith(
        expect.objectContaining({ name: "Groceries" }),
        expect.anything()
      );
    });
  });

  it("disables submit button while loading", () => {
    renderForm({ isLoading: true });
    expect(screen.getByRole("button", { name: /save/i })).toBeDisabled();
  });

  it("displays API error from parent", () => {
    renderForm({ error: { code: "CONFLICT", message: "Name already exists" } });
    expect(screen.getByRole("alert")).toHaveTextContent("Name already exists");
  });

  it("pre-fills fields from initial prop", () => {
    renderForm({ initial: { name: "Food", color: "#ff0000" } });
    expect(screen.getByLabelText<HTMLInputElement>(/name/i).value).toBe("Food");
  });
});
