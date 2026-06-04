"use client";

import { useQuery } from "@tanstack/react-query";
import { cn } from "@/shared/lib/utils";
import { prayersQueryOptions } from "@/features/prayers/queries";
import type { Prayer } from "@/features/prayers/types";
import { communityPrayers, type CommunityPrayer } from "../data/communityPrayers";
import { PrayerCard } from "./PrayerCard";

const toCard = (prayer: Prayer): CommunityPrayer => ({
  id: prayer.id,
  text: prayer.textDiacritized ?? prayer.text,
  category: prayer.category?.name ?? "",
});

const MarqueeRow = ({
  prayers,
  reverse,
}: {
  prayers: CommunityPrayer[];
  reverse?: boolean;
}) => (
  <div className="marquee-mask group overflow-x-clip overflow-y-visible py-3 motion-reduce:overflow-x-auto">
    <div
      className={cn(
        "flex w-max group-hover:[animation-play-state:paused] motion-reduce:animate-none",
        reverse ? "animate-marquee-reverse" : "animate-marquee",
      )}
    >
      {[...prayers, ...prayers].map((prayer, index) => (
        <div
          key={`${prayer.id}-${index}`}
          aria-hidden={index >= prayers.length}
          className="w-[240px] shrink-0 px-3 md:w-[280px]"
        >
          <PrayerCard prayer={prayer} />
        </div>
      ))}
    </div>
  </div>
);

export const PrayerMarquee = () => {
  const { data } = useQuery(
    prayersQueryOptions({ perPage: 14, sort: "-created" }),
  );

  const items = data?.items.length ? data.items.map(toCard) : communityPrayers;
  const rowOne = items;
  const rowTwo = [...items.slice(7), ...items.slice(0, 7)];

  return (
    <div dir="ltr" className="flex flex-col gap-5">
      <MarqueeRow prayers={rowOne} />
      <MarqueeRow prayers={rowTwo} reverse />
    </div>
  );
};
