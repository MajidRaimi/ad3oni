import type { CSSProperties, ReactNode } from "react"
import { SLIDE_HEIGHT, SLIDE_WIDTH } from "./order"
import { Wordmark } from "./Wordmark"

const PADDING_X = 120
const PADDING_Y = 80
const REG_INSET = 48

export type ChromeTone = "dark" | "light"

type TonePalette = {
  mark: string
  dim: string
  dim2: string
  dim3: string
  strong: string
  wordmark: "royal" | "paper"
}

const TONE: Record<ChromeTone, TonePalette> = {
  dark: {
    mark: "rgba(26,19,48,0.20)",
    dim: "rgba(26,19,48,0.45)",
    dim2: "rgba(26,19,48,0.28)",
    dim3: "rgba(26,19,48,0.5)",
    strong: "#1a1330",
    wordmark: "royal",
  },
  light: {
    mark: "rgba(255,255,255,0.34)",
    dim: "rgba(255,255,255,0.62)",
    dim2: "rgba(255,255,255,0.4)",
    dim3: "rgba(255,255,255,0.72)",
    strong: "#ffffff",
    wordmark: "paper",
  },
}

const corner: Record<"ts" | "te" | "bs" | "be", CSSProperties> = {
  ts: { top: REG_INSET, insetInlineStart: REG_INSET },
  te: { top: REG_INSET, insetInlineEnd: REG_INSET },
  bs: { bottom: REG_INSET, insetInlineStart: REG_INSET },
  be: { bottom: REG_INSET, insetInlineEnd: REG_INSET },
}

const RegistrationMark = ({ at, stroke }: { at: "ts" | "te" | "bs" | "be"; stroke: string }) => (
  <svg
    width={14}
    height={14}
    viewBox="0 0 14 14"
    aria-hidden
    style={{ position: "absolute", pointerEvents: "none", ...corner[at] }}
  >
    <line x1={7} y1={0} x2={7} y2={14} stroke={stroke} strokeWidth={1} />
    <line x1={0} y1={7} x2={14} y2={7} stroke={stroke} strokeWidth={1} />
  </svg>
)

const mono: CSSProperties = { fontFamily: "var(--font-mono)" }
const arabic: CSSProperties = { fontFamily: "var(--font-arabic)" }

type Props = {
  children: ReactNode
  pageNumber: string
  section: string
  background?: string
  bare?: boolean
  tone?: ChromeTone
}

export const SlideChrome = ({
  children,
  pageNumber,
  section,
  background = "#ffffff",
  bare = false,
  tone = "dark",
}: Props) => {
  const t = TONE[tone]
  return (
    <div
      style={{
        position: "relative",
        width: SLIDE_WIDTH,
        height: SLIDE_HEIGHT,
        background,
        color: t.strong,
        overflow: "hidden",
        fontFamily: "var(--font-sans)",
      }}
    >
      {children}

      <RegistrationMark at="ts" stroke={t.mark} />
      <RegistrationMark at="te" stroke={t.mark} />
      <RegistrationMark at="bs" stroke={t.mark} />
      <RegistrationMark at="be" stroke={t.mark} />

      {!bare && (
        <>
          <div style={{ position: "absolute", top: PADDING_Y - 6, insetInlineStart: PADDING_X }}>
            <Wordmark color={t.wordmark} size={34} />
          </div>

          <div
            style={{
              ...arabic,
              position: "absolute",
              top: PADDING_Y + 10,
              insetInlineEnd: PADDING_X,
              fontSize: 13,
              color: t.dim,
              fontWeight: 500,
            }}
          >
            نظام الهوية والتصميم · <span dir="ltr" style={{ ...mono, fontWeight: 600 }}>v0.1</span>
          </div>

          <div
            style={{
              ...arabic,
              position: "absolute",
              insetInlineEnd: 56,
              top: "50%",
              transform: "translateY(-50%)",
              writingMode: "vertical-rl",
              fontSize: 13,
              color: t.dim2,
              whiteSpace: "nowrap",
            }}
          >
            {section}
          </div>

          <div style={{ position: "absolute", bottom: PADDING_Y, insetInlineStart: PADDING_X, fontSize: 13 }}>
            <span style={{ ...mono, color: t.strong, fontWeight: 600 }}>{pageNumber}</span>
          </div>

          <div
            style={{
              position: "absolute",
              bottom: PADDING_Y,
              insetInlineEnd: PADDING_X,
              display: "flex",
              alignItems: "baseline",
              gap: 10,
              fontSize: 13,
              color: t.dim3,
              fontWeight: 500,
            }}
          >
            <span style={arabic}>ادْعُونِي</span>
            <span aria-hidden style={{ color: t.dim2 }}>·</span>
            <span dir="ltr" style={{ ...mono, fontSize: 12, letterSpacing: "0.24em", textTransform: "uppercase" }}>
              Ad3oni
            </span>
          </div>
        </>
      )}
    </div>
  )
}

export { PADDING_X, PADDING_Y }
