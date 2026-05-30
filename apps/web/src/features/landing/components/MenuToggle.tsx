"use client";

import { motion, type Variants } from "motion/react";
import { cn } from "@/shared/lib/utils";

const barTransition = { duration: 0.32, ease: [0.16, 1, 0.3, 1] as const };

const topBar: Variants = {
  closed: { y: 0, rotate: 0 },
  open: { y: 6, rotate: 45 },
};

const middleBar: Variants = {
  closed: { opacity: 1, scaleX: 1 },
  open: { opacity: 0, scaleX: 0 },
};

const bottomBar: Variants = {
  closed: { y: 0, rotate: 0 },
  open: { y: -6, rotate: -45 },
};

const bar = "absolute inset-x-0 mx-auto h-[2px] w-6 rounded-full bg-current";

type MenuToggleProps = {
  open: boolean;
  onClick: () => void;
};

export const MenuToggle = ({ open, onClick }: MenuToggleProps) => (
  <motion.button
    type="button"
    onClick={onClick}
    whileTap={{ scale: 0.88 }}
    animate={open ? "open" : "closed"}
    aria-label={open ? "إغلاق القائمة" : "فتح القائمة"}
    aria-expanded={open}
    className="group relative flex size-11 items-center justify-center rounded-full text-paper transition-colors hover:bg-paper/10 md:hidden"
  >
    <span className="relative block h-4 w-6">
      <motion.span
        variants={topBar}
        transition={barTransition}
        style={{ top: 1 }}
        className={bar}
      />
      <motion.span
        variants={middleBar}
        transition={barTransition}
        style={{ top: 7 }}
        className={cn(bar, "w-4 transition-[width] duration-300 group-hover:w-6")}
      />
      <motion.span
        variants={bottomBar}
        transition={barTransition}
        style={{ top: 13 }}
        className={bar}
      />
    </span>
  </motion.button>
);
