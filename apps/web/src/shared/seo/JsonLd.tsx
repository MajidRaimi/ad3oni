import { siteStructuredData } from "./structuredData";

export const JsonLd = () => (
  <script
    type="application/ld+json"
    dangerouslySetInnerHTML={{ __html: JSON.stringify(siteStructuredData) }}
  />
);
