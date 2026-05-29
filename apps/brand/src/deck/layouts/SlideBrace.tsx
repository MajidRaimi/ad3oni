import { SlideBody, SlideHeader } from "../primitives"

export const SlideBrace = () => (
  <SlideBody>
    <SlideHeader no={8} ar="إطار القوسين" en="Brace" title="إطار القوسين" titleEn="The Brace Frame" />

    <div className="mt-12 grid flex-1 grid-cols-[1.5fr_1fr] gap-14">
      <div className="night-bg flex items-center justify-center gap-8 rounded-3xl px-12 text-paper" dir="rtl">
        <span className="font-display text-[180px] leading-none text-paper select-none">&#123;</span>
        <p className="m-0 text-center font-display text-[56px] leading-[1.6] text-paper">
          ربِّ اشرح لي صدري ويسِّر لي أمري
        </p>
        <span className="font-display text-[180px] leading-none text-paper select-none">&#125;</span>
      </div>

      <div className="flex flex-col justify-center gap-6 text-[21px] leading-[1.8] text-neutral/80">
        <p className="m-0">
          القوسان <span className="font-display text-[34px] text-royal">{"{ }"}</span> هما توقيع العلامة البصري. يحتضنان
          الدعاء كأنه اقتباس مقدّس، ويمنحانه إيقاعا فوريا يُعرف من بعيد.
        </p>
        <ul className="m-0 flex list-none flex-col gap-3 p-0">
          <li className="flex items-start gap-3"><span className="mt-2 h-2 w-2 shrink-0 rounded-full bg-violet" /> ليلكي على الخلفيات الداكنة، وبنفسجي على الفاتحة.</li>
          <li className="flex items-start gap-3"><span className="mt-2 h-2 w-2 shrink-0 rounded-full bg-violet" /> يدوران 90° على الجوال ليحيطا النص رأسيا.</li>
          <li className="flex items-start gap-3"><span className="mt-2 h-2 w-2 shrink-0 rounded-full bg-violet" /> دائما بخط رقعة، لا يستبدلان بأقواس عادية.</li>
        </ul>
      </div>
    </div>
  </SlideBody>
)
