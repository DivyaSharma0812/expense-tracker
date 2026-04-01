import { BudgetList } from "../components/budgets/BudgetList";

export function BudgetsPage() {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Budgets</h1>
        <p className="mt-1 text-sm text-gray-500">Set monthly spending limits per category.</p>
      </div>
      <BudgetList />
    </div>
  );
}
