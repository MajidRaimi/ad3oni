import { Link } from "@tanstack/react-router"
import { Wordmark } from "../Wordmark"
import { deckOrder } from "../order"

export const SlideCover = () => (
  <div className="night-bg absolute inset-0 flex flex-col justify-between px-[120px] py-[100px] text-paper">
    <div className="flex items-start justify-between">
      <span className="text-[22px] text-paper/70">نظام الهوية والتصميم</span>
      <span dir="ltr" className="font-mono text-[14px] tracking-[0.18em] text-paper/45 uppercase">
        {deckOrder.length} slides · v0.1
      </span>
    </div>

    <div className="flex flex-col items-start gap-12">
      <div className="flex items-center gap-8" dir="rtl">
        <span className="font-display text-[200px] leading-none text-paper/45 select-none">&#123;</span>
        <Wordmark color="paper" size={280} />
        <span className="font-display text-[200px] leading-none text-paper/45 select-none">&#125;</span>
      </div>
      <p dir="rtl" className="m-0 max-w-[1320px] text-[34px] leading-[1.6] text-paper/65">
        نظام الهوية والتصميم الحي لمنصة «ادْعُونِي». الاستراتيجية، الشعار، الألوان، الخطوط، الأيقونات، الأسس،
        والمكونات، وكيف تظهر جميعها في مكان واحد ليبني عليها كل من يعمل معنا.
      </p>
    </div>

    <div className="flex items-end justify-between">
      <Link
        to="/contents"
        className="text-[18px] text-paper/60 underline-offset-[10px] transition-colors hover:text-lilac hover:underline"
      >
        المحتويات ←
      </Link>
      <span dir="ltr" className="font-mono text-[13px] tracking-[0.24em] text-paper/40 uppercase">
        Ad3oni · 2026
      </span>
    </div>
  </div>
)
