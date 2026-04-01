import { apiClient } from "./client";
import type { ApiResponse } from "../types/api";
import { categorySchema } from "../types/category";
import type { Category, CategoryCreate, CategoryUpdate } from "../types/category";
import { z } from "zod";

const listSchema = z.object({ data: z.array(categorySchema) });
const singleSchema = z.object({ data: categorySchema });

export async function getCategories(): Promise<Category[]> {
  const response = await apiClient.get<ApiResponse<Category[]>>("/categories");
  return listSchema.parse(response.data).data;
}

export async function getCategory(id: number): Promise<Category> {
  const response = await apiClient.get<ApiResponse<Category>>(`/categories/${id}`);
  return singleSchema.parse(response.data).data;
}

export async function createCategory(data: CategoryCreate): Promise<Category> {
  const response = await apiClient.post<ApiResponse<Category>>("/categories", data);
  return singleSchema.parse(response.data).data;
}

export async function updateCategory(id: number, data: CategoryUpdate): Promise<Category> {
  const response = await apiClient.put<ApiResponse<Category>>(`/categories/${id}`, data);
  return singleSchema.parse(response.data).data;
}

export async function deleteCategory(id: number): Promise<void> {
  await apiClient.delete(`/categories/${id}`);
}
