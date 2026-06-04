import { create } from "zustand";

type ShareView = "form" | "success";

type ShareModalState = {
  isOpen: boolean;
  view: ShareView;
  open: () => void;
  close: () => void;
  showSuccess: () => void;
  reset: () => void;
};

export const useShareModal = create<ShareModalState>((set) => ({
  isOpen: false,
  view: "form",
  open: () => set({ isOpen: true, view: "form" }),
  close: () => set({ isOpen: false }),
  showSuccess: () => set({ view: "success" }),
  reset: () => set({ view: "form" }),
}));
