import { Wordmark } from "../Wordmark"
import { SlideBody, SlideHeader } from "../primitives"

type Variant = {
  bg: string
  color: Parameters<typeof Wordmark>[0]["color"]
  ar: string
  en: string
  border?: boolean
}

const variants: Array<Variant> = [
  { bg: "#ffffff", color: "royal", ar: "أرجواني على أبيض", en: "Royal on white", border: true },
  { bg: "#2b0d69", color: "paper", ar: "أبيض على أرجواني", en: "White on royal" },
  { bg: "#0c0626", color: "lilac", ar: "ليلكي على ليلي", en: "Lilac on night" },
  { bg: "#6d49d6", color: "paper", ar: "أبيض على بنفسجي", en: "White on violet" },
  { bg: "#a98ee6", color: "royal", ar: "أرجواني على ليلكي", en: "Royal on lilac" },
  { bg: "#1a1330", color: "paper", ar: "أبيض صلب", en: "Mono white", border: true },
]

export const SlideLogoVariants = () => (
  <SlideBody>
    <SlideHeader no={2} ar="الأشكال" en="Variants" title="أشكال الألوان والخلفيات" titleEn="Color & Background Variants" />

    <div className="mt-12 grid flex-1 grid-cols-3 gap-7">
      {variants.map((v) => (
        <div key={v.en} className="flex flex-col gap-3">
          <div
            className="flex flex-1 items-center justify-center rounded-2xl"
            style={{ background: v.bg, border: v.border ? "1px solid rgba(7,1,42,0.12)" : "none" }}
          >
            <Wordmark color={v.color} size={68} />
          </div>
          <div className="flex items-baseline justify-between px-1">
            <span className="text-[16px] text-royal">{v.ar}</span>
            <span dir="ltr" className="font-mono text-[11px] tracking-[0.16em] text-neutral/45 uppercase">{v.en}</span>
          </div>
        </div>
      ))}
    </div>
  </SlideBody>
)
