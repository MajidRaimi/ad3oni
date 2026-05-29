import { Wordmark } from "../Wordmark"
import { SlideBody, SlideHeader } from "../primitives"

export const SlideLogoClearspace = () => (
  <SlideBody>
    <SlideHeader no={2} ar="الحيز الآمن" en="Clearspace" title="الحيز الآمن والحد الأدنى" titleEn="Clearspace & Min Size" />

    <div className="mt-12 grid flex-1 grid-cols-[1.5fr_1fr] gap-14">
      <div className="relative flex items-center justify-center rounded-3xl border border-royal/10 bg-royal/[0.03]">
        <div className="relative p-[72px]">
          <div className="pointer-events-none absolute inset-0 rounded-xl border-2 border-dashed border-violet/50" />
          <div className="pointer-events-none absolute inset-[36px] rounded-md border border-royal/15" />
          <Wordmark color="royal" size={150} />
        </div>
        <span className="absolute bottom-7 font-mono text-[13px] tracking-[0.18em] text-neutral/45 uppercase">
          padding = 1×
        </span>
      </div>

      <div className="flex flex-col justify-center gap-10">
        <div className="flex flex-col gap-3">
          <span className="text-[20px] font-bold text-royal">منطقة العزل</span>
          <p className="m-0 text-[22px] leading-[1.8] text-neutral/75">
            اترك حول الشعار مسافة لا تقل عن ارتفاع حرف «ع» من الكلمة. لا يقترب منها نص أو حد أو حافة.
          </p>
        </div>
        <div className="h-px bg-royal/10" />
        <div className="flex flex-col gap-4">
          <span className="text-[20px] font-bold text-royal">الحد الأدنى للحجم</span>
          <div className="flex items-end gap-10">
            <div className="flex flex-col items-center gap-2">
              <Wordmark color="royal" size={40} />
              <span dir="ltr" className="font-mono text-[12px] text-neutral/50">40px · شاشة</span>
            </div>
            <div className="flex flex-col items-center gap-2">
              <Wordmark color="royal" size={26} />
              <span dir="ltr" className="font-mono text-[12px] text-neutral/50">14mm · طباعة</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </SlideBody>
)
