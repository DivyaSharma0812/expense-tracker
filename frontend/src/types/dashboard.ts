export interface CategorySummary {
  category_id: number;
  category_name: string;
  color: string;
  icon: string | null;
  budgeted: string;
  spent: string;
  remaining: string;
  percent_used: number | null;
  is_over_budget: boolean;
  expense_count: number;
}

export interface DashboardSummary {
  year: number;
  month: number;
  total_spent: string;
  total_budgeted: string;
  remaining: string;
  percent_used: number | null;
  categories: CategorySummary[];
  unbudgeted_spending: string;
  categories_over_budget: number;
}

export interface MonthlyTrend {
  year: number;
  month: number;
  total_spent: string;
  total_budgeted: string;
}
