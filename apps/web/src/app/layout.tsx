import type { Metadata, Viewport } from "next";
import { Rakkas, Geist_Mono, Amiri } from "next/font/google";
import localFont from "next/font/local";
import { JsonLd } from "@/shared/seo/JsonLd";
import {
  BRAND_BACKGROUND,
  BRAND_COLOR,
  SITE_DESCRIPTION,
  SITE_KEYWORDS,
  SITE_NAME,
  SITE_TAGLINE,
  SITE_URL,
  TWITTER_HANDLE,
} from "@/shared/seo/site";
import { Providers } from "./providers";
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

const amiri = Amiri({
  weight: ["400", "700"],
  subsets: ["arabic"],
  variable: "--font-amiri",
  display: "swap",
});

const geistMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-geist-mono",
  display: "swap",
});

const TITLE = `${SITE_NAME} · ${SITE_TAGLINE}`;

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: BRAND_BACKGROUND },
    { media: "(prefers-color-scheme: dark)", color: BRAND_COLOR },
  ],
};

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: TITLE,
    template: `%s · ${SITE_NAME}`,
  },
  description: SITE_DESCRIPTION,
  keywords: SITE_KEYWORDS,
  applicationName: SITE_NAME,
  category: "religion",
  alternates: {
    canonical: "/",
  },
  openGraph: {
    type: "website",
    locale: "ar_SA",
    url: SITE_URL,
    siteName: SITE_NAME,
    title: TITLE,
    description: SITE_DESCRIPTION,
  },
  twitter: {
    card: "summary_large_image",
    site: TWITTER_HANDLE,
    creator: TWITTER_HANDLE,
    title: TITLE,
    description: SITE_DESCRIPTION,
  },
  appleWebApp: {
    capable: true,
    title: SITE_NAME,
    statusBarStyle: "default",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-image-preview": "large",
      "max-snippet": -1,
      "max-video-preview": -1,
    },
  },
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
      className={`${rakkas.variable} ${tajawal.variable} ${amiri.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full">
        <JsonLd />
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
