"use client";

import { useEffect } from "react";

let lockCount = 0;
let originalOverflow = "";

export const useLockBodyScroll = (locked: boolean) => {
  useEffect(() => {
    if (!locked) return;

    const root = document.documentElement;
    if (lockCount === 0) {
      originalOverflow = root.style.overflow;
      root.style.overflow = "hidden";
    }
    lockCount += 1;

    return () => {
      lockCount -= 1;
      if (lockCount === 0) {
        root.style.overflow = originalOverflow;
      }
    };
  }, [locked]);
};
