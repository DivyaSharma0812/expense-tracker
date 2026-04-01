import { z } from "zod";

export const categorySchema = z.object({
  id: z.number(),
  name: z.string(),
  color: z.string(),
  icon: z.string().nullable(),
  created_at: z.string(),
  updated_at: z.string(),
});

export const categoryCreateSchema = z.object({
  name: z.string().min(1, "Name is required").max(100),
});

export const categoryUpdateSchema = categoryCreateSchema.partial();

export type Category = z.infer<typeof categorySchema>;
export type CategoryCreate = z.infer<typeof categoryCreateSchema>;
export type CategoryUpdate = z.infer<typeof categoryUpdateSchema>;
