import { apiClient } from "./client";
import type { DashboardSummary, MonthlyTrend } from "../types/dashboard";

export async function getDashboardSummary(year?: number, month?: number): Promise<DashboardSummary> {
  const response = await apiClient.get<{ data: DashboardSummary }>("/dashboard/summary", {
    params: { year, month },
  });
  return response.data.data;
}

export async function getDashboardTrends(months = 6): Promise<MonthlyTrend[]> {
  const response = await apiClient.get<{ data: MonthlyTrend[] }>("/dashboard/trends", {
    params: { months },
  });
  return response.data.data;
}
