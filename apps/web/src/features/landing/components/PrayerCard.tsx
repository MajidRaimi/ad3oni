import type { CommunityPrayer } from "../data/communityPrayers";

type PrayerCardProps = {
  prayer: CommunityPrayer;
};

export const PrayerCard = ({ prayer }: PrayerCardProps) => (
  <article
    dir="rtl"
    className="flex h-full flex-col gap-3 rounded-2xl border border-border bg-paper p-6"
  >
    {prayer.category ? (
      <span className="self-start rounded-full bg-muted px-2.5 py-1 text-[11px] text-violet">
        {prayer.category}
      </span>
    ) : null}
    <p className="font-sans text-sm leading-[1.85] text-royal">{prayer.text}</p>
  </article>
);
