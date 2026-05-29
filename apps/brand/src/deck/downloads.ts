import { colorTokens, radiusTokens, shadowTokens, motionTokens, fontTokens, easeBrand } from "./tokens"

export const buildTokensCss = (): string => {
  const colors = colorTokens.map((c) => `  ${c.varName}: ${c.hex};`).join("\n")
  const radius = radiusTokens.map((r) => `  --radius-${r.name}: ${r.px};`).join("\n")
  const shadows = shadowTokens.map((s) => `  --shadow-${s.name}: ${s.value};`).join("\n")
  const motion = motionTokens.map((m) => `  --duration-${m.name}: ${m.value};`).join("\n")
  return [
    "@theme {",
    colors,
    `  --font-display: "${fontTokens.display.name}", serif;`,
    `  --font-sans: "${fontTokens.sans.name}", sans-serif;`,
    `  --font-mono: "${fontTokens.mono.name}", monospace;`,
    radius,
    shadows,
    motion,
    `  --ease-brand: ${easeBrand};`,
    "}",
    "",
  ].join("\n")
}

export const buildTokensJson = (): string => {
  const json = {
    color: Object.fromEntries(colorTokens.map((c) => [c.name.toLowerCase(), c.hex])),
    font: {
      display: fontTokens.display.name,
      sans: fontTokens.sans.name,
      mono: fontTokens.mono.name,
    },
    radius: Object.fromEntries(radiusTokens.map((r) => [r.name, r.px])),
    shadow: Object.fromEntries(shadowTokens.map((s) => [s.name, s.value])),
    duration: Object.fromEntries(motionTokens.map((m) => [m.name, m.value])),
    ease: { brand: easeBrand },
  }
  return JSON.stringify(json, null, 2)
}

export const downloadFile = (filename: string, content: string, mime: string) => {
  if (typeof window === "undefined") return
  const blob = new Blob([content], { type: mime })
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}
