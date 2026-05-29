import { BookHeart, Compass, Sparkles } from "lucide-react"
import { SlideBody, SlideHeader } from "../primitives"

const values = [
  { ar: "اللطف", en: "Gentleness", desc: "تذكير بلا ثقل، نبرة دافئة قريبة." },
  { ar: "الصدق", en: "Sincerity", desc: "محتوى صحيح المصدر، بلا مبالغة." },
  { ar: "الانفتاح", en: "Openness", desc: "مفتوح المصدر، يبنيه المجتمع معنا." },
  { ar: "العربية أولا", en: "Arabic-first", desc: "RTL أصيل، الخط العربي في القلب." },
]

export const SlideMission = () => (
  <SlideBody>
    <SlideHeader no={1} ar="الرسالة والقيم" en="Mission" title="الرسالة · الرؤية · القيم" titleEn="Mission · Vision · Values" />

    <div className="mt-11 grid flex-1 grid-cols-2 gap-8">
      <div className="flex flex-col gap-6">
        <div className="flex flex-1 flex-col gap-3 rounded-3xl border border-royal/10 bg-royal/[0.04] p-10">
          <div className="flex items-center gap-3 text-royal">
            <BookHeart size={26} />
            <span className="text-[19px] font-bold">الرسالة</span>
            <span dir="ltr" className="font-mono text-[11px] tracking-[0.22em] text-neutral/40 uppercase">Mission</span>
          </div>
          <p className="m-0 text-[26px] leading-[1.7] text-neutral/80">
            نُبقي القلوب موصولة بالدعاء عبر تذكير يومي لطيف، في كل منصة يكون فيها الناس.
          </p>
        </div>
        <div className="flex flex-1 flex-col gap-3 rounded-3xl border border-violet/20 bg-violet/[0.08] p-10">
          <div className="flex items-center gap-3 text-violet">
            <Compass size={26} />
            <span className="text-[19px] font-bold">الرؤية</span>
            <span dir="ltr" className="font-mono text-[11px] tracking-[0.22em] text-neutral/40 uppercase">Vision</span>
          </div>
          <p className="m-0 text-[26px] leading-[1.7] text-neutral/80">
            أن يكون «ادْعُونِي» أرفق رفيق رقمي للذكر، يبنيه مجتمع مفتوح المصدر حول العالم.
          </p>
        </div>
      </div>

      <div className="flex flex-col gap-4 rounded-3xl border border-royal/10 bg-white p-10 shadow-[0_18px_44px_rgba(7,1,42,0.08)]">
        <div className="flex items-center gap-3 text-royal">
          <Sparkles size={26} />
          <span className="text-[19px] font-bold">القيم</span>
          <span dir="ltr" className="font-mono text-[11px] tracking-[0.22em] text-neutral/40 uppercase">Values</span>
        </div>
        <div className="mt-2 grid flex-1 grid-cols-2 gap-5">
          {values.map((v) => (
            <div key={v.en} className="flex flex-col justify-center gap-2 rounded-2xl bg-royal/[0.03] p-7">
              <div className="flex items-baseline gap-2">
                <span className="text-[24px] font-bold text-royal">{v.ar}</span>
                <span dir="ltr" className="font-mono text-[11px] tracking-[0.18em] text-violet uppercase">{v.en}</span>
              </div>
              <p className="m-0 text-[17px] leading-[1.7] text-neutral/65">{v.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  </SlideBody>
)
