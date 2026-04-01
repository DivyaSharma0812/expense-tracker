import { z } from "zod";
import { categorySchema } from "./category";

export const budgetSchema = z.object({
  id: z.number(),
  category_id: z.number(),
  category: categorySchema,
  year: z.number(),
  month: z.number(),
  amount: z.string(),
  created_at: z.string(),
  updated_at: z.string(),
});

export const budgetCreateSchema = z.object({
  category_id: z.number({ error: "Category is required" }),
  year: z.number().int().min(2000).max(2100),
  month: z.number().int().min(1).max(12),
  amount: z
    .string()
    .min(1, "Amount is required")
    .refine((v) => parseFloat(v) > 0, "Amount must be greater than 0"),
});

export const budgetUpdateSchema = z.object({
  amount: z
    .string()
    .min(1, "Amount is required")
    .refine((v) => parseFloat(v) > 0, "Amount must be greater than 0"),
});

export type Budget = z.infer<typeof budgetSchema>;
export type BudgetCreate = z.infer<typeof budgetCreateSchema>;
export type BudgetUpdate = z.infer<typeof budgetUpdateSchema>;
