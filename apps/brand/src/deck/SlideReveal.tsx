import type { ReactNode } from "react"
import { motion, useReducedMotion } from "motion/react"

export const SlideReveal = ({ revealKey, children }: { revealKey: string; children: ReactNode }) => {
  const reduce = useReducedMotion()

  if (reduce) {
    return <div style={{ position: "absolute", inset: 0 }}>{children}</div>
  }

  return (
    <motion.div
      key={revealKey}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.46, ease: [0.19, 1, 0.22, 1] }}
      style={{ position: "absolute", inset: 0 }}
    >
      {children}
    </motion.div>
  )
}
