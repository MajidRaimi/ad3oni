import { SlideBody, SlideHeader } from "../primitives"

const scale = [
  { name: "Display", ar: "ادْعُونِي", px: 76, lh: "1.1", weight: "Rakkas", font: "font-display", cls: "text-royal" },
  { name: "H1", ar: "عنوان رئيسي", px: 52, lh: "1.2", weight: "Bold 700", font: "font-sans font-bold", cls: "text-royal" },
  { name: "H2", ar: "عنوان فرعي", px: 38, lh: "1.3", weight: "Bold 700", font: "font-sans font-bold", cls: "text-royal" },
  { name: "Body L", ar: "نص أساسي كبير", px: 26, lh: "1.7", weight: "Regular 400", font: "font-sans", cls: "text-neutral" },
  { name: "Body", ar: "نص أساسي", px: 20, lh: "1.7", weight: "Regular 400", font: "font-sans", cls: "text-neutral" },
  { name: "Caption", ar: "تسمية صغيرة", px: 15, lh: "1.5", weight: "Medium 500", font: "font-sans font-medium", cls: "text-neutral/70" },
]

export const SlideTypeScale = () => (
  <SlideBody>
    <SlideHeader no={4} ar="المقياس" en="Scale" title="مقياس الخط والتسلسل" titleEn="Type Scale" />

    <div className="mt-10 flex flex-1 flex-col justify-center divide-y divide-royal/8">
      {scale.map((s) => (
        <div key={s.name} className="flex items-baseline justify-between gap-8 py-4">
          <span className={`${s.font} ${s.cls} truncate`} style={{ fontSize: s.px, lineHeight: s.lh }}>
            {s.ar}
          </span>
          <div className="flex shrink-0 items-baseline gap-6">
            <span className="w-[90px] text-[16px] font-bold text-royal">{s.name}</span>
            <span dir="ltr" className="w-[110px] font-mono text-[13px] text-neutral/55">{s.px}px</span>
            <span dir="ltr" className="w-[90px] font-mono text-[13px] text-neutral/45">lh {s.lh}</span>
            <span dir="ltr" className="w-[120px] font-mono text-[12px] text-neutral/45 uppercase">{s.weight}</span>
          </div>
        </div>
      ))}
    </div>
  </SlideBody>
)
