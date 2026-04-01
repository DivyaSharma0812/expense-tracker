import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { categoryCreateSchema } from "../../types/category";
import type { CategoryCreate, Category } from "../../types/category";
import { Input } from "../ui/Input";
import { Button } from "../ui/Button";
import { ErrorMessage } from "../ui/ErrorMessage";
import type { ApiError } from "../../types/api";

interface Props {
  initial?: Partial<Category>;
  onSubmit: (data: CategoryCreate) => void;
  isLoading: boolean;
  error: ApiError | null | undefined;
  submitLabel?: string;
}

export function CategoryForm({ initial, onSubmit, isLoading, error, submitLabel = "Save" }: Props) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CategoryCreate>({
    resolver: zodResolver(categoryCreateSchema),
    defaultValues: {
      name: initial?.name ?? "",
    },
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4" noValidate>
      <ErrorMessage error={error} />
      <Input label="Name" {...register("name")} error={errors.name?.message} />
      <div className="flex justify-end gap-2 pt-2">
        <Button type="submit" loading={isLoading}>
          {submitLabel}
        </Button>
      </div>
    </form>
  );
}
