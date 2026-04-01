import type { CategorySummary } from "../../types/dashboard";

interface Props {
  categories: CategorySummary[];
}

export function BudgetProgress({ categories }: Props) {
  if (categories.length === 0) {
    return <p className="py-4 text-center text-sm text-gray-500">No spending data this month.</p>;
  }

  return (
    <div className="space-y-3">
      {categories.map((categorySummary) => {
        const spent = parseFloat(categorySummary.spent);
        const budgeted = parseFloat(categorySummary.budgeted);
        const percentUsed = categorySummary.percent_used ?? (budgeted === 0 ? 100 : (spent / budgeted) * 100);
        const cappedPercent = Math.min(percentUsed, 100);
        const isOverBudget = categorySummary.is_over_budget;

        return (
          <div key={categorySummary.category_id} data-testid={`budget-progress-${categorySummary.category_id}`}>
            <div className="mb-1 flex items-center justify-between text-sm">
              <span className="font-medium text-gray-800">
                {categorySummary.icon && <span className="mr-1">{categorySummary.icon}</span>}
                {categorySummary.category_name}
              </span>
              <span className={isOverBudget ? "font-semibold text-red-600" : "text-gray-600"}>
                ${spent.toFixed(2)} / ${budgeted > 0 ? budgeted.toFixed(2) : "—"}
              </span>
            </div>
            {budgeted > 0 && (
              <div className="h-2 w-full overflow-hidden rounded-full bg-gray-100">
                <div
                  className={`h-full rounded-full transition-all ${isOverBudget ? "bg-red-500" : "bg-indigo-500"}`}
                  style={{ width: `${cappedPercent}%` }}
                  role="progressbar"
                  aria-valuenow={percentUsed}
                  aria-valuemin={0}
                  aria-valuemax={100}
                  aria-label={`${categorySummary.category_name} budget usage`}
                />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
