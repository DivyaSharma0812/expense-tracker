import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { expenseCreateSchema } from "../../types/expense";
import type { ExpenseCreate, Expense } from "../../types/expense";
import type { Category } from "../../types/category";
import { Input } from "../ui/Input";
import { Select } from "../ui/Select";
import { Button } from "../ui/Button";
import { ErrorMessage } from "../ui/ErrorMessage";
import type { ApiError } from "../../types/api";

interface Props {
  initial?: Partial<Expense>;
  categories: Category[];
  onSubmit: (data: ExpenseCreate) => void;
  isLoading: boolean;
  error: ApiError | null | undefined;
  submitLabel?: string;
}

export function ExpenseForm({ initial, categories, onSubmit, isLoading, error, submitLabel = "Save" }: Props) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ExpenseCreate>({
    resolver: zodResolver(expenseCreateSchema),
    defaultValues: {
      category_id: initial?.category_id ?? undefined,
      amount: initial?.amount ?? "",
      description: initial?.description ?? "",
      date: initial?.date ?? new Date().toISOString().split("T")[0],
      notes: initial?.notes ?? "",
    },
  });

  const categoryOptions = categories.map((category) => ({ value: category.id, label: `${category.icon ?? ""} ${category.name}`.trim() }));

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4" noValidate>
      <ErrorMessage error={error} />
      <Select
        label="Category"
        options={categoryOptions}
        {...register("category_id", { valueAsNumber: true })}
        error={errors.category_id?.message}
      />
      <Input
        label="Amount"
        type="number"
        step="0.01"
        min="0.01"
        placeholder="0.00"
        {...register("amount")}
        error={errors.amount?.message}
      />
      <Input label="Description" {...register("description")} error={errors.description?.message} />
      <Input label="Date" type="date" {...register("date")} error={errors.date?.message} />
      <Input label="Notes (optional)" {...register("notes")} error={errors.notes?.message} />
      <div className="flex justify-end gap-2 pt-2">
        <Button type="submit" loading={isLoading}>
          {submitLabel}
        </Button>
      </div>
    </form>
  );
}
