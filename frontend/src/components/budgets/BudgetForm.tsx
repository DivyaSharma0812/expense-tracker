import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { budgetCreateSchema } from "../../types/budget";
import type { BudgetCreate, Budget } from "../../types/budget";
import type { Category } from "../../types/category";
import { Input } from "../ui/Input";
import { Select } from "../ui/Select";
import { Button } from "../ui/Button";
import { ErrorMessage } from "../ui/ErrorMessage";
import type { ApiError } from "../../types/api";

const MONTHS = [
  { value: 1, label: "January" }, { value: 2, label: "February" },
  { value: 3, label: "March" }, { value: 4, label: "April" },
  { value: 5, label: "May" }, { value: 6, label: "June" },
  { value: 7, label: "July" }, { value: 8, label: "August" },
  { value: 9, label: "September" }, { value: 10, label: "October" },
  { value: 11, label: "November" }, { value: 12, label: "December" },
];

interface Props {
  initial?: Partial<Budget>;
  categories: Category[];
  defaultYear?: number;
  defaultMonth?: number;
  onSubmit: (data: BudgetCreate) => void;
  isLoading: boolean;
  error: ApiError | null | undefined;
  submitLabel?: string;
}

export function BudgetForm({
  initial,
  categories,
  defaultYear,
  defaultMonth,
  onSubmit,
  isLoading,
  error,
  submitLabel = "Save",
}: Props) {
  const now = new Date();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<BudgetCreate>({
    resolver: zodResolver(budgetCreateSchema),
    defaultValues: {
      category_id: initial?.category_id ?? undefined,
      year: initial?.year ?? defaultYear ?? now.getFullYear(),
      month: initial?.month ?? defaultMonth ?? now.getMonth() + 1,
      amount: initial?.amount ?? "",
    },
  });

  const categoryOptions = categories.map((category) => ({ value: category.id, label: `${category.icon ?? ""} ${category.name}`.trim() }));
  const yearOptions = [2023, 2024, 2025, 2026].map((yearValue) => ({ value: yearValue, label: String(yearValue) }));

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4" noValidate>
      <ErrorMessage error={error} />
      <Select
        label="Category"
        options={categoryOptions}
        {...register("category_id", { valueAsNumber: true })}
        error={errors.category_id?.message}
      />
      <Select
        label="Year"
        options={yearOptions}
        {...register("year", { valueAsNumber: true })}
        error={errors.year?.message}
      />
      <Select
        label="Month"
        options={MONTHS}
        {...register("month", { valueAsNumber: true })}
        error={errors.month?.message}
      />
      <Input
        label="Budget Amount"
        type="number"
        step="0.01"
        min="0.01"
        placeholder="0.00"
        {...register("amount")}
        error={errors.amount?.message}
      />
      <div className="flex justify-end gap-2 pt-2">
        <Button type="submit" loading={isLoading}>
          {submitLabel}
        </Button>
      </div>
    </form>
  );
}
