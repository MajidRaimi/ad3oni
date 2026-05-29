import { ArrowLeft } from "lucide-react"
import { SlideBody, SlideHeader } from "../primitives"

const layers = [
  {
    title: "أولية",
    en: "Primitive",
    color: "bg-royal/[0.04] border-royal/12",
    items: ["--color-royal: #2b0d69", "--color-violet: #6d49d6", "--color-lilac: #a98ee6", "--space-4: 16px"],
  },
  {
    title: "دلالية",
    en: "Semantic",
    color: "bg-violet/[0.1] border-violet/35",
    items: ["--primary: royal", "--accent: violet", "--ring: violet", "--background: paper"],
  },
  {
    title: "مكوّن",
    en: "Component",
    color: "bg-lilac/[0.18] border-lilac/45",
    items: ["button/bg: primary", "card/border: border", "input/ring: ring", "badge/bg: secondary"],
  },
]

export const SlideTokens = () => (
  <SlideBody>
    <SlideHeader no={6} ar="الرموز" en="Tokens" title="رموز التصميم · الطبقات" titleEn="Design Tokens" />

    <div className="mt-12 flex flex-1 items-stretch gap-6" dir="rtl">
      {layers.map((l, i) => (
        <div key={l.en} className="flex flex-1 items-center gap-6">
          <div className={`flex flex-1 flex-col gap-5 rounded-3xl border p-9 ${l.color}`}>
            <div className="flex items-baseline justify-between">
              <span className="text-[24px] font-bold text-royal">{l.title}</span>
              <span dir="ltr" className="font-mono text-[12px] tracking-[0.2em] text-neutral/45 uppercase">{l.en}</span>
            </div>
            <div className="flex flex-col gap-3">
              {l.items.map((it) => (
                <span key={it} dir="ltr" className="rounded-lg bg-white/70 px-4 py-2.5 font-mono text-[14px] text-royal">
                  {it}
                </span>
              ))}
            </div>
          </div>
          {i < layers.length - 1 && <ArrowLeft size={32} className="shrink-0 text-violet" />}
        </div>
      ))}
    </div>

    <p className="mt-8 text-center text-[19px] text-neutral/60">
      كل الرموز تعيش في <span dir="ltr" className="font-mono text-royal">@theme</span> داخل Tailwind v4، فتتغير الهوية كلها من مكان واحد.
    </p>
  </SlideBody>
)
