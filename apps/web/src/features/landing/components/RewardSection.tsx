import { rewardHadith, rewardParagraphs } from "../data/reward";
import { BracePrayer } from "./BracePrayer";
import { Reveal } from "./Reveal";
import { SectionHeading } from "./SectionHeading";

export const RewardSection = () => (
  <section id="reward" className="night-bg px-6 py-20 text-paper md:py-28">
    <div className="mx-auto max-w-6xl">
      <SectionHeading label="الأجر" title="أجرٌ يجري إليك" tone="dark" />

      <div className="grid items-stretch gap-8 lg:grid-cols-2">
        <Reveal>
          <div className="flex h-full items-center justify-center rounded-3xl border border-paper/10 bg-paper/5 p-10 md:p-14">
            <div className="flex flex-col items-center gap-6">
              <BracePrayer braceClassName="text-lilac/40 md:text-[110px]">
                <p className="font-naskh text-xl text-paper md:text-2xl">
                  {rewardHadith.text}
                </p>
              </BracePrayer>
              <span className="text-sm text-paper/60">
                <bdi>{rewardHadith.attribution}</bdi>
              </span>
            </div>
          </div>
        </Reveal>

        <Reveal delay={0.12}>
          <div className="flex h-full flex-col justify-center gap-6">
            {rewardParagraphs.map((paragraph) => (
              <p
                key={paragraph}
                className="text-xl leading-[2] text-paper/70 md:text-[22px]"
              >
                {paragraph}
              </p>
            ))}
          </div>
        </Reveal>
      </div>
    </div>
  </section>
);
