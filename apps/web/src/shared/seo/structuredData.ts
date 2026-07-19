import {
  DISCORD_INVITE_URL,
  GITHUB_URL,
  SITE_DESCRIPTION,
  SITE_NAME,
  SITE_NAME_LATIN,
  SITE_URL,
  TWITTER_URL,
  absoluteUrl,
} from "./site";

const ORGANIZATION_ID = `${SITE_URL}/#organization`;
const WEBSITE_ID = `${SITE_URL}/#website`;

export const siteStructuredData = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": ORGANIZATION_ID,
      name: SITE_NAME,
      alternateName: SITE_NAME_LATIN,
      url: SITE_URL,
      description: SITE_DESCRIPTION,
      logo: {
        "@type": "ImageObject",
        url: absoluteUrl("/icon-512.png"),
        width: 512,
        height: 512,
      },
      sameAs: [TWITTER_URL, GITHUB_URL, DISCORD_INVITE_URL],
    },
    {
      "@type": "WebSite",
      "@id": WEBSITE_ID,
      url: SITE_URL,
      name: SITE_NAME,
      alternateName: SITE_NAME_LATIN,
      description: SITE_DESCRIPTION,
      inLanguage: "ar",
      publisher: { "@id": ORGANIZATION_ID },
    },
  ],
};
