import { useEffect, useState } from "react"
import type { ReactNode } from "react"
import { useRouterState } from "@tanstack/react-router"
import { deckOrder, entryOfPath, indexOfPath, pad2 } from "./order"
import { SlideStage } from "./SlideStage"
import { SlideChrome } from "./SlideChrome"
import { DeckControls } from "./DeckControls"
import { MobileDeck } from "./MobileDeck"
import { Wordmark } from "./Wordmark"
import { SlideReveal } from "./SlideReveal"
import { useIsMobile } from "./useIsMobile"
import { useKeyboardNav } from "./useKeyboardNav"

export const DeckShell = ({ children }: { children: ReactNode }) => {
  const pathname = useRouterState({ select: (s) => s.location.pathname })
  const index = indexOfPath(pathname)
  const total = deckOrder.length
  const entry = entryOfPath(pathname)
  const prevPath = index > 0 ? deckOrder[index - 1].path : null
  const nextPath = index < total - 1 ? deckOrder[index + 1].path : null

  useKeyboardNav(prevPath, nextPath)

  const [mounted, setMounted] = useState(false)
  useEffect(() => setMounted(true), [])
  const isMobile = useIsMobile()

  if (!mounted || isMobile === null) {
    return (
      <div className="flex h-dvh w-full items-center justify-center bg-paper">
        <div className="flex flex-col items-center gap-3">
          <Wordmark color="royal" size={48} className="opacity-50" />
          <span dir="ltr" className="font-mono text-[10.5px] tracking-[0.32em] uppercase text-royal/30">
            Loading the deck
          </span>
        </div>
      </div>
    )
  }

  const chrome = (
    <SlideChrome
      pageNumber={pad2(index + 1)}
      section={entry.section}
      bare={entry.kind === "cover"}
      tone={entry.tone ?? "dark"}
    >
      <SlideReveal revealKey={pathname}>{children}</SlideReveal>
    </SlideChrome>
  )

  if (isMobile) {
    return (
      <MobileDeck index={index} total={total} prevPath={prevPath} nextPath={nextPath}>
        {chrome}
      </MobileDeck>
    )
  }

  return (
    <div className="flex h-dvh w-full flex-col items-center justify-center gap-6 bg-paper p-8">
      <SlideStage>{chrome}</SlideStage>
      <DeckControls index={index} total={total} prevPath={prevPath} nextPath={nextPath} />
    </div>
  )
}
