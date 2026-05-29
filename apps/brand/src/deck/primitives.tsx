import type { ReactNode } from "react"
import { pad2 } from "./order"

export const Eyebrow = ({ no, ar, en }: { no?: number; ar: string; en: string }) => (
  <div className="flex items-center gap-3">
    {no !== undefined && (
      <span className="font-mono text-[15px] font-semibold text-violet">{pad2(no)}</span>
    )}
    <span className="text-[17px] font-medium text-royal">{ar}</span>
    <span dir="ltr" className="font-mono text-[12px] tracking-[0.24em] text-neutral/45 uppercase">
      {en}
    </span>
  </div>
)

export const SlideBody = ({
  children,
  className = "",
  dir = "rtl",
}: {
  children: ReactNode
  className?: string
  dir?: "rtl" | "ltr"
}) => (
  <div dir={dir} className={`absolute inset-0 flex flex-col px-[120px] pt-[184px] pb-[148px] ${className}`}>
    {children}
  </div>
)

export const SlideHeader = ({
  no,
  ar,
  en,
  title,
  titleEn,
  light = false,
}: {
  no?: number
  ar: string
  en: string
  title: string
  titleEn: string
  light?: boolean
}) => (
  <div className="flex flex-col gap-3">
    <Eyebrow no={no} ar={ar} en={en} />
    <h2 className={`m-0 font-display text-[76px] leading-[1.06] ${light ? "text-paper" : "text-royal"}`}>
      {title}
    </h2>
    <p
      dir="ltr"
      className={`m-0 font-mono text-[14px] tracking-[0.24em] uppercase ${light ? "text-paper/55" : "text-neutral/45"}`}
    >
      {titleEn}
    </p>
  </div>
)

export const MonoTag = ({ children, className = "" }: { children: ReactNode; className?: string }) => (
  <span dir="ltr" className={`font-mono text-[13px] tracking-[0.04em] tabular-nums ${className}`}>
    {children}
  </span>
)

export const Panel = ({
  children,
  className = "",
}: {
  children: ReactNode
  className?: string
}) => (
  <div
    className={`rounded-2xl border border-royal/10 bg-white p-8 shadow-[0_18px_44px_rgba(7,1,42,0.08)] ${className}`}
  >
    {children}
  </div>
)
