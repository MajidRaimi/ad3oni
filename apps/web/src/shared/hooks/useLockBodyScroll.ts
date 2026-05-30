"use client";

import { useEffect } from "react";

export const useLockBodyScroll = (locked: boolean) => {
  useEffect(() => {
    if (!locked) return;

    const root = document.documentElement;
    const original = root.style.overflow;
    root.style.overflow = "hidden";

    return () => {
      root.style.overflow = original;
    };
  }, [locked]);
};
