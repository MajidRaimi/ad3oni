import type { ReactNode } from "react";
import { cn } from "@/shared/lib/utils";

type BracePrayerProps = {
  children: ReactNode;
  className?: string;
  braceClassName?: string;
};

export const BracePrayer = ({
  children,
  className,
  braceClassName,
}: BracePrayerProps) => (
  <div
    className={cn(
      "flex items-center justify-center gap-3 md:gap-10",
      className,
    )}
  >
    <span
      aria-hidden
      className={cn(
        "font-display leading-none text-current/40 select-none text-5xl md:text-[150px]",
        braceClassName,
      )}
    >
      &#123;
    </span>
    <div className="text-center">{children}</div>
    <span
      aria-hidden
      className={cn(
        "font-display leading-none text-current/40 select-none text-5xl md:text-[150px]",
        braceClassName,
      )}
    >
      &#125;
    </span>
  </div>
);
