import { useState } from "react";
import { toast } from "sonner";
import { useExpenses, useCreateExpense, useUpdateExpense, useDeleteExpense } from "../../hooks/useExpenses";
import { useCategories } from "../../hooks/useCategories";
import { Modal } from "../ui/Modal";
import { Button } from "../ui/Button";
import { Select } from "../ui/Select";
import { ConfirmDialog } from "../ui/ConfirmDialog";
import { ExpenseForm } from "./ExpenseForm";
import type { Expense, ExpenseCreate } from "../../types/expense";
import type { ApiError } from "../../types/api";

const MONTHS = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
];

export function ExpenseList() {
  const now = new Date();
  const [filterYear, setFilterYear] = useState(now.getFullYear());
  const [filterMonth, setFilterMonth] = useState(now.getMonth() + 1);
  const [filterCategoryId, setFilterCategoryId] = useState<number | undefined>();
  const [page, setPage] = useState(1);

  const { data, isLoading } = useExpenses({
    page,
    per_page: 20,
    year: filterYear,
    month: filterMonth,
    category_id: filterCategoryId,
  });

  const { data: categories } = useCategories();
  const createMutation = useCreateExpense();
  const deleteMutation = useDeleteExpense();

  const [editTarget, setEditTarget] = useState<Expense | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [mutationError, setMutationError] = useState<ApiError | null>(null);
  const [confirmDeleteId, setConfirmDeleteId] = useState<number | null>(null);

  const updateMutation = useUpdateExpense(editTarget?.id ?? 0);

  function handleCreate(data: ExpenseCreate) {
    setMutationError(null);
    createMutation.mutate(data, {
      onSuccess: () => {
        toast.success("Expense added");
        setShowCreate(false);
        setPage(1);
      },
      onError: (error) => {
        const apiError = error as unknown as ApiError;
        toast.error(apiError.message);
        setMutationError(apiError);
      },
    });
  }

  function handleUpdate(data: ExpenseCreate) {
    if (!editTarget) return;
    setMutationError(null);
    updateMutation.mutate(data, {
      onSuccess: () => {
        toast.success("Expense updated");
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
        toast.success("Expense deleted");
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
  const monthOptions = MONTHS.map((monthName, i) => ({ value: i + 1, label: monthName }));
  const categoryOptions = (categories ?? []).map((category) => ({ value: category.id, label: category.name }));

  return (
    <div>
      <div className="mb-4 flex flex-wrap items-end gap-3">
        <Select
          label="Year"
          options={yearOptions}
          value={filterYear}
          onChange={(event) => { setFilterYear(Number(event.target.value)); setPage(1); }}
        />
        <Select
          label="Month"
          options={monthOptions}
          value={filterMonth}
          onChange={(event) => { setFilterMonth(Number(event.target.value)); setPage(1); }}
        />
        <Select
          label="Category"
          options={categoryOptions}
          value={filterCategoryId ?? ""}
          onChange={(event) => { setFilterCategoryId(event.target.value ? Number(event.target.value) : undefined); setPage(1); }}
        />
        <Button onClick={() => { setShowCreate(true); setMutationError(null); }}>
          + New Expense
        </Button>
      </div>

      {isLoading && <p className="text-gray-500">Loading…</p>}

      {!isLoading && data?.expenses.length === 0 && (
        <div className="py-12 text-center">
          <p className="text-3xl mb-2">🧾</p>
          <p className="text-gray-500">No expenses found for this period.</p>
        </div>
      )}

      {!isLoading && data && data.expenses.length > 0 && (
        <div className="overflow-x-auto rounded-lg border border-gray-200 bg-white shadow-sm">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-left">
              <tr>
                <th className="px-4 py-3 text-xs font-semibold uppercase tracking-wider text-gray-500">Date</th>
                <th className="px-4 py-3 text-xs font-semibold uppercase tracking-wider text-gray-500">Description</th>
                <th className="px-4 py-3 text-xs font-semibold uppercase tracking-wider text-gray-500">Category</th>
                <th className="px-4 py-3 text-xs font-semibold uppercase tracking-wider text-gray-500 text-right">Amount</th>
                <th className="px-4 py-3" />
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {data.expenses.map((expense, index) => (
                <tr
                  key={expense.id}
                  className={`group hover:bg-indigo-50 transition-colors ${index % 2 === 0 ? "bg-white" : "bg-gray-50"}`}
                >
                  <td className="px-4 py-3 text-gray-600">{expense.date}</td>
                  <td className="px-4 py-3 font-medium text-gray-900">{expense.description}</td>
                  <td className="px-4 py-3">
                    <span
                      className="inline-flex items-center gap-1.5 rounded-full px-2.5 py-0.5 text-xs font-semibold"
                      style={{ backgroundColor: expense.category.color + "22", color: expense.category.color }}
                    >
                      <span
                        className="h-1.5 w-1.5 rounded-full"
                        style={{ backgroundColor: expense.category.color }}
                      />
                      {expense.category.icon && <span>{expense.category.icon}</span>}
                      {expense.category.name}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right font-mono font-bold text-indigo-700">
                    ${parseFloat(expense.amount).toFixed(2)}
                  </td>
                  <td className="px-4 py-3">
                    <div className="invisible flex justify-end gap-2 group-hover:visible">
                      <Button variant="ghost" size="sm" onClick={() => { setEditTarget(expense); setMutationError(null); }}>
                        Edit
                      </Button>
                      <Button
                        variant="danger"
                        size="sm"
                        onClick={() => setConfirmDeleteId(expense.id)}
                      >
                        Delete
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {data.meta.pages > 1 && (
            <div className="flex items-center justify-between border-t border-gray-200 px-4 py-3">
              <p className="text-xs text-gray-500">
                {data.meta.total} total
              </p>
              <div className="flex gap-2">
                <Button variant="secondary" size="sm" disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
                  Prev
                </Button>
                <span className="flex items-center px-2 text-sm">
                  {page} / {data.meta.pages}
                </span>
                <Button variant="secondary" size="sm" disabled={page >= data.meta.pages} onClick={() => setPage((p) => p + 1)}>
                  Next
                </Button>
              </div>
            </div>
          )}
        </div>
      )}

      <ConfirmDialog
        open={confirmDeleteId !== null}
        title="Delete Expense"
        message="Are you sure you want to delete this expense? This action cannot be undone."
        onConfirm={handleConfirmDelete}
        onCancel={() => setConfirmDeleteId(null)}
        isLoading={deleteMutation.isPending}
      />

      <Modal title="New Expense" open={showCreate} onClose={() => setShowCreate(false)}>
        <ExpenseForm
          categories={categories ?? []}
          onSubmit={handleCreate}
          isLoading={createMutation.isPending}
          error={mutationError}
        />
      </Modal>

      <Modal title="Edit Expense" open={editTarget !== null} onClose={() => setEditTarget(null)}>
        {editTarget && (
          <ExpenseForm
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
