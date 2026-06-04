"use client";

import { ChevronDown } from "lucide-react";
import { motion, useReducedMotion, type Variants } from "motion/react";
import { useQuery } from "@tanstack/react-query";
import { buttonVariants } from "@/shared/ui/button";
import { randomPrayerQueryOptions } from "@/features/prayers/queries";
import { dailyPrayer } from "../data/prayer";
import { BracePrayer } from "./BracePrayer";

const container: Variants = {
  hidden: {},
  show: {
    transition: { staggerChildren: 0.12, delayChildren: 0.1 },
  },
};

const item: Variants = {
  hidden: { opacity: 0, y: 24 },
  show: { opacity: 1, y: 0, transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] } },
};

export const Hero = () => {
  const reduceMotion = useReducedMotion();
  const { data: prayer } = useQuery(randomPrayerQueryOptions());

  const prayerText = prayer?.textDiacritized ?? prayer?.text ?? dailyPrayer.text;
  const prayerLabel = prayer?.category?.name ?? dailyPrayer.attribution;

  return (
    <section className="dotted-bg relative flex min-h-svh items-center overflow-hidden text-paper">
      <div className="pointer-events-none absolute inset-0 bg-gradient-to-b from-royal-deep/30 via-transparent to-royal-deep/60" />

      <motion.div
        variants={container}
        initial={reduceMotion ? false : "hidden"}
        animate="show"
        className="relative mx-auto flex w-full max-w-5xl flex-col items-center gap-10 px-6 py-32 text-center"
      >
        <motion.div
          variants={item}
          className="flex items-center gap-4 text-paper/70"
        >
          <span className="h-px w-10 bg-paper/30" />
          <span className="text-sm tracking-[0.18em]">دعاء اليوم</span>
          <span className="h-px w-10 bg-paper/30" />
        </motion.div>

        <motion.div variants={item}>
          <BracePrayer>
            <p className="font-display text-4xl text-paper sm:text-5xl md:text-6xl">
              {prayerText}
            </p>
          </BracePrayer>
        </motion.div>

        <motion.p variants={item} className="text-sm text-paper/55">
          <bdi>{prayerLabel}</bdi>
        </motion.p>

        <motion.div
          variants={item}
          className="flex flex-col items-center gap-3 sm:flex-row"
        >
          <a href="#share" className={buttonVariants({ variant: "paper", size: "lg" })}>
            شاركنا دعاءك
          </a>
          <a
            href="#platforms"
            className={buttonVariants({ variant: "outline", size: "lg", className: "text-paper" })}
          >
            تصفّح منصّاتنا
          </a>
        </motion.div>
      </motion.div>

      <motion.a
        href="#about"
        aria-label="اكتشف المزيد"
        initial={reduceMotion ? false : { opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.1, duration: 0.8 }}
        className="absolute bottom-8 left-1/2 flex -translate-x-1/2 flex-col items-center gap-1 text-paper/60 transition-colors hover:text-paper"
      >
        <span className="text-xs tracking-[0.16em]">اكتشف المزيد</span>
        <motion.span
          animate={reduceMotion ? undefined : { y: [0, 6, 0] }}
          transition={{ repeat: Infinity, duration: 1.8, ease: "easeInOut" }}
        >
          <ChevronDown size={20} />
        </motion.span>
      </motion.a>
    </section>
  );
};
