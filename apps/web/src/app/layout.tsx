import type { Metadata } from "next";
import { Rakkas, Geist_Mono } from "next/font/google";
import localFont from "next/font/local";
import "./globals.css";

const rakkas = Rakkas({
  weight: "400",
  subsets: ["arabic"],
  variable: "--font-rakkas",
  display: "swap",
});

const tajawal = localFont({
  variable: "--font-tajawal",
  display: "swap",
  declarations: [
    { prop: "ascent-override", value: "100%" },
    { prop: "descent-override", value: "50%" },
    { prop: "line-gap-override", value: "0%" },
  ],
  src: [
    { path: "./fonts/tajawal-arabic-400-normal.woff2", weight: "400", style: "normal" },
    { path: "./fonts/tajawal-arabic-500-normal.woff2", weight: "500", style: "normal" },
    { path: "./fonts/tajawal-arabic-700-normal.woff2", weight: "700", style: "normal" },
  ],
});

const geistMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-geist-mono",
  display: "swap",
});

const verse = "وَقَالَ رَبُّكُمُ ادْعُونِي أَسْتَجِبْ لَكُمْ";

export const metadata: Metadata = {
  title: "ادْعُونِي · تذكير يومي بالدعاء",
  description: `${verse} — مبادرة مفتوحة المصدر تذكّرك بالدعاء كل يوم عبر منصاتك المفضلة.`,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="ar"
      dir="rtl"
      className={`${rakkas.variable} ${tajawal.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full">{children}</body>
    </html>
  );
}
