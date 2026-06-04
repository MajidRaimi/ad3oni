import { cn } from "@/shared/lib/utils";
import { toArabicIndex } from "@/shared/lib/arabic";
import { howItWorksSteps } from "../data/howItWorks";
import { Reveal } from "./Reveal";
import { SectionHeading } from "./SectionHeading";

export const HowItWorksSection = () => (
  <section id="how" className="bg-muted/40 px-6 py-20 md:py-28">
    <div className="mx-auto max-w-6xl">
      <SectionHeading label="كيف تعمل" title="ثلاث خطوات بسيطة" />

      <ol className="mx-auto hidden max-w-5xl grid-cols-3 md:grid">
        {howItWorksSteps.map((step, index) => {
          const isFirst = index === 0;
          const isLast = index === howItWorksSteps.length - 1;
          return (
            <li key={step.key}>
              <Reveal delay={index * 0.08}>
                <div className="flex flex-col items-center text-center">
                  <div className="flex w-full items-center gap-4">
                    <span
                      className={cn(
                        "h-px flex-1 bg-violet/25",
                        isFirst && "opacity-0",
                      )}
                    />
                    <span className="font-sans text-5xl font-bold leading-none text-violet">
                      <bdi>{toArabicIndex(index + 1)}</bdi>
                    </span>
                    <span
                      className={cn(
                        "h-px flex-1 bg-violet/25",
                        isLast && "opacity-0",
                      )}
                    />
                  </div>
                  <h3 className="mt-8 px-4 font-display text-3xl text-royal">
                    {step.title}
                  </h3>
                  <p className="mt-4 px-4 text-lg leading-[1.95] text-neutral">
                    {step.description}
                  </p>
                </div>
              </Reveal>
            </li>
          );
        })}
      </ol>

      <ol className="mx-auto max-w-md md:hidden">
        {howItWorksSteps.map((step, index) => {
          const isLast = index === howItWorksSteps.length - 1;
          return (
            <li key={step.key}>
              <Reveal delay={index * 0.08}>
                <div className="grid grid-cols-[auto_1fr] gap-6">
                  <div className="flex flex-col items-center">
                    <span className="font-sans text-4xl font-bold leading-none text-violet">
                      <bdi>{toArabicIndex(index + 1)}</bdi>
                    </span>
                    {!isLast ? (
                      <span className="mt-4 w-px flex-1 bg-gradient-to-b from-violet/40 to-transparent" />
                    ) : null}
                  </div>
                  <div className={cn(isLast ? "pb-0" : "pb-12")}>
                    <h3 className="font-display text-2xl text-royal">
                      {step.title}
                    </h3>
                    <p className="mt-3 text-lg leading-[1.95] text-neutral">
                      {step.description}
                    </p>
                  </div>
                </div>
              </Reveal>
            </li>
          );
        })}
      </ol>
    </div>
  </section>
);
