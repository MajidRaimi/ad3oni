import { Heart, MessageCircle, Repeat2 } from "lucide-react";
import type { Platform } from "../data/platforms";
import { DiscordIcon, XIcon } from "./icons";

const samplePrayer = "اللهم اشرح صدري، ويسّر أمري، وارزقني طمأنينة.";

const TweetFrame = () => (
  <div className="rounded-2xl border border-border bg-paper p-5">
    <div className="flex items-center gap-3">
      <span className="flex size-10 items-center justify-center rounded-full bg-royal text-paper">
        <XIcon className="size-4" />
      </span>
      <div className="leading-tight">
        <p className="font-display text-royal">ادْعُونِي</p>
        <p className="text-left font-mono text-xs text-neutral">
          <bdi>@ad3oni_</bdi>
        </p>
      </div>
    </div>
    <p className="mt-4 text-[15px] leading-[1.9] text-ink">{samplePrayer}</p>
    <div dir="ltr" className="mt-5 flex items-center gap-8 text-neutral/45">
      <MessageCircle className="size-4" />
      <Repeat2 className="size-4" />
      <Heart className="size-4" />
    </div>
  </div>
);

const DiscordFrame = () => (
  <div className="rounded-2xl border border-border bg-paper p-5">
    <div className="flex items-center gap-3">
      <span className="flex size-10 items-center justify-center rounded-full bg-violet text-paper">
        <DiscordIcon className="size-5" />
      </span>
      <p className="flex items-center gap-2 font-display text-royal">
        ادْعُونِي
        <span className="rounded bg-violet/15 px-1.5 py-0.5 font-sans text-[10px] tracking-wide text-violet">
          BOT
        </span>
      </p>
    </div>
    <div className="mt-3 rounded-xl border-r-2 border-violet bg-muted/50 p-4 text-[15px] leading-[1.9] text-ink">
      {samplePrayer}
    </div>
  </div>
);

const WebFrame = () => (
  <div className="overflow-hidden rounded-2xl border border-border bg-paper">
    <div dir="ltr" className="relative flex items-center border-b border-border px-4 py-3">
      <div className="flex items-center gap-1.5">
        <span className="size-2.5 rounded-full bg-neutral/25" />
        <span className="size-2.5 rounded-full bg-neutral/25" />
        <span className="size-2.5 rounded-full bg-neutral/25" />
      </div>
      <span className="absolute left-1/2 -translate-x-1/2 rounded-md bg-muted px-3 py-1 font-mono text-xs text-neutral">
        ad3oni.com
      </span>
    </div>
    <div className="px-6 py-8 text-center">
      <p className="text-xs tracking-wide text-violet">دعاء اليوم</p>
      <p className="mt-3 font-naskh text-lg leading-[1.95] text-royal">{samplePrayer}</p>
    </div>
  </div>
);

const NotificationFrame = ({ platform }: { platform: Platform }) => {
  const Icon = platform.icon;
  return (
    <div className="rounded-2xl border border-border bg-paper p-5">
      <div className="flex items-center gap-3">
        <span className="flex size-10 items-center justify-center rounded-xl bg-royal text-paper">
          <Icon className="size-5" />
        </span>
        <div className="flex-1">
          <div className="flex items-center justify-between">
            <p className="font-display text-sm text-royal">ادْعُونِي</p>
            <span className="font-sans text-[10px] text-neutral">الآن</span>
          </div>
          <p className="text-xs text-neutral">حان وقت دعاء اليوم</p>
        </div>
      </div>
      <p className="mt-3 text-[15px] leading-[1.85] text-ink">{samplePrayer}</p>
    </div>
  );
};

export const PlatformPreview = ({ platform }: { platform: Platform }) => {
  switch (platform.key) {
    case "x":
      return <TweetFrame />;
    case "discord":
      return <DiscordFrame />;
    case "web":
      return <WebFrame />;
    default:
      return <NotificationFrame platform={platform} />;
  }
};
