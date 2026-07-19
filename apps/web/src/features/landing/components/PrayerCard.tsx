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
    <p className="font-naskh text-[15px] leading-[2] text-royal">{prayer.text}</p>
    {prayer.source ? (
      <span className="mt-auto text-[11px] text-neutral/70">
        <bdi>{prayer.source}</bdi>
      </span>
    ) : null}
  </article>
);
