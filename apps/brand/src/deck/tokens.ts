export type ColorToken = {
  name: string
  varName: string
  hex: string
  rgb: string
  ar: string
  role: string
  onLight: boolean
}

export const colorTokens: Array<ColorToken> = [
  { name: "Royal", varName: "--color-royal", hex: "#2b0d69", rgb: "43, 13, 105", ar: "الأرجواني", role: "اللون الأساسي · الأزرار والعناوين", onLight: true },
  { name: "Violet", varName: "--color-violet", hex: "#6d49d6", rgb: "109, 73, 214", ar: "البنفسجي", role: "اللكنة · الروابط وحلقات التركيز", onLight: true },
  { name: "Lilac", varName: "--color-lilac", hex: "#a98ee6", rgb: "169, 142, 230", ar: "الليلكي", role: "اللكنة على الداكن · القوسان", onLight: false },
  { name: "Night", varName: "--color-night", hex: "#0c0626", rgb: "12, 6, 38", ar: "الليلي", role: "الخلفيات الداكنة · المشاهد", onLight: true },
  { name: "Paper", varName: "--color-paper", hex: "#ffffff", rgb: "255, 255, 255", ar: "الورقي", role: "السطح الفاتح · النص على الداكن", onLight: false },
  { name: "Ink", varName: "--color-ink", hex: "#1a1330", rgb: "26, 19, 48", ar: "الحبري", role: "النص الأساسي على الفاتح", onLight: true },
]

export const royalRamp: Array<{ step: string; hex: string }> = [
  { step: "950", hex: "#0c0626" },
  { step: "900", hex: "#1c0847" },
  { step: "800", hex: "#2b0d69" },
  { step: "600", hex: "#4f2caa" },
  { step: "500", hex: "#6d49d6" },
  { step: "400", hex: "#8a6ed6" },
  { step: "300", hex: "#ad97e4" },
  { step: "100", hex: "#e9e3f9" },
]

export const radiusTokens: Array<{ name: string; px: string }> = [
  { name: "xs", px: "4px" },
  { name: "sm", px: "8px" },
  { name: "md", px: "12px" },
  { name: "lg", px: "20px" },
  { name: "xl", px: "28px" },
  { name: "pill", px: "999px" },
]

export const spacingTokens: Array<string> = ["4", "8", "12", "16", "24", "32", "48", "64", "96"]

export const shadowTokens: Array<{ name: string; value: string }> = [
  { name: "xs", value: "0 1px 2px rgba(7,1,42,.06)" },
  { name: "sm", value: "0 6px 16px rgba(7,1,42,.08)" },
  { name: "md", value: "0 18px 44px rgba(7,1,42,.12)" },
  { name: "lg", value: "0 28px 64px rgba(7,1,42,.16)" },
  { name: "royal", value: "0 20px 52px rgba(43,13,105,.28)" },
]

export const motionTokens: Array<{ name: string; value: string; ms: string }> = [
  { name: "fast", value: "150ms", ms: "150" },
  { name: "base", value: "280ms", ms: "280" },
  { name: "slow", value: "480ms", ms: "480" },
]

export const easeBrand = "cubic-bezier(0.19, 1, 0.22, 1)"

export const fontTokens = {
  display: { name: "Rakkas", ar: "رقعة", role: "العناوين والكلمة علامة" },
  sans: { name: "Tajawal", ar: "تجوال", role: "النصوص والواجهة" },
  mono: { name: "Geist Mono", ar: "—", role: "الأرقام والرموز" },
}
