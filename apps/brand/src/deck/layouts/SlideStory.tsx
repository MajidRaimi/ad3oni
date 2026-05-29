import { SlideBody, SlideHeader } from "../primitives"

export const SlideStory = () => (
  <SlideBody>
    <SlideHeader no={1} ar="القصة" en="Story" title="ادْعُونِي أَسْتَجِبْ لَكُمْ" titleEn="Call upon Me, I will answer you" />

    <div className="mt-12 grid flex-1 grid-cols-[1.1fr_1fr] gap-14">
      <div className="night-bg flex flex-col justify-center gap-8 rounded-3xl px-16 py-14 text-paper">
        <div className="flex items-center justify-center gap-6" dir="rtl">
          <span className="font-display text-[110px] leading-none text-paper/55 select-none">&#123;</span>
          <p className="m-0 text-center font-display text-[52px] leading-[1.7] text-paper">
            وَقَالَ رَبُّكُمُ ادْعُونِي أَسْتَجِبْ لَكُمْ
          </p>
          <span className="font-display text-[110px] leading-none text-paper/55 select-none">&#125;</span>
        </div>
        <span dir="rtl" className="text-center text-[15px] font-medium tracking-wide text-paper/70">
          سورة غافر · الآية ٦٠
        </span>
      </div>

      <div className="flex flex-col justify-center gap-7 text-[24px] leading-[1.9] text-neutral/80">
        <p className="m-0">
          الاسم مأخوذ من الآية مباشرة: «ادْعُونِي». دعوة مفتوحة، دافئة، لا تتطلب أكثر من قلب يلتفت. هذا هو
          وعد العلامة كله في كلمة واحدة.
        </p>
        <p className="m-0">
          «ادْعُونِي» منصة مفتوحة المصدر تذكّرك بالدعاء وذكر الله عبر تويتر، الموقع، وبوت ديسكورد، وتطبيقات
          قادمة. نجمع التقنية والروح في تذكير لطيف يومي.
        </p>
        <div className="mt-2 flex gap-4">
          <span className="rounded-full bg-royal/8 px-5 py-2 text-[17px] font-medium text-royal">دعاء يومي</span>
          <span className="rounded-full bg-violet/12 px-5 py-2 text-[17px] font-medium text-violet">مفتوح المصدر</span>
          <span className="rounded-full bg-royal/6 px-5 py-2 text-[17px] font-medium text-royal">عربي أولا</span>
        </div>
      </div>
    </div>
  </SlideBody>
)
