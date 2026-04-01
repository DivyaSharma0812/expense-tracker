import type { SelectHTMLAttributes } from "react";
import { forwardRef } from "react";

interface Option {
  value: string | number;
  label: string;
}

interface Props extends SelectHTMLAttributes<HTMLSelectElement> {
  label: string;
  options: Option[];
  error?: string;
}

export const Select = forwardRef<HTMLSelectElement, Props>(function Select(
  { label, options, error, className = "", id, ...props },
  ref
) {
  const selectId = id ?? label.toLowerCase().replace(/\s+/g, "-");
  return (
    <div className="flex flex-col gap-1">
      <label htmlFor={selectId} className="mb-0.5 text-sm font-medium text-gray-700">
        {label}
      </label>
      <select
        id={selectId}
        ref={ref}
        className={`w-full rounded-md border px-3 py-2.5 text-sm shadow-sm transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 ${
          error ? "border-red-500" : "border-gray-300"
        } ${className}`}
        {...props}
      >
        <option value="">Select…</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && <p className="text-xs text-red-600">{error}</p>}
    </div>
  );
});
