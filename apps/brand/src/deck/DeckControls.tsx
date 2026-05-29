import { Link } from "@tanstack/react-router"
import { ChevronLeft, ChevronRight } from "lucide-react"

type Props = {
  index: number
  total: number
  prevPath: string | null
  nextPath: string | null
}

const dotClass =
  "flex h-9 w-9 items-center justify-center rounded-full border border-royal/15 text-royal transition-colors hover:border-violet/50 hover:bg-royal/5"
const disabledClass = "pointer-events-none opacity-30"

export const DeckControls = ({ index, total, prevPath, nextPath }: Props) => (
  <div
    dir="ltr"
    className="flex items-center gap-4 rounded-full border border-royal/10 bg-royal/[0.03] px-4 py-2 backdrop-blur"
  >
    {nextPath ? (
      <Link to={nextPath} className={dotClass} aria-label="الشريحة التالية">
        <ChevronLeft size={18} />
      </Link>
    ) : (
      <span className={`${dotClass} ${disabledClass}`} aria-hidden>
        <ChevronLeft size={18} />
      </span>
    )}

    <span className="min-w-16 text-center font-mono text-[13px] tracking-[0.08em] tabular-nums text-royal/55">
      {index + 1} / {total}
    </span>

    {prevPath ? (
      <Link to={prevPath} className={dotClass} aria-label="الشريحة السابقة">
        <ChevronRight size={18} />
      </Link>
    ) : (
      <span className={`${dotClass} ${disabledClass}`} aria-hidden>
        <ChevronRight size={18} />
      </span>
    )}
  </div>
)
