import { CopyButton } from "../CopyButton"
import { colorTokens } from "../tokens"
import { MonoTag, SlideBody, SlideHeader } from "../primitives"

export const SlideColorPalette = () => (
  <SlideBody>
    <SlideHeader no={3} ar="اللوحة" en="Palette" title="لوحة الألوان" titleEn="The Palette" />

    <div className="mt-12 grid flex-1 grid-cols-3 gap-7">
      {colorTokens.map((c) => (
        <div
          key={c.name}
          className="flex flex-col justify-end overflow-hidden rounded-2xl border border-royal/10 shadow-[0_14px_36px_rgba(7,1,42,0.08)]"
          style={{ background: c.hex }}
        >
          <div className="flex h-[150px] items-start justify-between p-6" style={{ color: c.onLight ? "#ffffff" : "#1a1330" }}>
            <span className="text-[26px] font-bold">{c.ar}</span>
            <CopyButton value={c.hex} className={c.onLight ? "text-white/70 hover:text-white" : "text-ink/50 hover:text-ink"} />
          </div>
          <div className="flex flex-col gap-1 bg-white px-6 py-5">
            <div className="flex items-baseline justify-between">
              <span className="text-[18px] font-bold text-royal">{c.name}</span>
              <MonoTag className="text-neutral/55 uppercase">{c.hex}</MonoTag>
            </div>
            <div className="flex items-baseline justify-between">
              <span className="text-[14px] text-neutral/60">{c.role}</span>
              <MonoTag className="text-[11px] text-neutral/40">rgb({c.rgb})</MonoTag>
            </div>
          </div>
        </div>
      ))}
    </div>
  </SlideBody>
)
