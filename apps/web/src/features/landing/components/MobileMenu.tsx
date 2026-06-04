"use client";

import { useEffect } from "react";
import { motion, useReducedMotion, type Variants } from "motion/react";
import { useLockBodyScroll } from "@/shared/hooks/useLockBodyScroll";
import { toArabicIndex } from "@/shared/lib/arabic";
import { ShareButton } from "@/features/share/components/ShareButton";
import { navLinks } from "../data/navigation";
import { platforms } from "../data/platforms";

const livePlatforms = platforms.filter((platform) => platform.status === "live");

type MobileMenuProps = {
  onClose: () => void;
};

export const MobileMenu = ({ onClose }: MobileMenuProps) => {
  const reduce = useReducedMotion();
  useLockBodyScroll(true);

  useEffect(() => {
    const handleKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [onClose]);

  const list: Variants = {
    hidden: {},
    visible: { transition: { staggerChildren: 0.07, delayChildren: 0.18 } },
  };

  const item: Variants = {
    hidden: { opacity: 0, x: reduce ? 0 : 40 },
    visible: {
      opacity: 1,
      x: 0,
      transition: { duration: 0.5, ease: [0.16, 1, 0.3, 1] },
    },
  };

  return (
    <motion.div
      role="dialog"
      aria-modal
      aria-label="القائمة"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
      className="night-bg fixed inset-0 z-40 flex flex-col px-8 pt-28 pb-12 md:hidden"
    >
      <motion.nav
        variants={list}
        initial="hidden"
        animate="visible"
        className="flex flex-1 flex-col justify-center gap-1"
      >
        {navLinks.map((link, index) => (
          <motion.a
            key={link.href}
            variants={item}
            href={link.href}
            onClick={onClose}
            className="group flex items-baseline gap-4 py-2"
          >
            <span className="font-sans text-base text-lilac/60">
              {toArabicIndex(index + 1)}
            </span>
            <span className="font-display text-5xl text-paper transition-colors group-hover:text-lilac">
              {link.label}
            </span>
          </motion.a>
        ))}
      </motion.nav>

      <motion.div
        variants={item}
        initial="hidden"
        animate="visible"
        className="flex flex-col gap-8"
      >
        <ShareButton variant="paper" size="lg" className="w-full" onClick={onClose}>
          شاركنا دعاءك
        </ShareButton>
        <div className="flex items-center gap-6 text-paper/60">
          {livePlatforms.map((platform) => {
            const Icon = platform.icon;
            return (
              <a
                key={platform.key}
                href={platform.href}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={platform.name}
                className="transition-colors hover:text-paper"
              >
                <Icon className="size-6" />
              </a>
            );
          })}
        </div>
      </motion.div>
    </motion.div>
  );
};
