import { useEffect } from "react"
import { useRouter } from "@tanstack/react-router"

export const useKeyboardNav = (prevPath: string | null, nextPath: string | null) => {
  const router = useRouter()

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      const t = e.target
      if (t instanceof HTMLElement && ["INPUT", "TEXTAREA", "SELECT"].includes(t.tagName)) return
      if (e.metaKey || e.ctrlKey || e.altKey) return

      if ((e.key === "ArrowLeft" || e.key === "PageDown" || e.key === " ") && nextPath) {
        e.preventDefault()
        router.navigate({ to: nextPath })
      } else if ((e.key === "ArrowRight" || e.key === "PageUp") && prevPath) {
        e.preventDefault()
        router.navigate({ to: prevPath })
      }
    }
    window.addEventListener("keydown", handler)
    return () => window.removeEventListener("keydown", handler)
  }, [router, prevPath, nextPath])
}
