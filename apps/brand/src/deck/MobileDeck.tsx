import type { ReactNode } from "react"
import { SLIDE_HEIGHT, SLIDE_WIDTH } from "./order"
import { Wordmark } from "./Wordmark"
import { DeckControls } from "./DeckControls"

type Props = {
  children: ReactNode
  index: number
  total: number
  prevPath: string | null
  nextPath: string | null
}

export const MobileDeck = ({ children, index, total, prevPath, nextPath }: Props) => {
  const margin = 24
  const scale = typeof window === "undefined" ? 0.2 : (window.innerWidth - margin * 2) / SLIDE_WIDTH

  return (
    <div className="flex min-h-dvh flex-col items-center gap-5 bg-paper px-6 py-7">
      <div className="flex w-full items-center justify-between">
        <Wordmark color="royal" size={30} />
        <span dir="ltr" className="font-mono text-[11px] tracking-[0.2em] text-royal/45 uppercase">
          {index + 1} / {total}
        </span>
      </div>

      <p dir="rtl" className="text-center text-[13px] leading-relaxed text-neutral/70">
        العرض مهيأ لشاشة أوسع. تصفح الشرائح هنا أو افتحه على الحاسوب لتجربة كاملة.
      </p>

      <div
        className="overflow-hidden rounded-xl shadow-[0_18px_44px_rgba(7,1,42,0.16),0_0_0_1px_rgba(7,1,42,0.06)]"
        style={{ width: SLIDE_WIDTH * scale, height: SLIDE_HEIGHT * scale }}
      >
        <div
          className="origin-top-left"
          style={{ width: SLIDE_WIDTH, height: SLIDE_HEIGHT, transform: `scale(${scale})` }}
        >
          {children}
        </div>
      </div>

      <DeckControls index={index} total={total} prevPath={prevPath} nextPath={nextPath} />
    </div>
  )
}
