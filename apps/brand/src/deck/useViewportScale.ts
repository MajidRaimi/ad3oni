import { useEffect, useState } from "react"
import { SLIDE_HEIGHT, SLIDE_WIDTH } from "./order"

const compute = (padding: number): number => {
  if (typeof window === "undefined") return 1
  const availableW = window.innerWidth - padding * 2
  const availableH = window.innerHeight - padding * 2
  const next = Math.min(availableW / SLIDE_WIDTH, availableH / SLIDE_HEIGHT)
  return next > 0 ? next : 1
}

export const useViewportScale = (padding = 64): number => {
  const [scale, setScale] = useState(1)

  useEffect(() => {
    const onResize = () => setScale(compute(padding))
    onResize()
    window.addEventListener("resize", onResize)
    return () => window.removeEventListener("resize", onResize)
  }, [padding])

  return scale
}
