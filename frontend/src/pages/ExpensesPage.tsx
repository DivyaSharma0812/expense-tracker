import { ExpenseList } from "../components/expenses/ExpenseList";

export function ExpensesPage() {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Expenses</h1>
        <p className="mt-1 text-sm text-gray-500">Track and manage your individual transactions.</p>
      </div>
      <ExpenseList />
    </div>
  );
}
