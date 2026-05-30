import { cn } from "@/shared/lib/utils";

type WordmarkProps = {
  className?: string;
};

export const Wordmark = ({ className }: WordmarkProps) => (
  <span
    className={cn(
      "font-display leading-none tracking-[0.01em] select-none",
      className,
    )}
  >
    ادْعُونِي
  </span>
);
