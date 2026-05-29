import { radiusTokens, shadowTokens } from "../tokens"
import { SlideBody, SlideHeader } from "../primitives"

export const SlideRadius = () => (
  <SlideBody>
    <SlideHeader no={6} ar="الحواف والظل" en="Radius" title="نصف القطر والارتفاع" titleEn="Radius & Elevation" />

    <div className="mt-12 grid flex-1 grid-cols-2 gap-16">
      <div className="flex flex-col gap-5">
        <span className="text-[19px] font-bold text-royal">نصف القطر</span>
        <div className="grid grid-cols-3 gap-5">
          {radiusTokens.map((r) => (
            <div key={r.name} className="flex flex-col items-center gap-3">
              <div
                className="h-[110px] w-full border-2 border-royal bg-royal/[0.06]"
                style={{ borderRadius: r.px === "999px" ? "999px" : r.px }}
              />
              <div className="flex items-baseline gap-2">
                <span className="text-[16px] font-bold text-royal">{r.name}</span>
                <span dir="ltr" className="font-mono text-[12px] text-neutral/50">{r.px}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex flex-col gap-5">
        <span className="text-[19px] font-bold text-royal">الارتفاع والظل</span>
        <div className="grid grid-cols-1 gap-4">
          {shadowTokens.map((s) => (
            <div key={s.name} className="flex items-center gap-6">
              <div className="h-[58px] w-[58px] shrink-0 rounded-xl bg-white" style={{ boxShadow: s.value }} />
              <div className="flex flex-1 items-baseline justify-between border-b border-royal/8 pb-3">
                <span className="text-[17px] font-bold text-royal">shadow-{s.name}</span>
                <span dir="ltr" className="font-mono text-[12px] text-neutral/50">{s.value}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  </SlideBody>
)
