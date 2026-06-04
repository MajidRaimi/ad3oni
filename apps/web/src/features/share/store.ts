import { create } from "zustand";

type ShareModalState = {
  isOpen: boolean;
  open: () => void;
  close: () => void;
};

export const useShareModal = create<ShareModalState>((set) => ({
  isOpen: false,
  open: () => set({ isOpen: true }),
  close: () => set({ isOpen: false }),
}));
