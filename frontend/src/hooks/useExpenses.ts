import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import * as api from "../api/expenses";
import type { ExpenseFilters } from "../api/expenses";
import type { ExpenseCreate, ExpenseUpdate } from "../types/expense";

export const EXPENSES_KEY = "expenses";

export function useExpenses(filters: ExpenseFilters = {}) {
  return useQuery({
    queryKey: [EXPENSES_KEY, filters],
    queryFn: () => api.getExpenses(filters),
    staleTime: 30_000,
  });
}

export function useCreateExpense() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ExpenseCreate) => api.createExpense(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [EXPENSES_KEY] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });
}

export function useUpdateExpense(id: number) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: ExpenseUpdate) => api.updateExpense(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [EXPENSES_KEY] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });
}

export function useDeleteExpense() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => api.deleteExpense(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [EXPENSES_KEY] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });
}
