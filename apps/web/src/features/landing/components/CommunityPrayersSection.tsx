import { buttonVariants } from "@/shared/ui/button";
import { PrayerMarquee } from "./PrayerMarquee";
import { Reveal } from "./Reveal";
import { SectionHeading } from "./SectionHeading";

export const CommunityPrayersSection = () => (
  <section id="prayers" className="overflow-hidden bg-paper py-28 md:py-36">
    <div className="mx-auto max-w-6xl px-6">
      <SectionHeading
        label="من أدعيتكم"
        title="أدعية شاركها أمثالك"
        subtitle="هذه نماذج من أدعية شاركها الناس عبر ادْعُونِي، ووصلت غيرهم فكُتب لهم أجرها."
      />
    </div>

    <Reveal>
      <PrayerMarquee />
    </Reveal>

    <div className="mx-auto mt-16 flex max-w-6xl justify-center px-6">
      <a
        href="#share"
        className={buttonVariants({ variant: "default", size: "lg" })}
      >
        شارك دعاءك أنت أيضًا
      </a>
    </div>
  </section>
);
