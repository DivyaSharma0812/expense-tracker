import { useState } from "react";
import { useDashboardSummary, useDashboardTrends } from "../hooks/useDashboard";
import { SummaryCards } from "../components/dashboard/SummaryCards";
import { BudgetProgress } from "../components/dashboard/BudgetProgress";
import { SpendingTrendChart } from "../components/dashboard/SpendingByCategory";
import { Select } from "../components/ui/Select";

const MONTH_NAMES = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export function DashboardPage() {
  const now = new Date();
  const [year, setYear] = useState(now.getFullYear());
  const [month, setMonth] = useState(now.getMonth() + 1);

  const { data: summary, isLoading: summaryLoading } = useDashboardSummary(year, month);
  const { data: trends } = useDashboardTrends(6);

  const yearOptions = [2023, 2024, 2025, 2026].map((yearValue) => ({ value: yearValue, label: String(yearValue) }));
  const monthOptions = MONTH_NAMES.slice(1).map((monthName, i) => ({ value: i + 1, label: monthName }));

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-1 text-sm text-gray-500">Your spending overview at a glance.</p>
      </div>
      <div className="flex flex-wrap items-end gap-3">
        <Select
          label="Year"
          options={yearOptions}
          value={year}
          onChange={(event) => setYear(Number(event.target.value))}
        />
        <Select
          label="Month"
          options={monthOptions}
          value={month}
          onChange={(event) => setMonth(Number(event.target.value))}
        />
      </div>

      {summaryLoading && <p className="text-gray-500">Loading…</p>}

      {summary && (
        <>
          <SummaryCards summary={summary} />

          <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
            <h2 className="mb-4 text-xs font-semibold uppercase tracking-wider text-gray-500">Budget vs Spending</h2>
            <BudgetProgress categories={summary.categories} />
            {summary.categories_over_budget > 0 && (
              <p className="mt-3 text-sm font-medium text-red-600">
                ⚠ {summary.categories_over_budget} {summary.categories_over_budget === 1 ? "category" : "categories"} over budget
              </p>
            )}
          </div>
        </>
      )}

      <div className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
        <h2 className="mb-4 text-xs font-semibold uppercase tracking-wider text-gray-500">6-Month Spending Trend</h2>
        <SpendingTrendChart trends={trends ?? []} />
      </div>
    </div>
  );
}
