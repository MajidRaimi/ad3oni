import { Link } from "@tanstack/react-router"
import { chapters, pad2 } from "../order"
import { SlideHeader } from "../primitives"

export const SlideContents = () => (
  <div className="absolute inset-0 flex flex-col px-[120px] pt-[172px] pb-[150px]" dir="rtl">
    <SlideHeader no={0} ar="المقدمة" en="Intro" title="المحتويات" titleEn="Contents" />

    <div className="mt-10 grid flex-1 grid-cols-4 gap-x-12 gap-y-7 content-start">
      {chapters.map((c) => (
        <div key={c.no} className="flex flex-col gap-3">
          <div className="flex items-baseline gap-3 border-b border-royal/10 pb-2">
            <span className="font-mono text-[15px] font-semibold text-violet">{pad2(c.no)}</span>
            <span className="text-[20px] font-bold text-royal">{c.title}</span>
            <span dir="ltr" className="font-mono text-[11px] tracking-[0.2em] text-neutral/40 uppercase">
              {c.titleEn}
            </span>
          </div>
          <div className="flex flex-col gap-1.5">
            {c.entries
              .filter((e) => e.kind !== "divider")
              .map((e) => (
                <Link
                  key={e.path}
                  to={e.path}
                  className="text-[15px] text-neutral/70 transition-colors hover:text-royal"
                >
                  {e.label}
                </Link>
              ))}
          </div>
        </div>
      ))}
    </div>
  </div>
)
