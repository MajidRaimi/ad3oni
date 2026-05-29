import { SlideBody, SlideHeader } from "../primitives"

const mix = [
  { hex: "#2b0d69", w: "58%", ar: "أرجواني" },
  { hex: "#ffffff", w: "22%", ar: "ورقي" },
  { hex: "#6d49d6", w: "12%", ar: "بنفسجي" },
  { hex: "#a98ee6", w: "8%", ar: "ليلكي" },
]

const pairs = [
  { fg: "#ffffff", bg: "#2b0d69", label: "أبيض على أرجواني", ratio: "12.8", grade: "AAA" },
  { fg: "#2b0d69", bg: "#a98ee6", label: "أرجواني على ليلكي", ratio: "7.1", grade: "AAA" },
  { fg: "#a98ee6", bg: "#0c0626", label: "ليلكي على ليلي", ratio: "7.0", grade: "AAA" },
  { fg: "#ffffff", bg: "#6d49d6", label: "أبيض على بنفسجي", ratio: "5.9", grade: "AA" },
  { fg: "#1a1330", bg: "#ffffff", label: "حبري على أبيض", ratio: "17.5", grade: "AAA" },
  { fg: "#a98ee6", bg: "#2b0d69", label: "ليلكي على أرجواني", ratio: "5.6", grade: "AA" },
]

export const SlideColorRatios = () => (
  <SlideBody>
    <SlideHeader no={3} ar="النسب والتباين" en="Ratios" title="النسب والتباين" titleEn="Ratios & Contrast" />

    <div className="mt-12 flex flex-1 flex-col gap-9">
      <div className="flex flex-col gap-4">
        <span className="text-[19px] font-bold text-royal">النسب المقترحة للمزج</span>
        <div className="flex h-[110px] overflow-hidden rounded-2xl shadow-[0_14px_36px_rgba(7,1,42,0.1)]">
          {mix.map((m) => (
            <div key={m.ar} className="flex items-end justify-center pb-3" style={{ background: m.hex, width: m.w }}>
              <span className="font-mono text-[13px]" style={{ color: m.hex === "#ffffff" || m.hex === "#a98ee6" ? "#1c0847" : "#ffffff" }}>
                {m.w}
              </span>
            </div>
          ))}
        </div>
      </div>

      <div className="flex flex-col gap-4">
        <span className="text-[19px] font-bold text-royal">تباين النص · WCAG</span>
        <div className="grid grid-cols-3 gap-5">
          {pairs.map((p) => (
            <div key={p.label} className="overflow-hidden rounded-2xl border border-royal/10">
              <div className="flex h-[96px] items-center justify-center" style={{ background: p.bg, color: p.fg }}>
                <span className="text-[26px] font-bold">دعاء اليوم</span>
              </div>
              <div className="flex items-center justify-between bg-white px-5 py-3">
                <span className="text-[15px] text-neutral/70">{p.label}</span>
                <div className="flex items-center gap-2">
                  <span dir="ltr" className="font-mono text-[13px] text-neutral/55">{p.ratio}:1</span>
                  <span className={`rounded-md px-2 py-0.5 font-mono text-[11px] font-bold ${p.grade === "AAA" ? "bg-violet/15 text-violet" : "bg-lilac/25 text-royal"}`}>
                    {p.grade}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  </SlideBody>
)
