import type { MetadataRoute } from "next";
import {
  BRAND_BACKGROUND,
  BRAND_COLOR,
  SITE_DESCRIPTION,
  SITE_NAME,
  SITE_SHORT_NAME,
  SITE_TAGLINE,
} from "@/shared/seo/site";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: `${SITE_NAME} · ${SITE_TAGLINE}`,
    short_name: SITE_SHORT_NAME,
    description: SITE_DESCRIPTION,
    lang: "ar",
    dir: "rtl",
    start_url: "/",
    display: "standalone",
    orientation: "portrait",
    background_color: BRAND_BACKGROUND,
    theme_color: BRAND_COLOR,
    categories: ["lifestyle", "education"],
    icons: [
      {
        src: "/icon-192.png",
        sizes: "192x192",
        type: "image/png",
        purpose: "any",
      },
      {
        src: "/icon-512.png",
        sizes: "512x512",
        type: "image/png",
        purpose: "any",
      },
      {
        src: "/icon-512.png",
        sizes: "512x512",
        type: "image/png",
        purpose: "maskable",
      },
    ],
  };
}
