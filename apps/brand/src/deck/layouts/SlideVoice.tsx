import { Check, X } from "lucide-react"
import { SlideBody, SlideHeader } from "../primitives"

const sayThis = [
  "حان وقت دعاء اليوم.",
  "ذكّرناك بخير، لا تنسَ تدعي.",
  "دعوة صغيرة، أثرها كبير.",
  "خذ لحظة، وادعُ بما في قلبك.",
]
const notThis = [
  "يجب عليك الدعاء الآن وإلا...",
  "لا تكن من الغافلين!",
  "اشترك الآن! عرض محدود.",
  "إن لم تدعِ ستندم على ذلك.",
]

export const SlideVoice = () => (
  <SlideBody>
    <SlideHeader no={1} ar="الصوت والنبرة" en="Voice" title="الصوت والنبرة" titleEn="Voice & Tone" />

    <div className="mt-10 flex items-center gap-5">
      {["دافئة", "لطيفة", "عربية أولا", "غير مؤسسية", "مشجّعة لا آمرة"].map((t) => (
        <span key={t} className="rounded-full border border-royal/12 px-5 py-2 text-[18px] text-royal">
          {t}
        </span>
      ))}
    </div>

    <div className="mt-9 grid flex-1 grid-cols-2 gap-8">
      <div className="flex flex-col gap-5 rounded-3xl border border-violet/25 bg-violet/[0.07] p-10">
        <div className="flex items-center gap-3">
          <span className="flex h-11 w-11 items-center justify-center rounded-full bg-violet text-paper">
            <Check size={22} strokeWidth={3} />
          </span>
          <span className="text-[24px] font-bold text-violet">نقول</span>
          <span dir="ltr" className="font-mono text-[12px] tracking-[0.22em] text-neutral/45 uppercase">We say</span>
        </div>
        <div className="flex flex-col gap-4">
          {sayThis.map((s) => (
            <p key={s} className="m-0 rounded-2xl bg-white/70 px-6 py-5 text-[23px] leading-[1.6] text-neutral/80">
              {s}
            </p>
          ))}
        </div>
      </div>

      <div className="flex flex-col gap-5 rounded-3xl border border-destructive/20 bg-destructive/[0.05] p-10">
        <div className="flex items-center gap-3">
          <span className="flex h-11 w-11 items-center justify-center rounded-full bg-destructive text-white">
            <X size={22} strokeWidth={3} />
          </span>
          <span className="text-[24px] font-bold text-destructive">لا نقول</span>
          <span dir="ltr" className="font-mono text-[12px] tracking-[0.22em] text-neutral/45 uppercase">We don't</span>
        </div>
        <div className="flex flex-col gap-4">
          {notThis.map((s) => (
            <p key={s} className="m-0 rounded-2xl bg-white/70 px-6 py-5 text-[23px] leading-[1.6] text-neutral/55 line-through decoration-destructive/40">
              {s}
            </p>
          ))}
        </div>
      </div>
    </div>
  </SlideBody>
)
