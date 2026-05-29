import { useRouterState } from "@tanstack/react-router"
import { chapters, entryOfPath, pad2 } from "../order"

export const SlideDivider = () => {
  const pathname = useRouterState({ select: (s) => s.location.pathname })
  const entry = entryOfPath(pathname)
  const chapter = chapters.find((c) => c.no === entry.chapter)

  return (
    <div className="night-bg absolute inset-0 flex flex-col justify-between px-[120px] py-[110px] text-paper">
      <div className="flex items-center gap-4">
        <span className="font-mono text-[18px] font-semibold text-lilac">{pad2(entry.chapter)}</span>
        <span dir="ltr" className="font-mono text-[13px] tracking-[0.3em] text-paper/45 uppercase">
          {entry.sectionEn}
        </span>
      </div>

      <div className="flex items-end gap-12" dir="rtl">
        <span className="font-display text-[420px] leading-[0.8] text-lilac/20 select-none">
          {pad2(entry.chapter)}
        </span>
        <div className="mb-10 flex flex-col gap-4">
          <h2 className="m-0 font-display text-[120px] leading-[1.02] text-paper">{entry.title}</h2>
          <p className="m-0 max-w-[760px] text-[22px] leading-[1.7] text-paper/55">
            {chapterIntro[entry.chapter] ?? ""}
          </p>
        </div>
      </div>

      <div className="flex items-center gap-3 text-paper/40">
        <span className="text-[15px]">{chapter ? `${chapter.entries.filter((e) => e.kind !== "divider").length} شرائح` : ""}</span>
      </div>
    </div>
  )
}

const chapterIntro: Record<number, string> = {
  1: "من أين تبدأ العلامة، وما الذي تعد به، وكيف تتكلم.",
  2: "الكلمة علامة، بناؤها، حيزها الآمن، وأشكالها المسموحة.",
  3: "اللوحة، الدور اللوني لكل لون، ونسب التباين.",
  4: "خطان يحملان الصوت العربي: العنوان والنص.",
  5: "أسلوب موحد للأيقونات ومجموعة العمل الأساسية.",
  6: "الرموز، التباعد، الحواف، الحركة، والحالات.",
  7: "مكونات حية مبنية على shadcn ومُلوّنة بهوية ادعوني.",
  8: "إطار القوسين، الخلفيات، وقواعد الاستخدام في الميدان.",
  9: "كيف تظهر الهوية في بطاقات الدعاء والمشاركة.",
  10: "المصادر، التنزيلات، ومن صنع هذا.",
}
