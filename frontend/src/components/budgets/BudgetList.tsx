import { useState } from "react";
import { toast } from "sonner";
import { useBudgets, useCreateBudget, useUpdateBudget, useDeleteBudget } from "../../hooks/useBudgets";
import { useCategories } from "../../hooks/useCategories";
import { Modal } from "../ui/Modal";
import { Button } from "../ui/Button";
import { Select } from "../ui/Select";
import { ConfirmDialog } from "../ui/ConfirmDialog";
import { BudgetForm } from "./BudgetForm";
import type { Budget, BudgetCreate } from "../../types/budget";
import type { ApiError } from "../../types/api";

const MONTH_NAMES = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export function BudgetList() {
  const now = new Date();
  const [filterYear, setFilterYear] = useState(now.getFullYear());
  const [filterMonth, setFilterMonth] = useState(now.getMonth() + 1);

  const { data: budgets, isLoading } = useBudgets({ year: filterYear, month: filterMonth });
  const { data: categories } = useCategories();
  const createMutation = useCreateBudget();
  const deleteMutation = useDeleteBudget();

  const [editTarget, setEditTarget] = useState<Budget | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [mutationError, setMutationError] = useState<ApiError | null>(null);
  const [confirmDeleteId, setConfirmDeleteId] = useState<number | null>(null);

  const updateMutation = useUpdateBudget(editTarget?.id ?? 0);

  function handleCreate(data: BudgetCreate) {
    setMutationError(null);
    createMutation.mutate(data, {
      onSuccess: () => {
        toast.success("Budget created");
        setShowCreate(false);
      },
      onError: (error) => {
        const apiError = error as unknown as ApiError;
        toast.error(apiError.message);
        setMutationError(apiError);
      },
    });
  }

  function handleUpdate(data: BudgetCreate) {
    if (!editTarget) return;
    setMutationError(null);
    updateMutation.mutate({ amount: data.amount }, {
      onSuccess: () => {
        toast.success("Budget updated");
        setEditTarget(null);
      },
      onError: (error) => {
        const apiError = error as unknown as ApiError;
        toast.error(apiError.message);
        setMutationError(apiError);
      },
    });
  }

  function handleConfirmDelete() {
    if (confirmDeleteId === null) return;
    deleteMutation.mutate(confirmDeleteId, {
      onSuccess: () => {
        toast.success("Budget deleted");
        setConfirmDeleteId(null);
      },
      onError: (error) => {
        const apiError = error as unknown as ApiError;
        toast.error(apiError.message);
        setConfirmDeleteId(null);
      },
    });
  }

  const yearOptions = [2023, 2024, 2025, 2026].map((yearValue) => ({ value: yearValue, label: String(yearValue) }));
  const monthOptions = MONTH_NAMES.slice(1).map((monthName, i) => ({ value: i + 1, label: monthName }));

  return (
    <div>
      <div className="mb-4 flex flex-wrap items-end gap-3">
        <Select
          label="Year"
          options={yearOptions}
          value={filterYear}
          onChange={(event) => setFilterYear(Number(event.target.value))}
        />
        <Select
          label="Month"
          options={monthOptions}
          value={filterMonth}
          onChange={(event) => setFilterMonth(Number(event.target.value))}
        />
        <Button onClick={() => { setShowCreate(true); setMutationError(null); }}>
          + New Budget
        </Button>
      </div>

      {isLoading && <p className="text-gray-500">Loading…</p>}

      {!isLoading && budgets?.length === 0 && (
        <div className="py-12 text-center">
          <p className="text-3xl mb-2">📊</p>
          <p className="text-gray-500">
            No budgets for {MONTH_NAMES[filterMonth]} {filterYear}. Set one to track your spending.
          </p>
        </div>
      )}

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {budgets?.map((budget) => (
          <div
            key={budget.id}
            className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm border-l-4 transition-shadow hover:shadow-md"
            style={{ borderLeftColor: budget.category.color }}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start gap-3">
                <span
                  className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-sm font-bold"
                  style={{ backgroundColor: budget.category.color + "22", color: budget.category.color }}
                >
                  {budget.category.name.charAt(0).toUpperCase()}
                </span>
                <div>
                  <p className="font-medium text-gray-900">{budget.category.name}</p>
                  <span className="inline-flex items-center rounded-full bg-gray-100 px-2 py-0.5 text-xs text-gray-500">
                    {MONTH_NAMES[budget.month]} {budget.year}
                  </span>
                </div>
              </div>
              <p className="text-xl font-bold text-indigo-600">
                ${parseFloat(budget.amount).toFixed(2)}
              </p>
            </div>
            <div className="mt-3 flex justify-end gap-2">
              <Button variant="ghost" size="sm" onClick={() => { setEditTarget(budget); setMutationError(null); }}>
                Edit
              </Button>
              <Button
                variant="danger"
                size="sm"
                onClick={() => setConfirmDeleteId(budget.id)}
              >
                Delete
              </Button>
            </div>
          </div>
        ))}
      </div>

      <ConfirmDialog
        open={confirmDeleteId !== null}
        title="Delete Budget"
        message="Are you sure you want to delete this budget? This action cannot be undone."
        onConfirm={handleConfirmDelete}
        onCancel={() => setConfirmDeleteId(null)}
        isLoading={deleteMutation.isPending}
      />

      <Modal title="New Budget" open={showCreate} onClose={() => setShowCreate(false)}>
        <BudgetForm
          categories={categories ?? []}
          defaultYear={filterYear}
          defaultMonth={filterMonth}
          onSubmit={handleCreate}
          isLoading={createMutation.isPending}
          error={mutationError}
        />
      </Modal>

      <Modal title="Edit Budget" open={editTarget !== null} onClose={() => setEditTarget(null)}>
        {editTarget && (
          <BudgetForm
            initial={editTarget}
            categories={categories ?? []}
            onSubmit={handleUpdate}
            isLoading={updateMutation.isPending}
            error={mutationError}
            submitLabel="Update"
          />
        )}
      </Modal>
    </div>
  );
}
