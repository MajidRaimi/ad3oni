"use client";

import { ArrowUpLeft, Check } from "lucide-react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { useRef, useState, type KeyboardEvent } from "react";
import { toArabicIndex } from "@/shared/lib/arabic";
import { cn } from "@/shared/lib/utils";
import { buttonVariants } from "@/shared/ui/button";
import { IsolatedHandles } from "@/shared/ui/IsolatedHandles";
import { ShareButton } from "@/features/share/components/ShareButton";
import { platforms } from "../data/platforms";
import { PlatformPreview } from "./PlatformPreview";

export const PlatformTabs = () => {
  const reduceMotion = useReducedMotion();
  const [active, setActive] = useState(0);
  const tabRefs = useRef<(HTMLButtonElement | null)[]>([]);
  const platform = platforms[active];
  const isLive = platform.status === "live";

  const focusTab = (index: number) => {
    setActive(index);
    tabRefs.current[index]?.focus();
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    const count = platforms.length;
    let next: number | null = null;
    if (event.key === "ArrowLeft") next = (active + 1) % count;
    else if (event.key === "ArrowRight") next = (active - 1 + count) % count;
    else if (event.key === "Home") next = 0;
    else if (event.key === "End") next = count - 1;
    if (next !== null) {
      event.preventDefault();
      focusTab(next);
    }
  };

  return (
    <div className="w-full">
      <div
        role="tablist"
        aria-label="منصّاتنا"
        onKeyDown={handleKeyDown}
        className="flex flex-wrap justify-center gap-2 md:gap-3"
      >
        {platforms.map((item, index) => {
          const Icon = item.icon;
          const selected = index === active;
          return (
            <button
              key={item.key}
              ref={(el) => {
                tabRefs.current[index] = el;
              }}
              role="tab"
              id={`platform-tab-${item.key}`}
              aria-selected={selected}
              aria-controls={`platform-panel-${item.key}`}
              tabIndex={selected ? 0 : -1}
              onClick={() => setActive(index)}
              className={cn(
                "inline-flex items-center gap-2 rounded-full px-4 py-2.5 text-sm transition-all outline-none focus-visible:ring-[3px] focus-visible:ring-ring/50",
                selected
                  ? "bg-royal text-paper shadow-royal"
                  : "border border-border bg-paper text-neutral hover:border-violet/40 hover:text-royal",
              )}
            >
              <Icon className="size-4" />
              {item.name}
            </button>
          );
        })}
      </div>

      <div className="mt-10">
        <AnimatePresence mode="wait">
          <motion.div
            key={platform.key}
            role="tabpanel"
            id={`platform-panel-${platform.key}`}
            aria-labelledby={`platform-tab-${platform.key}`}
            initial={reduceMotion ? false : { opacity: 0, y: 12 }}
            animate={reduceMotion ? undefined : { opacity: 1, y: 0 }}
            exit={reduceMotion ? undefined : { opacity: 0, y: -12 }}
            transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
            className="grid gap-10 rounded-3xl border border-border bg-paper p-8 md:grid-cols-2 md:p-12"
          >
            <div className="flex flex-col gap-8">
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-3">
                  <h3 className="font-display text-3xl text-royal">{platform.name}</h3>
                  {isLive ? (
                    <span className="flex items-center gap-1.5 text-xs text-violet">
                      <span className="size-2 rounded-full bg-violet" />
                      متاح الآن
                    </span>
                  ) : (
                    <span className="rounded-full bg-muted px-3 py-1 text-xs text-neutral">
                      قريبًا
                    </span>
                  )}
                </div>
                <span
                  dir="ltr"
                  className={cn(
                    "self-start text-xs text-neutral/70",
                    /[؀-ۿ]/.test(platform.handle) ? "font-sans" : "font-mono",
                  )}
                >
                  <bdi>{platform.handle}</bdi>
                </span>
              </div>

              <div className="flex flex-col gap-4">
                <p className="text-sm tracking-[0.18em] text-violet">كيف يعمل</p>
                <ol className="flex flex-col gap-3">
                  {platform.steps.map((step, index) => (
                    <li key={step} className="flex items-start gap-3">
                      <span className="font-sans text-sm font-bold text-violet/60">
                        <bdi>{toArabicIndex(index + 1)}</bdi>
                      </span>
                      <span className="text-[15px] leading-[1.8] text-neutral">
                        <IsolatedHandles text={step} />
                      </span>
                    </li>
                  ))}
                </ol>
              </div>

              <div className="flex flex-col gap-4">
                <p className="text-sm tracking-[0.18em] text-violet">المميزات</p>
                <ul className="grid grid-cols-1 gap-2.5 sm:grid-cols-2">
                  {platform.features.map((feature) => (
                    <li key={feature} className="flex items-center gap-2 text-[15px] text-neutral">
                      <Check className="size-4 shrink-0 text-violet" />
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>

              {platform.key === "web" ? (
                <ShareButton variant="default" size="lg" className="self-start">
                  {platform.cta}
                  <ArrowUpLeft className="size-4" />
                </ShareButton>
              ) : isLive ? (
                <a
                  href={platform.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={buttonVariants({
                    variant: "default",
                    size: "lg",
                    className: "self-start",
                  })}
                >
                  {platform.cta}
                  <ArrowUpLeft className="size-4" />
                </a>
              ) : (
                <span
                  className={buttonVariants({
                    variant: "default",
                    size: "lg",
                    className: "pointer-events-none self-start opacity-50",
                  })}
                >
                  قريبًا
                </span>
              )}
            </div>

            <div className="order-first flex items-center justify-center rounded-2xl bg-muted/40 p-6 md:order-none md:p-8">
              <div className="w-full max-w-sm">
                <PlatformPreview platform={platform} />
              </div>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
};
