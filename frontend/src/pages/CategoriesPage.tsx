import { CategoryList } from "../components/categories/CategoryList";

export function CategoriesPage() {
  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Categories</h1>
        <p className="mt-1 text-sm text-gray-500">Organize your spending into named groups.</p>
      </div>
      <CategoryList />
    </div>
  );
}
