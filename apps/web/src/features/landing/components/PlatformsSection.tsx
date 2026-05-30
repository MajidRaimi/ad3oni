import { ArrowUpLeft } from "lucide-react";
import { cn } from "@/shared/lib/utils";
import { platforms, type Platform } from "../data/platforms";
import { Reveal } from "./Reveal";

const PlatformCard = ({ platform }: { platform: Platform }) => {
  const Icon = platform.icon;
  const isLive = platform.status === "live";

  const inner = (
    <div
      className={cn(
        "group flex h-full flex-col gap-5 rounded-3xl border border-border bg-paper p-8 transition-all",
        isLive
          ? "hover:-translate-y-1 hover:border-violet/40 hover:shadow-violet"
          : "opacity-70",
      )}
    >
      <div className="flex items-center justify-between">
        <span
          className={cn(
            "flex size-14 items-center justify-center rounded-2xl",
            isLive ? "bg-royal text-paper" : "bg-muted text-neutral",
          )}
        >
          <Icon className="size-6" />
        </span>
        {isLive ? (
          <span className="flex items-center gap-2 text-xs text-violet">
            <span className="size-2 rounded-full bg-violet" />
            متاح الآن
          </span>
        ) : (
          <span className="rounded-full bg-muted px-3 py-1 text-xs text-neutral">
            قريبًا
          </span>
        )}
      </div>

      <div className="flex flex-col gap-1">
        <h3 className="font-display text-2xl text-royal">{platform.name}</h3>
        <span dir="ltr" className="self-end font-mono text-xs tracking-wide text-neutral/70">
          <bdi>{platform.handle}</bdi>
        </span>
      </div>

      <p className="text-[15px] leading-[1.9] text-neutral">{platform.description}</p>

      {isLive && (
        <span className="mt-auto flex items-center gap-1 text-sm font-medium text-royal transition-colors group-hover:text-violet">
          افتح
          <ArrowUpLeft className="size-4" />
        </span>
      )}
    </div>
  );

  if (!isLive) {
    return inner;
  }

  return (
    <a
      href={platform.href}
      target="_blank"
      rel="noopener noreferrer"
      className="block h-full rounded-3xl outline-none focus-visible:ring-[3px] focus-visible:ring-ring/50"
    >
      {inner}
    </a>
  );
};

export const PlatformsSection = () => (
  <section id="platforms" className="bg-muted/40 px-6 py-28 md:py-36">
    <div className="mx-auto max-w-6xl">
      <Reveal>
        <div className="mb-16 flex flex-col items-center gap-3 text-center">
          <span className="text-sm tracking-[0.18em] text-violet">أينما كنت</span>
          <h2 className="font-display text-4xl text-royal md:text-5xl">منصّاتنا</h2>
          <p className="max-w-xl text-lg leading-[1.9] text-neutral">
            نذكّرك بالدعاء حيث تقضي يومك، من ديسكورد وإكس إلى الموقع والتطبيقات.
          </p>
        </div>
      </Reveal>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {platforms.map((platform, index) => (
          <Reveal key={platform.key} delay={index * 0.08}>
            <PlatformCard platform={platform} />
          </Reveal>
        ))}
      </div>
    </div>
  </section>
);
