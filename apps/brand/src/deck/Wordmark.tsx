type WordmarkColor = "royal" | "violet" | "lilac" | "paper" | "ink" | "night"

const COLOR: Record<WordmarkColor, string> = {
  royal: "#2b0d69",
  violet: "#6d49d6",
  lilac: "#a98ee6",
  paper: "#ffffff",
  ink: "#1a1330",
  night: "#0c0626",
}

type Props = {
  color?: WordmarkColor
  size?: number
  className?: string
  withHarakat?: boolean
}

export const Wordmark = ({ color = "royal", size = 28, className = "", withHarakat = true }: Props) => (
  <span
    dir="rtl"
    className={`font-display leading-none ${className}`}
    style={{ color: COLOR[color], fontSize: size, letterSpacing: "0.005em" }}
  >
    {withHarakat ? "ادْعُونِي" : "ادعوني"}
  </span>
)
