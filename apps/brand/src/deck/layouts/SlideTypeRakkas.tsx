import { SlideHeader } from "../primitives"

export const SlideTypeRakkas = () => (
  <div className="night-bg absolute inset-0 flex flex-col px-[120px] pt-[184px] pb-[148px] text-paper" dir="rtl">
    <SlideHeader no={4} ar="رقعة" en="Rakkas" title="«رقعة» · خط العناوين" titleEn="Rakkas · Display" light />

    <div className="mt-8 grid flex-1 grid-cols-[1fr_1.3fr] gap-16">
      <div className="flex items-center justify-center">
        <span className="font-display text-[400px] leading-none text-lilac">ع</span>
      </div>

      <div className="flex flex-col justify-center gap-10">
        <p className="m-0 font-display text-[80px] leading-[1.35] text-paper">
          ادْعُونِي أَسْتَجِبْ لَكُمْ
        </p>
        <p className="m-0 font-display text-[44px] leading-[1.5] text-paper/55" dir="ltr">
          0123456789
        </p>
        <div className="flex flex-wrap gap-3">
          {["العناوين الكبيرة", "الكلمة علامة", "الأرقام البطولية", "الاقتباسات"].map((u) => (
            <span key={u} className="rounded-full border border-paper/20 bg-paper/[0.06] px-5 py-2 text-[17px] text-paper/80">
              {u}
            </span>
          ))}
        </div>
        <p className="m-0 text-[18px] leading-[1.7] text-paper/45">
          لا يُستعمل للنصوص الطويلة أو الأحجام الصغيرة. اتركه للعناوين حيث يتنفس.
        </p>
      </div>
    </div>
  </div>
)
