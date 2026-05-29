import { Link } from "@tanstack/react-router"
import { Wordmark } from "./Wordmark"

export const SlideError = ({ variant }: { variant: "notFound" | "error" }) => {
  const title = variant === "notFound" ? "الشريحة غير موجودة" : "حدث خطأ ما"
  const titleEn = variant === "notFound" ? "Slide not found" : "Something went wrong"

  return (
    <div className="flex h-dvh w-full flex-col items-center justify-center gap-6 bg-paper">
      <Wordmark color="royal" size={56} />
      <div className="flex flex-col items-center gap-1">
        <p dir="rtl" className="text-2xl font-bold text-royal">
          {title}
        </p>
        <p dir="ltr" className="font-mono text-xs tracking-[0.24em] uppercase text-neutral/50">
          {titleEn}
        </p>
      </div>
      <Link
        to="/"
        className="rounded-full border border-royal/20 px-6 py-2 text-sm text-royal transition-colors hover:bg-royal hover:text-paper"
      >
        العودة إلى الغلاف
      </Link>
    </div>
  )
}
