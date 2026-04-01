import { z } from "zod";
import { categorySchema } from "./category";

export const expenseSchema = z.object({
  id: z.number(),
  category_id: z.number(),
  category: categorySchema,
  amount: z.string(),
  description: z.string(),
  date: z.string(),
  notes: z.string().nullable(),
  created_at: z.string(),
  updated_at: z.string(),
});

export const expenseCreateSchema = z.object({
  category_id: z.number({ error: "Category is required" }),
  amount: z
    .string()
    .min(1, "Amount is required")
    .refine((v) => parseFloat(v) > 0, "Amount must be greater than 0"),
  description: z.string().min(1, "Description is required").max(500),
  date: z
    .string()
    .min(1, "Date is required")
    .refine((d) => new Date(d) <= new Date(), "Date cannot be in the future"),
  notes: z.string().max(2000).nullable().optional(),
});

export const expenseUpdateSchema = expenseCreateSchema.partial();

export type Expense = z.infer<typeof expenseSchema>;
export type ExpenseCreate = z.infer<typeof expenseCreateSchema>;
export type ExpenseUpdate = z.infer<typeof expenseUpdateSchema>;
