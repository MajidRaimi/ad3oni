"use client";

import type { ReactNode } from "react";
import type { VariantProps } from "class-variance-authority";
import { buttonVariants } from "@/shared/ui/button";
import { cn } from "@/shared/lib/utils";
import { useShareModal } from "../store";

type ShareButtonProps = VariantProps<typeof buttonVariants> & {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
};

export const ShareButton = ({
  variant,
  size,
  className,
  children,
  onClick,
}: ShareButtonProps) => {
  const open = useShareModal((state) => state.open);

  const handleClick = () => {
    onClick?.();
    open();
  };

  return (
    <button
      type="button"
      onClick={handleClick}
      className={cn(buttonVariants({ variant, size }), className)}
    >
      {children}
    </button>
  );
};
