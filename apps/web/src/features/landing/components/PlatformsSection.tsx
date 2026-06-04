import { PlatformTabs } from "./PlatformTabs";
import { Reveal } from "./Reveal";
import { SectionHeading } from "./SectionHeading";

export const PlatformsSection = () => (
  <section id="platforms" className="bg-muted/40 py-20 md:py-28">
    <div className="mx-auto max-w-7xl px-6 md:px-10">
      <SectionHeading
        label="أينما كنت"
        title="منصّاتنا"
        subtitle="نذكّرك بالدعاء حيث تقضي يومك، من ديسكورد وإكس إلى الموقع والتطبيقات."
      />
      <Reveal>
        <PlatformTabs />
      </Reveal>
    </div>
  </section>
);
