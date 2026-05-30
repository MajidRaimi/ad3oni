"use client";

import Link from "next/link";
import { AnimatePresence } from "motion/react";
import { useDisclosure } from "@/shared/hooks/useDisclosure";
import { useHideOnScroll } from "@/shared/hooks/useHideOnScroll";
import { useScrolledPastViewport } from "@/shared/hooks/useScrolledPastViewport";
import { buttonVariants } from "@/shared/ui/button";
import { cn } from "@/shared/lib/utils";
import { navLinks } from "../data/navigation";
import { MenuToggle } from "./MenuToggle";
import { MobileMenu } from "./MobileMenu";
import { Wordmark } from "./Wordmark";

export const SiteNav = () => {
  const drawer = useDisclosure();
  const scrolled = useScrolledPastViewport();
  const hiddenOnScroll = useHideOnScroll();
  const glass = scrolled && !drawer.isOpen;
  const hidden = hiddenOnScroll && !drawer.isOpen;

  return (
    <header className="fixed inset-x-0 top-0 z-50">
      <nav
        className={cn(
          "w-full border-b transition-all duration-700 ease-out",
          glass
            ? "border-paper/10 bg-royal/70 backdrop-blur-xl"
            : "border-transparent bg-transparent",
          hidden && "-translate-y-full",
        )}
      >
        <div className="mx-auto flex h-20 max-w-7xl items-center justify-between gap-6 px-6 md:px-10">
          <Link
            href="/"
            className="relative z-50 text-paper transition-opacity hover:opacity-80"
            aria-label="ادْعُونِي"
          >
            <Wordmark className="text-[30px]" />
          </Link>

          <div className="hidden items-center gap-9 md:flex">
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="text-[15px] text-paper/75 transition-colors hover:text-paper"
              >
                {link.label}
              </a>
            ))}
            <a href="#share" className={buttonVariants({ variant: "paper", size: "sm" })}>
              شاركنا دعاءك
            </a>
          </div>

          <div className="relative z-50 md:hidden">
            <MenuToggle open={drawer.isOpen} onClick={drawer.toggle} />
          </div>
        </div>
      </nav>

      <AnimatePresence>
        {drawer.isOpen && <MobileMenu onClose={drawer.close} />}
      </AnimatePresence>
    </header>
  );
};
