import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import * as api from "../api/budgets";
import type { BudgetFilters } from "../api/budgets";
import type { BudgetCreate, BudgetUpdate } from "../types/budget";

export const BUDGETS_KEY = "budgets";

export function useBudgets(filters: BudgetFilters = {}) {
  return useQuery({
    queryKey: [BUDGETS_KEY, filters],
    queryFn: () => api.getBudgets(filters),
    staleTime: 60_000,
  });
}

export function useCreateBudget() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: BudgetCreate) => api.createBudget(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [BUDGETS_KEY] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });
}

export function useUpdateBudget(id: number) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: BudgetUpdate) => api.updateBudget(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [BUDGETS_KEY] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });
}

export function useDeleteBudget() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => api.deleteBudget(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: [BUDGETS_KEY] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    },
  });
}
