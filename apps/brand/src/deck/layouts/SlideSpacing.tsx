import { spacingTokens } from "../tokens"
import { SlideHeader } from "../primitives"

export const SlideSpacing = () => (
  <div className="night-bg absolute inset-0 flex flex-col px-[120px] pt-[184px] pb-[148px] text-paper" dir="rtl">
    <SlideHeader no={6} ar="التباعد والشبكة" en="Spacing" title="التباعد والشبكة" titleEn="Spacing & Grid" />

    <div className="mt-10 grid flex-1 grid-cols-[1fr_1fr] gap-16">
      <div className="flex flex-col justify-center gap-4">
        <span className="text-[19px] font-bold text-lilac">سلم 8pt</span>
        <div className="flex flex-col gap-3">
          {spacingTokens.map((s) => (
            <div key={s} className="flex items-center gap-5">
              <span dir="ltr" className="w-12 shrink-0 font-mono text-[14px] text-paper/55">{s}</span>
              <div className="h-5 rounded-sm bg-lilac" style={{ width: `${Number(s) * 1.8}px` }} />
            </div>
          ))}
        </div>
      </div>

      <div className="flex flex-col justify-center gap-4">
        <span className="text-[19px] font-bold text-lilac">شبكة 12 عمودا</span>
        <div className="grid grid-cols-12 gap-2">
          {Array.from({ length: 12 }).map((_, i) => (
            <div key={i} className="flex h-[260px] items-end justify-center rounded-md bg-paper/[0.07] pb-3">
              <span className="font-mono text-[12px] text-paper/40">{i + 1}</span>
            </div>
          ))}
        </div>
        <p className="m-0 text-[17px] leading-[1.7] text-paper/55">
          أقصى عرض للحاوية 1200px، هوامش 24px على الجوال و64px على سطح المكتب.
        </p>
      </div>
    </div>
  </div>
)
