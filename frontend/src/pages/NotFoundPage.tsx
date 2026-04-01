import { Link } from "react-router-dom";

export function NotFoundPage() {
  return (
    <div className="flex flex-col items-center justify-center py-24 text-center">
      <p className="text-4xl font-bold text-gray-300">404</p>
      <p className="mt-2 text-gray-500">Page not found</p>
      <Link to="/" className="mt-4 text-indigo-600 hover:underline">
        Go to Dashboard
      </Link>
    </div>
  );
}
