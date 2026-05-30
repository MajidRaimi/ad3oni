"use client";

import { useEffect, useState } from "react";

export const useHideOnScroll = (threshold = 80, idleDelay = 200) => {
  const [hidden, setHidden] = useState(false);

  useEffect(() => {
    let lastY = window.scrollY;
    let timeout: ReturnType<typeof setTimeout>;

    const handleScroll = () => {
      const y = window.scrollY;
      if (y > lastY && y > threshold) {
        setHidden(true);
      } else if (y < lastY) {
        setHidden(false);
      }
      lastY = y;
      clearTimeout(timeout);
      timeout = setTimeout(() => setHidden(false), idleDelay);
    };

    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => {
      clearTimeout(timeout);
      window.removeEventListener("scroll", handleScroll);
    };
  }, [threshold, idleDelay]);

  return hidden;
};
