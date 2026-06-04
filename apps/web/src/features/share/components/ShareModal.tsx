"use client";

import { useEffect } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { Check, X } from "lucide-react";
import { useLockBodyScroll } from "@/shared/hooks/useLockBodyScroll";
import { useMediaQuery } from "@/shared/hooks/useMediaQuery";
import { Button } from "@/shared/ui/button";
import { useShareModal } from "../store";
import { SharePrayerForm } from "./SharePrayerForm";

type SharePanelProps = {
  onClose: () => void;
  isDesktop: boolean;
  reduce: boolean;
};

const SharePanel = ({ onClose, isDesktop, reduce }: SharePanelProps) => {
  useLockBodyScroll(true);
  const view = useShareModal((state) => state.view);
  const reset = useShareModal((state) => state.reset);

  useEffect(() => {
    const previouslyFocused = document.activeElement as HTMLElement | null;

    const handleKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleKey);

    return () => {
      window.removeEventListener("keydown", handleKey);
      previouslyFocused?.focus?.();
    };
  }, [onClose]);

  const panelMotion = reduce
    ? { initial: { opacity: 0 }, animate: { opacity: 1 }, exit: { opacity: 0 } }
    : isDesktop
      ? {
          initial: { opacity: 0, scale: 0.96, y: 8 },
          animate: { opacity: 1, scale: 1, y: 0 },
          exit: { opacity: 0, scale: 0.96, y: 8 },
        }
      : { initial: { y: "100%" }, animate: { y: 0 }, exit: { y: "100%" } };

  const isSuccess = view === "success";

  return (
    <motion.div
      className="fixed inset-0 z-[100] flex items-end justify-center md:items-center md:p-6"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.2 }}
    >
      <button
        type="button"
        aria-hidden
        tabIndex={-1}
        onClick={onClose}
        className="absolute inset-0 bg-night/50 backdrop-blur-sm"
      />

      <motion.div
        role="dialog"
        aria-modal="true"
        aria-labelledby="share-modal-title"
        {...panelMotion}
        transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
        className="relative flex max-h-[90vh] w-full flex-col overflow-y-auto rounded-t-3xl bg-paper p-6 pb-8 md:max-w-md md:rounded-3xl md:p-8"
      >
        <div className="mx-auto mb-5 h-1.5 w-12 shrink-0 rounded-full bg-neutral/20 md:hidden" />

        <div className="flex flex-col gap-2">
          <div className="flex items-center justify-between gap-4">
            <h2 id="share-modal-title" className="font-display text-2xl text-royal">
              {isSuccess ? "جزاك الله خيرًا" : "شارك دعاءك"}
            </h2>
            <button
              type="button"
              onClick={onClose}
              aria-label="إغلاق"
              className="-me-1 flex size-9 shrink-0 items-center justify-center rounded-full text-neutral transition-colors hover:bg-muted hover:text-royal"
            >
              <X className="size-5" />
            </button>
          </div>
          {!isSuccess && (
            <p className="text-sm leading-[1.8] text-neutral">
              اكتب دعاءً صادقًا، وسنشاركه ليصل غيرك فتُكتب لك أجوره بإذن الله.
            </p>
          )}
        </div>

        {isSuccess ? (
          <div className="mt-6 flex flex-col gap-7">
            <div className="flex flex-col items-center gap-4 text-center">
              <span className="flex size-14 items-center justify-center rounded-full bg-violet/10 text-violet">
                <Check className="size-7" />
              </span>
              <p className="text-sm leading-[1.9] text-neutral">
                وصلنا دعاؤك. سيظهر للجميع بعد المراجعة بإذن الله، فتُكتب لك أجوره كلما
                دعا به أحد.
              </p>
            </div>
            <div className="flex flex-col gap-3">
              <Button type="button" size="lg" onClick={reset}>
                شارك دعاءً آخر
              </Button>
              <button
                type="button"
                onClick={onClose}
                className="text-sm text-neutral transition-colors hover:text-royal"
              >
                إغلاق
              </button>
            </div>
          </div>
        ) : (
          <div className="mt-6">
            <SharePrayerForm />
          </div>
        )}
      </motion.div>
    </motion.div>
  );
};

export const ShareModal = () => {
  const isOpen = useShareModal((state) => state.isOpen);
  const close = useShareModal((state) => state.close);
  const isDesktop = useMediaQuery("(min-width: 768px)");
  const reduce = useReducedMotion();

  return (
    <AnimatePresence>
      {isOpen && (
        <SharePanel onClose={close} isDesktop={isDesktop} reduce={Boolean(reduce)} />
      )}
    </AnimatePresence>
  );
};
