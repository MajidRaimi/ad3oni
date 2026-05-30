"use client";

import { useEffect, useState } from "react";

export const useScrolledPastViewport = (ratio = 0.85) => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > window.innerHeight * ratio);
    };

    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, [ratio]);

  return scrolled;
};
