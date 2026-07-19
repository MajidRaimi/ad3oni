export const SITE_URL = "https://ad3oni.com";

export const SITE_NAME = "ادْعُونِي";
export const SITE_SHORT_NAME = "ادعوني";
export const SITE_NAME_LATIN = "Ad3oni";

export const SITE_TAGLINE = "تذكير يومي بالدعاء";

export const SITE_DESCRIPTION =
  "ادْعُونِي مبادرة خيرية مفتوحة المصدر تذكّرك بالدعاء كل يوم، عبر إكس وبوت ديسكورد والموقع والتطبيقات القادمة. شارك دعاءك ليصل غيرك فتُكتب لك أجوره.";

export const SITE_KEYWORDS = [
  "أدعية",
  "دعاء",
  "دعاء اليوم",
  "أدعية يومية",
  "تذكير بالدعاء",
  "أذكار",
  "أدعية من القرآن",
  "أدعية نبوية",
  "بوت أدعية ديسكورد",
  "ادعوني",
  "ad3oni",
];

export const TWITTER_HANDLE = "@ad3oni_";
export const TWITTER_URL = "https://twitter.com/ad3oni_";
export const GITHUB_URL = "https://github.com/MajidRaimi/ad3oni";
export const DISCORD_INVITE_URL =
  "https://discord.com/oauth2/authorize?client_id=1159198588782518292&permissions=84992&scope=bot+applications.commands";

export const BRAND_COLOR = "#2b0d69";
export const BRAND_BACKGROUND = "#ffffff";

export const OG_IMAGE_ALT = `${SITE_NAME} · ${SITE_TAGLINE}`;

export const absoluteUrl = (path = "/") => new URL(path, SITE_URL).toString();
