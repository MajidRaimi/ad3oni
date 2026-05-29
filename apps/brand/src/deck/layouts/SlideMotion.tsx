import { motionTokens, easeBrand } from "../tokens"
import { SlideHeader } from "../primitives"

const states = [
  { ar: "استراحة", cls: "bg-lilac text-night" },
  { ar: "تحويم", cls: "bg-lilac text-night -translate-y-1 shadow-[0_16px_40px_rgba(109,73,214,0.4)]" },
  { ar: "تركيز", cls: "bg-lilac text-night ring-4 ring-violet ring-offset-2 ring-offset-night" },
  { ar: "معطّل", cls: "bg-lilac/35 text-night/50" },
]

export const SlideMotion = () => (
  <div className="night-bg absolute inset-0 flex flex-col px-[120px] pt-[184px] pb-[148px] text-paper" dir="rtl">
    <SlideHeader no={6} ar="الحركة والحالات" en="Motion" title="الحركة والحالات" titleEn="Motion & States" />

    <div className="mt-10 grid flex-1 grid-cols-[1fr_1fr] gap-16">
      <div className="flex flex-col justify-center gap-9">
        <div className="flex flex-col gap-4">
          <span className="text-[19px] font-bold text-lilac">المدة</span>
          <div className="flex gap-4">
            {motionTokens.map((m) => (
              <div key={m.name} className="flex flex-1 flex-col items-center gap-2 rounded-2xl border border-paper/15 bg-paper/[0.05] py-6">
                <span className="font-mono text-[28px] font-semibold text-paper">{m.value}</span>
                <span className="text-[15px] text-paper/55">{m.name}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="flex flex-col gap-4">
          <span className="text-[19px] font-bold text-lilac">منحنى التسارع</span>
          <div className="flex items-center gap-6 rounded-2xl border border-paper/15 bg-paper/[0.05] p-6">
            <svg width={120} height={120} viewBox="0 0 100 100" className="shrink-0">
              <line x1="0" y1="100" x2="100" y2="100" stroke="rgba(255,255,255,0.2)" />
              <line x1="0" y1="100" x2="0" y2="0" stroke="rgba(255,255,255,0.2)" />
              <path d="M0,100 C19,0 22,0 100,0" fill="none" stroke="#a98ee6" strokeWidth="3" />
            </svg>
            <div className="flex flex-col gap-1">
              <span className="text-[17px] font-bold text-paper">ease-brand</span>
              <span dir="ltr" className="font-mono text-[13px] text-paper/55">{easeBrand}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="flex flex-col justify-center gap-4">
        <span className="text-[19px] font-bold text-lilac">الحالات التفاعلية</span>
        <div className="grid grid-cols-2 gap-6">
          {states.map((s) => (
            <div key={s.ar} className="flex flex-col items-center gap-4 rounded-2xl border border-paper/12 bg-paper/[0.04] py-10">
              <span className={`inline-flex h-12 items-center justify-center rounded-full px-8 text-[18px] font-bold transition-all ${s.cls}`}>
                ادعُ الآن
              </span>
              <span className="text-[16px] text-paper/60">{s.ar}</span>
            </div>
          ))}
        </div>
        <p className="m-0 mt-2 text-[16px] leading-[1.7] text-paper/45">
          كل الحركات تتوقف مع <span dir="ltr" className="font-mono">prefers-reduced-motion</span>.
        </p>
      </div>
    </div>
  </div>
)
