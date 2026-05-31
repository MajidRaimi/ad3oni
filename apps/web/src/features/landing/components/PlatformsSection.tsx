import { PlatformTabs } from "./PlatformTabs";
import { Reveal } from "./Reveal";
import { SectionHeading } from "./SectionHeading";

export const PlatformsSection = () => (
  <section id="platforms" className="bg-muted/40 px-6 py-28 md:py-36">
    <div className="mx-auto max-w-6xl">
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
