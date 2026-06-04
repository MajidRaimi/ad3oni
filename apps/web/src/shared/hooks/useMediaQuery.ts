"use client";

import { useSyncExternalStore } from "react";

export const useMediaQuery = (query: string) => {
  const subscribe = (onChange: () => void) => {
    const list = window.matchMedia(query);
    list.addEventListener("change", onChange);
    return () => list.removeEventListener("change", onChange);
  };

  return useSyncExternalStore(
    subscribe,
    () => window.matchMedia(query).matches,
    () => false,
  );
};
