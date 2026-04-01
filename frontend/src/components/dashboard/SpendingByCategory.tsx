import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import type { MonthlyTrend } from "../../types/dashboard";

interface Props {
  trends: MonthlyTrend[];
}

const MONTH_SHORT = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

export function SpendingTrendChart({ trends }: Props) {
  const data = trends.map((trend) => ({
    label: `${MONTH_SHORT[trend.month]} ${trend.year}`,
    spent: parseFloat(trend.total_spent),
    budgeted: parseFloat(trend.total_budgeted),
  }));

  if (data.length === 0) {
    return <p className="py-4 text-center text-sm text-gray-500">No trend data available yet.</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={200}>
      <BarChart data={data} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis dataKey="label" tick={{ fontSize: 12 }} />
        <YAxis tick={{ fontSize: 12 }} tickFormatter={(value: number) => `$${value}`} />
        <Tooltip formatter={(value) => `$${Number(value).toFixed(2)}`} />
        <Bar dataKey="budgeted" fill="#e0e7ff" name="Budgeted" radius={[4, 4, 0, 0]} />
        <Bar dataKey="spent" fill="#6366f1" name="Spent" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
