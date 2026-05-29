import { useState } from "react"
import { Check, Copy } from "lucide-react"

export const CopyButton = ({ value, className = "" }: { value: string; className?: string }) => {
  const [copied, setCopied] = useState(false)

  const onClick = () => {
    if (typeof navigator === "undefined") return
    navigator.clipboard
      .writeText(value)
      .then(() => {
        setCopied(true)
        window.setTimeout(() => setCopied(false), 1400)
      })
      .catch(() => undefined)
  }

  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={`نسخ ${value}`}
      className={`inline-flex items-center gap-1.5 transition-colors ${className}`}
    >
      {copied ? <Check size={14} strokeWidth={2.5} /> : <Copy size={14} strokeWidth={2} />}
    </button>
  )
}
