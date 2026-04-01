import type { DashboardSummary } from "../../types/dashboard";

interface Props {
  summary: DashboardSummary;
}

export function SummaryCards({ summary }: Props) {
  const spent = parseFloat(summary.total_spent);
  const budgeted = parseFloat(summary.total_budgeted);
  const remaining = parseFloat(summary.remaining);

  return (
    <div className="grid gap-4 sm:grid-cols-3">
      <Card
        label="Total Spent"
        value={`$${spent.toFixed(2)}`}
        color="text-gray-900"
        icon="💸"
        iconBg="bg-gray-100"
        borderColor="border-l-gray-400"
      />
      <Card
        label="Total Budgeted"
        value={`$${budgeted.toFixed(2)}`}
        color="text-indigo-600"
        icon="🎯"
        iconBg="bg-indigo-50"
        borderColor="border-l-indigo-400"
      />
      <Card
        label="Remaining"
        value={`$${Math.abs(remaining).toFixed(2)}`}
        color={remaining < 0 ? "text-red-600" : "text-green-600"}
        icon="💰"
        iconBg={remaining < 0 ? "bg-red-50" : "bg-green-50"}
        borderColor={remaining < 0 ? "border-l-red-400" : "border-l-green-400"}
        suffix={remaining < 0 ? "over budget" : "left"}
      />
    </div>
  );
}

function Card({
  label,
  value,
  color,
  suffix,
  icon,
  iconBg,
  borderColor,
}: {
  label: string;
  value: string;
  color: string;
  suffix?: string;
  icon: string;
  iconBg: string;
  borderColor: string;
}) {
  return (
    <div className={`rounded-lg border border-gray-200 bg-white p-6 shadow-sm border-l-4 ${borderColor}`}>
      <div className="flex items-center gap-3 mb-3">
        <span className={`flex h-10 w-10 items-center justify-center rounded-lg text-xl ${iconBg}`}>{icon}</span>
        <p className="text-sm font-medium text-gray-500">{label}</p>
      </div>
      <p className={`text-3xl font-bold tracking-tight ${color}`}>{value}</p>
      {suffix && <p className="text-xs text-gray-400 mt-1">{suffix}</p>}
    </div>
  );
}
