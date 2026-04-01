import { apiClient } from "./client";
import type { ApiResponse } from "../types/api";
import { expenseSchema } from "../types/expense";
import type { Expense, ExpenseCreate, ExpenseUpdate } from "../types/expense";
import { z } from "zod";

const listSchema = z.object({
  data: z.array(expenseSchema),
  meta: z.object({
    total: z.number(),
    page: z.number(),
    per_page: z.number(),
    pages: z.number(),
  }),
});
const singleSchema = z.object({ data: expenseSchema });

export interface ExpenseFilters {
  page?: number;
  per_page?: number;
  category_id?: number;
  year?: number;
  month?: number;
}

export async function getExpenses(
  filters: ExpenseFilters = {}
): Promise<{ expenses: Expense[]; meta: { total: number; page: number; per_page: number; pages: number } }> {
  const response = await apiClient.get<ApiResponse<Expense[]>>("/expenses", { params: filters });
  const parsed = listSchema.parse(response.data);
  return { expenses: parsed.data, meta: parsed.meta };
}

export async function getExpense(id: number): Promise<Expense> {
  const response = await apiClient.get<ApiResponse<Expense>>(`/expenses/${id}`);
  return singleSchema.parse(response.data).data;
}

export async function createExpense(data: ExpenseCreate): Promise<Expense> {
  const response = await apiClient.post<ApiResponse<Expense>>("/expenses", data);
  return singleSchema.parse(response.data).data;
}

export async function updateExpense(id: number, data: ExpenseUpdate): Promise<Expense> {
  const response = await apiClient.put<ApiResponse<Expense>>(`/expenses/${id}`, data);
  return singleSchema.parse(response.data).data;
}

export async function deleteExpense(id: number): Promise<void> {
  await apiClient.delete(`/expenses/${id}`);
}
