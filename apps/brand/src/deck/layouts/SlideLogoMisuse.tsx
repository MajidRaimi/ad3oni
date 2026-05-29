import { X } from "lucide-react"
import { Wordmark } from "../Wordmark"
import { SlideBody, SlideHeader } from "../primitives"

const misuses = [
  { ar: "لا تمطّط أو تشوّه", en: "Don't stretch", style: { transform: "scaleX(1.6)" } },
  { ar: "لا تعد التلوين", en: "Don't recolor", color: "violet" as const },
  { ar: "لا تدر", en: "Don't rotate", style: { transform: "rotate(-12deg)" } },
  { ar: "لا تضف ظلا", en: "Don't add shadow", style: { filter: "drop-shadow(4px 6px 3px rgba(0,0,0,0.45))" } },
  { ar: "لا تضعه على خلفية مزدحمة", en: "Don't clutter", busy: true },
  { ar: "لا تخفض التباين", en: "Don't low-contrast", faint: true },
]

export const SlideLogoMisuse = () => (
  <SlideBody>
    <SlideHeader no={2} ar="سوء الاستخدام" en="Misuse" title="سوء الاستخدام · الممنوعات" titleEn="Misuse" />

    <div className="mt-12 grid flex-1 grid-cols-3 gap-7">
      {misuses.map((m) => (
        <div key={m.en} className="flex flex-col gap-3">
          <div
            className="relative flex flex-1 items-center justify-center overflow-hidden rounded-2xl border border-royal/10 bg-royal/[0.03]"
            style={m.busy ? { backgroundImage: "repeating-linear-gradient(45deg,#2b0d69,#2b0d69 10px,#6d49d6 10px,#6d49d6 20px)" } : undefined}
          >
            <span style={m.style}>
              <Wordmark color={m.color ?? (m.faint ? "royal" : "royal")} size={62} className={m.faint ? "opacity-15" : ""} />
            </span>
            <span className="absolute right-4 top-4 flex h-9 w-9 items-center justify-center rounded-full bg-destructive text-white">
              <X size={18} strokeWidth={3} />
            </span>
          </div>
          <div className="flex items-baseline justify-between px-1">
            <span className="text-[16px] font-medium text-destructive">{m.ar}</span>
            <span dir="ltr" className="font-mono text-[11px] tracking-[0.16em] text-neutral/40 uppercase">{m.en}</span>
          </div>
        </div>
      ))}
    </div>
  </SlideBody>
)
