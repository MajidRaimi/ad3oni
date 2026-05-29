import { royalRamp } from "../tokens"
import { SlideHeader } from "../primitives"

export const SlideColorRoyal = () => (
  <div className="absolute inset-0 flex flex-col bg-royal px-[120px] pt-[184px] pb-[148px] text-paper" dir="rtl">
    <SlideHeader no={3} ar="الأرجواني" en="Royal" title="الأرجواني · اللون الأساسي" titleEn="Royal · Primary" light />

    <div className="mt-12 grid flex-1 grid-cols-[1fr_1.1fr] gap-16">
      <div className="flex flex-col justify-center gap-6">
        <span className="font-mono text-[88px] leading-none font-semibold tracking-tight text-lilac">#2b0d69</span>
        <span dir="ltr" className="font-mono text-[18px] tracking-[0.2em] text-paper/55 uppercase">rgb(43, 13, 105)</span>
        <p className="m-0 mt-3 max-w-[560px] text-[24px] leading-[1.85] text-paper/70">
          الأرجواني هو صوت العلامة البصري: الأزرار الأساسية، العناوين، والكلمة علامة. عميق، هادئ، وموقّر،
          يحمل الطابع الروحي للمنصة.
        </p>
      </div>

      <div className="flex flex-col justify-center gap-7">
        <div className="overflow-hidden rounded-2xl">
          <div className="flex h-[180px]">
            {royalRamp.map((r) => (
              <div key={r.step} className="flex flex-1 items-end justify-center pb-4" style={{ background: r.hex }}>
                <span
                  className="font-mono text-[12px] tracking-[0.08em]"
                  style={{ color: ["100", "300", "400"].includes(r.step) ? "#1c0847" : "#ffffff" }}
                >
                  {r.step}
                </span>
              </div>
            ))}
          </div>
        </div>
        <div className="flex flex-wrap gap-3">
          {["الأزرار", "العناوين", "الكلمة علامة", "الأيقونات النشطة", "الحدود البارزة"].map((u) => (
            <span key={u} className="rounded-full border border-paper/20 bg-paper/[0.06] px-5 py-2 text-[17px] text-paper/80">
              {u}
            </span>
          ))}
        </div>
      </div>
    </div>
  </div>
)
