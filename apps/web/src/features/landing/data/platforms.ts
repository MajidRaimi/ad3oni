import { Globe } from "lucide-react";
import type { ComponentType, SVGProps } from "react";
import { AndroidIcon, AppleIcon, DiscordIcon, XIcon } from "../components/icons";

export type Platform = {
  key: string;
  name: string;
  handle: string;
  description: string;
  href: string;
  status: "live" | "soon";
  icon: ComponentType<SVGProps<SVGSVGElement>>;
  steps: string[];
  features: string[];
};

export const platforms: Platform[] = [
  {
    key: "web",
    name: "الموقع",
    handle: "ad3oni.com",
    description: "افتح الموقع في أي وقت لتقرأ دعاء اليوم وتشارك دعاءك.",
    href: "https://www.ad3oni.com",
    status: "live",
    icon: Globe,
    steps: [
      "افتح ad3oni.com في أي وقت",
      "اقرأ دعاء اليوم المتجدّد",
      "شارك دعاءك بضغطة واحدة",
    ],
    features: [
      "دعاء يومي متجدّد",
      "تصفّح حسب الفئة",
      "مشاركة دعائك",
      "بحث في الأدعية",
    ],
  },
  {
    key: "x",
    name: "إكس",
    handle: "@ad3oni_",
    description: "دعاء يومي يصلك في موجزك، تشاركه بضغطة واحدة.",
    href: "https://twitter.com/ad3oni_",
    status: "live",
    icon: XIcon,
    steps: [
      "تابِع حساب @ad3oni_",
      "يصلك دعاء اليوم في موجزك",
      "أعد نشره لمن تحب",
    ],
    features: [
      "تغريدة دعاء يومية",
      "مشاركة بنقرة",
      "تذكير للمتابعين",
      "أرشيف الأدعية",
    ],
  },
  {
    key: "discord",
    name: "ديسكورد",
    handle: "بوت ادْعُونِي",
    description: "ادعُ البوت إلى خادمك ليذكّر أعضاءك بدعاء اليوم تلقائيًا.",
    href: "https://discord.com/api/oauth2/authorize?client_id=1159198588782518292&permissions=26624&scope=bot%20applications.commands",
    status: "live",
    icon: DiscordIcon,
    steps: [
      "ادعُ البوت إلى خادمك",
      "اختر القناة ووقت التذكير",
      "يذكّر الأعضاء تلقائيًا كل يوم",
    ],
    features: [
      "تذكير يومي تلقائي",
      "أمر /دعاء",
      "تخصيص الوقت والقناة",
      "أدعية حسب الفئة",
    ],
  },
  {
    key: "ios",
    name: "آيفون",
    handle: "App Store",
    description: "تطبيق ادْعُونِي لنظام iOS، تذكير بالدعاء بين يديك.",
    href: "#",
    status: "soon",
    icon: AppleIcon,
    steps: [
      "حمّل التطبيق من App Store",
      "فعّل التذكير اليومي",
      "ادعُ أينما كنت",
    ],
    features: [
      "إشعار يومي",
      "ودجت على الشاشة",
      "حفظ المفضلة",
      "يعمل دون إنترنت",
    ],
  },
  {
    key: "android",
    name: "أندرويد",
    handle: "Google Play",
    description: "تطبيق ادْعُونِي لنظام Android، قريبًا على جهازك.",
    href: "#",
    status: "soon",
    icon: AndroidIcon,
    steps: [
      "حمّل التطبيق من Google Play",
      "فعّل التذكير اليومي",
      "ادعُ أينما كنت",
    ],
    features: [
      "إشعار يومي",
      "ودجت على الشاشة",
      "حفظ المفضلة",
      "يعمل دون إنترنت",
    ],
  },
];
