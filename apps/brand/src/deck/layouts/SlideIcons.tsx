import { Bell, BookOpen, Calendar, HandHeart, Heart, MapPin, MoonStar, Send, Share2, Sparkles, Sunrise, Clock } from "lucide-react"
import { SlideBody, SlideHeader } from "../primitives"

const set = [
  { Icon: HandHeart, ar: "دعاء" },
  { Icon: MoonStar, ar: "ليل" },
  { Icon: Sunrise, ar: "فجر" },
  { Icon: Clock, ar: "وقت" },
  { Icon: Bell, ar: "تذكير" },
  { Icon: Calendar, ar: "اليوم" },
  { Icon: BookOpen, ar: "ذكر" },
  { Icon: Heart, ar: "محبة" },
  { Icon: Share2, ar: "مشاركة" },
  { Icon: Send, ar: "إرسال" },
  { Icon: MapPin, ar: "قبلة" },
  { Icon: Sparkles, ar: "أثر" },
]

export const SlideIcons = () => (
  <SlideBody>
    <SlideHeader no={5} ar="الأسلوب والمجموعة" en="Icon Set" title="الأسلوب والمجموعة" titleEn="Style & Set" />

    <div className="mt-12 grid flex-1 grid-cols-[1fr_2fr] gap-12">
      <div className="flex flex-col justify-center gap-7">
        <div className="flex items-center justify-center rounded-3xl border border-royal/10 bg-royal/[0.03] py-10">
          <div className="relative">
            <div className="absolute inset-0 -m-3 rounded-lg border border-dashed border-violet/40" />
            <HandHeart size={120} strokeWidth={1.75} className="text-royal" />
          </div>
        </div>
        <div className="flex flex-col gap-3 text-[19px] leading-[1.7] text-neutral/75">
          <div className="flex items-center justify-between border-b border-royal/8 pb-2">
            <span>الشبكة</span><span dir="ltr" className="font-mono text-[14px] text-neutral/55">24 × 24</span>
          </div>
          <div className="flex items-center justify-between border-b border-royal/8 pb-2">
            <span>سُمك الخط</span><span dir="ltr" className="font-mono text-[14px] text-neutral/55">1.75px</span>
          </div>
          <div className="flex items-center justify-between border-b border-royal/8 pb-2">
            <span>النهايات</span><span>مدوّرة</span>
          </div>
          <div className="flex items-center justify-between">
            <span>المصدر</span><span dir="ltr" className="font-mono text-[14px] text-neutral/55">Lucide · ISC</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-4 content-center gap-5">
        {set.map(({ Icon, ar }) => (
          <div key={ar} className="flex flex-col items-center justify-center gap-3 rounded-2xl border border-royal/8 bg-white py-7 shadow-[0_8px_22px_rgba(7,1,42,0.05)]">
            <Icon size={40} strokeWidth={1.75} className="text-royal" />
            <span className="text-[16px] text-neutral/70">{ar}</span>
          </div>
        ))}
      </div>
    </div>
  </SlideBody>
)
