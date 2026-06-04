import { AboutSection } from "./components/AboutSection";
import { CommunityPrayersSection } from "./components/CommunityPrayersSection";
import { Hero } from "./components/Hero";
import { HowItWorksSection } from "./components/HowItWorksSection";
import { PlatformsSection } from "./components/PlatformsSection";
import { RewardSection } from "./components/RewardSection";
import { ShareSection } from "./components/ShareSection";
import { SiteFooter } from "./components/SiteFooter";
import { SiteNav } from "./components/SiteNav";
import { ShareModal } from "@/features/share/components/ShareModal";

export const LandingPage = () => (
  <>
    <SiteNav />
    <main>
      <Hero />
      <AboutSection />
      <HowItWorksSection />
      <RewardSection />
      <CommunityPrayersSection />
      <PlatformsSection />
      <ShareSection />
    </main>
    <SiteFooter />
    <ShareModal />
  </>
);
