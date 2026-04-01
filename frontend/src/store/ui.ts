import { create } from "zustand";

interface UiState {
  // Modal control
  openModal: string | null;
  modalData: unknown;
  openModalWith: (name: string, data?: unknown) => void;
  closeModal: () => void;

  // Active month filter for dashboard + budgets
  activeYear: number;
  activeMonth: number;
  setActiveMonth: (year: number, month: number) => void;
}

const now = new Date();

export const useUiStore = create<UiState>((set) => ({
  openModal: null,
  modalData: null,
  openModalWith: (name, data = null) => set({ openModal: name, modalData: data }),
  closeModal: () => set({ openModal: null, modalData: null }),

  activeYear: now.getFullYear(),
  activeMonth: now.getMonth() + 1,
  setActiveMonth: (year, month) => set({ activeYear: year, activeMonth: month }),
}));
