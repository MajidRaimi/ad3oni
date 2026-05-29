import { Wordmark } from "../Wordmark"
import { SlideBody, SlideHeader } from "../primitives"

export const SlideWordmark = () => (
  <SlideBody>
    <SlideHeader no={2} ar="الكلمة علامة" en="Wordmark" title="الكلمة علامة" titleEn="The Wordmark" />

    <div className="mt-12 grid flex-1 grid-cols-[1.4fr_1fr] gap-14">
      <div className="flex flex-col items-center justify-center gap-6 rounded-3xl border border-royal/10 bg-royal/[0.03]">
        <Wordmark color="royal" size={210} />
        <span dir="ltr" className="font-mono text-[13px] tracking-[0.3em] text-neutral/45 uppercase">
          Set in Rakkas · رقعة
        </span>
      </div>

      <div className="flex flex-col justify-center gap-8">
        <p className="m-0 text-[25px] leading-[1.85] text-neutral/80">
          الشعار هو الكلمة نفسها «ادْعُونِي»، مكتوبة بخط رقعة. بلا أيقونة وبلا إطار، الكلمة هي العلامة.
          الحركات جزء من الهوية، تبقى ظاهرة دائما.
        </p>
        <div className="flex flex-col gap-4">
          <div className="flex items-center justify-between rounded-2xl bg-white px-7 py-5 shadow-[0_10px_28px_rgba(7,1,42,0.07)]">
            <Wordmark color="royal" size={48} />
            <span className="text-[16px] text-neutral/55">أساسي · على فاتح</span>
          </div>
          <div className="flex items-center justify-between rounded-2xl bg-night px-7 py-5">
            <Wordmark color="paper" size={48} />
            <span className="text-[16px] text-paper/60">أبيض · على داكن</span>
          </div>
          <div className="flex items-center justify-between rounded-2xl bg-royal px-7 py-5">
            <Wordmark color="paper" size={48} />
            <span className="text-[16px] text-paper/70">أبيض · على الأرجواني</span>
          </div>
        </div>
      </div>
    </div>
  </SlideBody>
)
