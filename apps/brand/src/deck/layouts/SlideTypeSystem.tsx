import { SlideBody, SlideHeader } from "../primitives"

export const SlideTypeSystem = () => (
  <SlideBody>
    <SlideHeader no={4} ar="النظام" en="System" title="خطان · نظام واحد" titleEn="Two Fonts, One System" />

    <div className="mt-12 grid flex-1 grid-cols-2 gap-8">
      <div className="flex flex-col justify-between rounded-3xl border border-royal/10 bg-royal/[0.03] p-12">
        <div className="flex items-center justify-between">
          <span className="text-[20px] font-bold text-royal">رقعة</span>
          <span dir="ltr" className="font-mono text-[12px] tracking-[0.24em] text-neutral/45 uppercase">Rakkas · Display</span>
        </div>
        <p className="m-0 font-display text-[140px] leading-[1.2] text-royal">ادْعُونِي</p>
        <p className="m-0 text-[19px] leading-[1.7] text-neutral/65">
          خط العناوين والكلمة علامة. حروف منسابة ذات طابع خطّي عربي، تُستعمل بحجم كبير وبكثافة منخفضة.
        </p>
      </div>

      <div className="flex flex-col justify-between rounded-3xl border border-violet/20 bg-violet/[0.06] p-12">
        <div className="flex items-center justify-between">
          <span className="text-[20px] font-bold text-violet">تجوال</span>
          <span dir="ltr" className="font-mono text-[12px] tracking-[0.24em] text-neutral/45 uppercase">Tajawal · Body</span>
        </div>
        <div className="flex flex-col gap-2">
          <p className="m-0 font-sans text-[64px] font-bold leading-[1.3] text-royal">دعاء اليوم</p>
          <p className="m-0 font-sans text-[28px] leading-[1.7] text-neutral/75">
            خط النصوص والواجهة. واضح، حديث، ويدعم العربية واللاتينية بأوزان متعددة.
          </p>
        </div>
        <div dir="ltr" className="flex gap-3 font-sans text-[18px] text-neutral/55">
          <span className="font-light">Light 300</span>
          <span className="font-normal">Regular 400</span>
          <span className="font-medium">Medium 500</span>
          <span className="font-bold">Bold 700</span>
        </div>
      </div>
    </div>
  </SlideBody>
)
