export const SLIDE_WIDTH = 1920
export const SLIDE_HEIGHT = 1080

export type SlideKind = "cover" | "index" | "divider" | "slide" | "closing"

export type DeckEntry = {
  path: string
  label: string
  labelEn: string
  title: string
  titleEn: string
  chapter: number
  section: string
  sectionEn: string
  kind: SlideKind
  tone?: "dark" | "light"
}

const INTRO = "المقدمة"
const INTRO_EN = "Intro"

export const deckOrder: ReadonlyArray<DeckEntry> = [
  { path: "/", label: "الغلاف", labelEn: "Cover", title: "ادْعُونِي · نظام الهوية والتصميم", titleEn: "Ad3oni Design System", chapter: 0, section: INTRO, sectionEn: INTRO_EN, kind: "cover" },
  { path: "/contents", label: "المحتويات", labelEn: "Contents", title: "المحتويات", titleEn: "Contents", chapter: 0, section: INTRO, sectionEn: INTRO_EN, kind: "index" },

  { path: "/strategy", label: "الاستراتيجية", labelEn: "Strategy", title: "استراتيجية العلامة", titleEn: "Brand Strategy", chapter: 1, section: "الاستراتيجية", sectionEn: "Strategy", kind: "divider", tone: "light" },
  { path: "/story", label: "القصة", labelEn: "Story", title: "ادْعُونِي أَسْتَجِبْ لَكُمْ", titleEn: "Call upon Me, I will answer", chapter: 1, section: "الاستراتيجية", sectionEn: "Strategy", kind: "slide" },
  { path: "/mission", label: "الرسالة والقيم", labelEn: "Mission", title: "الرسالة · الرؤية · القيم", titleEn: "Mission · Vision · Values", chapter: 1, section: "الاستراتيجية", sectionEn: "Strategy", kind: "slide" },
  { path: "/voice", label: "الصوت والنبرة", labelEn: "Voice", title: "الصوت والنبرة", titleEn: "Voice & Tone", chapter: 1, section: "الاستراتيجية", sectionEn: "Strategy", kind: "slide" },

  { path: "/logo-system", label: "الشعار", labelEn: "Logo", title: "الشعار والكلمة علامة", titleEn: "Logo & Wordmark", chapter: 2, section: "الشعار", sectionEn: "Logo", kind: "divider", tone: "light" },
  { path: "/wordmark", label: "الكلمة علامة", labelEn: "Wordmark", title: "الكلمة علامة", titleEn: "The Wordmark", chapter: 2, section: "الشعار", sectionEn: "Logo", kind: "slide" },
  { path: "/logo-clearspace", label: "الحيز الآمن", labelEn: "Clearspace", title: "الحيز الآمن والحد الأدنى", titleEn: "Clearspace & Min Size", chapter: 2, section: "الشعار", sectionEn: "Logo", kind: "slide" },
  { path: "/logo-variants", label: "الأشكال", labelEn: "Variants", title: "أشكال الألوان والخلفيات", titleEn: "Color & Background Variants", chapter: 2, section: "الشعار", sectionEn: "Logo", kind: "slide" },
  { path: "/logo-misuse", label: "سوء الاستخدام", labelEn: "Misuse", title: "سوء الاستخدام · الممنوعات", titleEn: "Misuse", chapter: 2, section: "الشعار", sectionEn: "Logo", kind: "slide" },

  { path: "/color-system", label: "الألوان", labelEn: "Color", title: "الألوان", titleEn: "Color", chapter: 3, section: "الألوان", sectionEn: "Color", kind: "divider", tone: "light" },
  { path: "/color", label: "اللوحة", labelEn: "Palette", title: "لوحة الألوان", titleEn: "The Palette", chapter: 3, section: "الألوان", sectionEn: "Color", kind: "slide" },
  { path: "/color-royal", label: "الأرجواني", labelEn: "Royal", title: "الأرجواني · اللون الأساسي", titleEn: "Royal · Primary", chapter: 3, section: "الألوان", sectionEn: "Color", kind: "slide", tone: "light" },
  { path: "/color-ratios", label: "النسب والتباين", labelEn: "Ratios", title: "النسب والتباين", titleEn: "Ratios & Contrast", chapter: 3, section: "الألوان", sectionEn: "Color", kind: "slide" },

  { path: "/typography", label: "الخطوط", labelEn: "Type", title: "الخطوط", titleEn: "Typography", chapter: 4, section: "الخطوط", sectionEn: "Type", kind: "divider", tone: "light" },
  { path: "/type", label: "النظام", labelEn: "System", title: "خطان · نظام واحد", titleEn: "Two Fonts, One System", chapter: 4, section: "الخطوط", sectionEn: "Type", kind: "slide" },
  { path: "/type-rakkas", label: "رقعة", labelEn: "Rakkas", title: "«رقعة» · خط العناوين", titleEn: "Rakkas · Display", chapter: 4, section: "الخطوط", sectionEn: "Type", kind: "slide", tone: "light" },
  { path: "/type-scale", label: "المقياس", labelEn: "Scale", title: "مقياس الخط والتسلسل", titleEn: "Type Scale", chapter: 4, section: "الخطوط", sectionEn: "Type", kind: "slide" },

  { path: "/iconography", label: "الأيقونات", labelEn: "Icons", title: "الأيقونات", titleEn: "Iconography", chapter: 5, section: "الأيقونات", sectionEn: "Icons", kind: "divider", tone: "light" },
  { path: "/icons", label: "الأسلوب والمجموعة", labelEn: "Icon Set", title: "الأسلوب والمجموعة", titleEn: "Style & Set", chapter: 5, section: "الأيقونات", sectionEn: "Icons", kind: "slide" },

  { path: "/foundations", label: "الأسس", labelEn: "Foundations", title: "الأسس والرموز", titleEn: "Foundations & Tokens", chapter: 6, section: "الأسس", sectionEn: "Foundations", kind: "divider", tone: "light" },
  { path: "/tokens", label: "الرموز", labelEn: "Tokens", title: "رموز التصميم · الطبقات", titleEn: "Design Tokens", chapter: 6, section: "الأسس", sectionEn: "Foundations", kind: "slide" },
  { path: "/spacing", label: "التباعد والشبكة", labelEn: "Spacing", title: "التباعد والشبكة", titleEn: "Spacing & Grid", chapter: 6, section: "الأسس", sectionEn: "Foundations", kind: "slide", tone: "light" },
  { path: "/radius", label: "الحواف والظل", labelEn: "Radius", title: "نصف القطر والارتفاع", titleEn: "Radius & Elevation", chapter: 6, section: "الأسس", sectionEn: "Foundations", kind: "slide" },
  { path: "/motion", label: "الحركة والحالات", labelEn: "Motion", title: "الحركة والحالات", titleEn: "Motion & States", chapter: 6, section: "الأسس", sectionEn: "Foundations", kind: "slide", tone: "light" },

  { path: "/components", label: "المكونات", labelEn: "Components", title: "المكونات", titleEn: "Components", chapter: 7, section: "المكونات", sectionEn: "Components", kind: "divider", tone: "light" },
  { path: "/buttons", label: "الأزرار", labelEn: "Buttons", title: "الأزرار", titleEn: "Buttons", chapter: 7, section: "المكونات", sectionEn: "Components", kind: "slide" },
  { path: "/forms", label: "النماذج", labelEn: "Forms", title: "النماذج والحقول", titleEn: "Forms & Inputs", chapter: 7, section: "المكونات", sectionEn: "Components", kind: "slide" },
  { path: "/cards", label: "البطاقات", labelEn: "Cards", title: "البطاقات", titleEn: "Cards", chapter: 7, section: "المكونات", sectionEn: "Components", kind: "slide" },
  { path: "/feedback", label: "التغذية الراجعة", labelEn: "Feedback", title: "التغذية الراجعة والبيانات", titleEn: "Feedback & Data", chapter: 7, section: "المكونات", sectionEn: "Components", kind: "slide" },

  { path: "/patterns", label: "الأنماط والاستخدام", labelEn: "Patterns", title: "الأنماط والاستخدام", titleEn: "Patterns & Usage", chapter: 8, section: "الأنماط", sectionEn: "Patterns", kind: "divider", tone: "light" },
  { path: "/brace", label: "إطار الدعاء", labelEn: "Brace", title: "إطار القوسين", titleEn: "The Brace Frame", chapter: 8, section: "الأنماط", sectionEn: "Patterns", kind: "slide" },
  { path: "/dos-donts", label: "افعل ولا تفعل", labelEn: "Do / Don't", title: "افعل ولا تفعل", titleEn: "Do & Don't", chapter: 8, section: "الأنماط", sectionEn: "Patterns", kind: "slide" },

  { path: "/applications", label: "التطبيقات", labelEn: "Applications", title: "التطبيقات", titleEn: "Applications", chapter: 9, section: "التطبيقات", sectionEn: "Applications", kind: "divider", tone: "light" },
  { path: "/prayer-card", label: "بطاقة الدعاء", labelEn: "Prayer Card", title: "بطاقة دعاء اليوم", titleEn: "Daily Du'a Card", chapter: 9, section: "التطبيقات", sectionEn: "Applications", kind: "slide" },

  { path: "/resources", label: "المصادر", labelEn: "Resources", title: "المصادر والتنزيلات", titleEn: "Resources & Downloads", chapter: 10, section: "الختام", sectionEn: "Closing", kind: "slide" },
  { path: "/credits", label: "الاعتمادات", labelEn: "Credits", title: "ادْعُونِي", titleEn: "Ad3oni", chapter: 10, section: "الختام", sectionEn: "Closing", kind: "closing", tone: "light" },
]

export type DeckPath = (typeof deckOrder)[number]["path"]

export const pad2 = (n: number): string => String(n).padStart(2, "0")

export const indexOfPath = (pathname: string): number => {
  const clean = pathname.length > 1 ? pathname.replace(/\/+$/, "") : pathname
  const i = deckOrder.findIndex((e) => e.path === clean)
  return i === -1 ? 0 : i
}

export const entryOfPath = (pathname: string): DeckEntry => deckOrder[indexOfPath(pathname)]

export type Chapter = { no: number; title: string; titleEn: string; entries: Array<DeckEntry> }

export const chapters: Array<Chapter> = (() => {
  const byNo = new Map<number, Chapter>()
  for (const e of deckOrder) {
    if (e.chapter === 0) continue
    let c = byNo.get(e.chapter)
    if (!c) {
      c = { no: e.chapter, title: e.section, titleEn: e.sectionEn, entries: [] }
      byNo.set(e.chapter, c)
    }
    c.entries.push(e)
  }
  return [...byNo.values()].sort((a, b) => a.no - b.no)
})()
