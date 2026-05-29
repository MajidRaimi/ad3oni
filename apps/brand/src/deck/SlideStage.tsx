import type { ReactNode } from "react"
import { SLIDE_HEIGHT, SLIDE_WIDTH } from "./order"
import { useViewportScale } from "./useViewportScale"

export const SlideStage = ({ children }: { children: ReactNode }) => {
  const scale = useViewportScale()

  return (
    <div
      className="relative overflow-hidden rounded-2xl shadow-[0_30px_80px_rgba(7,1,42,0.18),0_0_0_1px_rgba(7,1,42,0.06)]"
      style={{ width: SLIDE_WIDTH * scale, height: SLIDE_HEIGHT * scale }}
    >
      <div
        className="absolute left-0 top-0 origin-top-left"
        style={{ width: SLIDE_WIDTH, height: SLIDE_HEIGHT, transform: `scale(${scale})` }}
      >
        {children}
      </div>
    </div>
  )
}
