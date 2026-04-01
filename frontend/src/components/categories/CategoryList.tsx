import { useState } from "react";
import { toast } from "sonner";
import { useCategories, useCreateCategory, useUpdateCategory, useDeleteCategory } from "../../hooks/useCategories";
import { Modal } from "../ui/Modal";
import { Button } from "../ui/Button";
import { ErrorMessage } from "../ui/ErrorMessage";
import { ConfirmDialog } from "../ui/ConfirmDialog";
import { CategoryForm } from "./CategoryForm";
import type { Category, CategoryCreate } from "../../types/category";
import type { ApiError } from "../../types/api";

export function CategoryList() {
  const { data: categories, isLoading, error } = useCategories();
  const createMutation = useCreateCategory();
  const deleteMutation = useDeleteCategory();

  const [editTarget, setEditTarget] = useState<Category | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [mutationError, setMutationError] = useState<ApiError | null>(null);
  const [deleteError, setDeleteError] = useState<ApiError | null>(null);
  const [confirmDeleteId, setConfirmDeleteId] = useState<number | null>(null);

  const updateMutation = useUpdateCategory(editTarget?.id ?? 0);

  function handleCreate(data: CategoryCreate) {
    setMutationError(null);
    createMutation.mutate(data, {
      onSuccess: () => {
        toast.success("Category created");
        setShowCreate(false);
      },
      onError: (error) => {
        const apiError = error as unknown as ApiError;
        toast.error(apiError.message);
        setMutationError(apiError);
      },
    });
  }

  function handleUpdate(data: CategoryCreate) {
    if (!editTarget) return;
    setMutationError(null);
    updateMutation.mutate(data, {
      onSuccess: () => {
        toast.success("Category updated");
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
    setDeleteError(null);
    deleteMutation.mutate(confirmDeleteId, {
      onSuccess: () => {
        toast.success("Category deleted");
        setConfirmDeleteId(null);
      },
      onError: (error) => {
        const apiError = error as unknown as ApiError;
        toast.error(apiError.message);
        setDeleteError(apiError);
        setConfirmDeleteId(null);
      },
    });
  }

  if (isLoading) return <p className="text-gray-500">Loading…</p>;
  if (error) return <p className="text-red-500">Failed to load categories.</p>;

  return (
    <div>
      <div className="mb-4 flex justify-end">
        <Button onClick={() => { setShowCreate(true); setMutationError(null); setDeleteError(null); }}>
          + New Category
        </Button>
      </div>

      {categories?.length === 0 && (
        <div className="py-12 text-center">
          <p className="text-3xl mb-2">🗂️</p>
          <p className="text-gray-500">No categories yet. Create one to organize your expenses.</p>
        </div>
      )}

      <ErrorMessage error={deleteError} />

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {categories?.map((category) => (
          <div
            key={category.id}
            className="flex items-center justify-between rounded-lg border border-gray-200 bg-white p-4 shadow-sm border-l-4 transition-shadow hover:shadow-md"
            style={{ borderLeftColor: category.color }}
          >
            <div className="flex items-center gap-3">
              <span
                className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full text-sm font-bold"
                style={{ backgroundColor: category.color + "22", color: category.color }}
              >
                {category.name.charAt(0).toUpperCase()}
              </span>
              <div>
                <p className="font-medium text-gray-900">{category.name}</p>
              </div>
            </div>
            <div className="flex gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => { setEditTarget(category); setMutationError(null); setDeleteError(null); }}
              >
                Edit
              </Button>
              <Button
                variant="danger"
                size="sm"
                onClick={() => { setDeleteError(null); setConfirmDeleteId(category.id); }}
              >
                Delete
              </Button>
            </div>
          </div>
        ))}
      </div>

      <ConfirmDialog
        open={confirmDeleteId !== null}
        title="Delete Category"
        message="Are you sure you want to delete this category? This action cannot be undone."
        onConfirm={handleConfirmDelete}
        onCancel={() => setConfirmDeleteId(null)}
        isLoading={deleteMutation.isPending}
      />

      <Modal title="New Category" open={showCreate} onClose={() => setShowCreate(false)}>
        <CategoryForm
          onSubmit={handleCreate}
          isLoading={createMutation.isPending}
          error={mutationError}
        />
      </Modal>

      <Modal
        title="Edit Category"
        open={editTarget !== null}
        onClose={() => setEditTarget(null)}
      >
        {editTarget && (
          <CategoryForm
            initial={editTarget}
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
