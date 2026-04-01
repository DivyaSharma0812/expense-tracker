import type { ApiError } from "../../types/api";

interface Props {
  error: ApiError | null | undefined;
}

export function ErrorMessage({ error }: Props) {
  if (!error) return null;
  return (
    <div role="alert" className="rounded-md border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
      <strong>{error.code}: </strong>
      {error.message}
    </div>
  );
}
