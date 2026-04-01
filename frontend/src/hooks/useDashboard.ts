import { useQuery } from "@tanstack/react-query";
import { getDashboardSummary, getDashboardTrends } from "../api/dashboard";

export function useDashboardSummary(year?: number, month?: number) {
  return useQuery({
    queryKey: ["dashboard", "summary", year, month],
    queryFn: () => getDashboardSummary(year, month),
    staleTime: 30_000,
  });
}

export function useDashboardTrends(months = 6) {
  return useQuery({
    queryKey: ["dashboard", "trends", months],
    queryFn: () => getDashboardTrends(months),
    staleTime: 60_000,
  });
}
