import { Mail } from "lucide-react"
import { Wordmark } from "../Wordmark"

const developers = [
  { ar: "ماجد الريمي", en: "Majid Al-Raimi", email: "majidsraimi@gmail.com" },
  { ar: "راكان الياقوت", en: "Rakkan Al-Yaqout", email: "rakanyaqoot@hotmail.com" },
]

export const SlideCredits = () => (
  <div className="night-bg absolute inset-0 flex flex-col justify-between px-[120px] py-[110px] text-paper">
    <div className="flex items-center justify-between">
      <span className="font-mono text-[13px] tracking-[0.3em] text-paper/60 uppercase">Open Source · v0.1</span>
      <span dir="ltr" className="font-mono text-[13px] tracking-[0.24em] text-paper/40 uppercase">2026</span>
    </div>

    <div className="flex flex-col gap-7">
      <Wordmark color="paper" size={180} />
      <p className="m-0 max-w-[1100px] text-[28px] leading-[1.7] text-paper/65">
        صُنع بحب وبشكل مفتوح المصدر، ليبني عليه كل من يريد أن يذكّر الناس بالخير. شاركنا، اقترح، وادعُ لنا.
      </p>
    </div>

    <div className="flex items-end justify-between">
      <div className="flex gap-12">
        {developers.map((d) => (
          <div key={d.email} className="flex flex-col gap-1">
            <span className="text-[24px] font-bold text-paper">{d.ar}</span>
            <span dir="ltr" className="font-mono text-[13px] tracking-[0.12em] text-paper/45 uppercase">{d.en}</span>
            <a href={`mailto:${d.email}`} className="mt-1 flex items-center gap-2 text-[16px] text-lilac transition-colors hover:text-paper">
              <Mail size={16} /> <bdi>{d.email}</bdi>
            </a>
          </div>
        ))}
      </div>
      <span dir="ltr" className="font-mono text-[13px] tracking-[0.24em] text-paper/40 uppercase">ad3oni.com</span>
    </div>
  </div>
)
