import { AboutSection } from "./components/AboutSection";
import { Hero } from "./components/Hero";
import { PlatformsSection } from "./components/PlatformsSection";
import { ShareSection } from "./components/ShareSection";
import { SiteFooter } from "./components/SiteFooter";
import { SiteNav } from "./components/SiteNav";

export const LandingPage = () => (
  <>
    <SiteNav />
    <main>
      <Hero />
      <AboutSection />
      <PlatformsSection />
      <ShareSection />
    </main>
    <SiteFooter />
  </>
);
