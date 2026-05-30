import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/shared/lib/utils";

const buttonVariants = cva(
  "inline-flex shrink-0 items-center justify-center gap-2 rounded-full font-medium leading-none whitespace-nowrap transition-all outline-none focus-visible:ring-[3px] focus-visible:ring-ring/50 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-royal text-paper shadow-royal hover:scale-[1.03]",
        accent: "bg-violet text-paper shadow-violet hover:scale-[1.03]",
        paper: "bg-paper text-royal shadow-royal hover:scale-[1.03]",
        outline: "border border-current/30 bg-transparent hover:bg-current/10",
        ghost: "bg-transparent hover:bg-current/10",
      },
      size: {
        default: "h-12 px-7 text-[15px]",
        sm: "h-10 px-5 text-sm",
        lg: "h-13 px-9 text-base",
        icon: "size-12",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

function Button({
  className,
  variant,
  size,
  ...props
}: React.ComponentProps<"button"> & VariantProps<typeof buttonVariants>) {
  return (
    <button
      data-slot="button"
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
}

export { Button, buttonVariants };
