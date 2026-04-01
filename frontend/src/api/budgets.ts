import { apiClient } from "./client";
import type { ApiResponse } from "../types/api";
import { budgetSchema } from "../types/budget";
import type { Budget, BudgetCreate, BudgetUpdate } from "../types/budget";
import { z } from "zod";

const listSchema = z.object({ data: z.array(budgetSchema) });
const singleSchema = z.object({ data: budgetSchema });

export interface BudgetFilters {
  year?: number;
  month?: number;
  category_id?: number;
}

export async function getBudgets(filters: BudgetFilters = {}): Promise<Budget[]> {
  const response = await apiClient.get<ApiResponse<Budget[]>>("/budgets", { params: filters });
  return listSchema.parse(response.data).data;
}

export async function getBudget(id: number): Promise<Budget> {
  const response = await apiClient.get<ApiResponse<Budget>>(`/budgets/${id}`);
  return singleSchema.parse(response.data).data;
}

export async function createBudget(data: BudgetCreate): Promise<Budget> {
  const response = await apiClient.post<ApiResponse<Budget>>("/budgets", data);
  return singleSchema.parse(response.data).data;
}

export async function updateBudget(id: number, data: BudgetUpdate): Promise<Budget> {
  const response = await apiClient.put<ApiResponse<Budget>>(`/budgets/${id}`, data);
  return singleSchema.parse(response.data).data;
}

export async function deleteBudget(id: number): Promise<void> {
  await apiClient.delete(`/budgets/${id}`);
}
