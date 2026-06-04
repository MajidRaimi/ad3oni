import { ShareButton } from "@/features/share/components/ShareButton";
import { Reveal } from "./Reveal";

export const ShareSection = () => (
  <section id="share" className="bg-paper py-20 md:py-28">
    <div className="mx-auto max-w-7xl px-6 md:px-10">
      <Reveal>
        <div className="night-bg flex w-full flex-col items-center gap-8 rounded-[2.5rem] px-6 py-20 text-center text-paper md:px-10 md:py-24">
          <span className="text-sm tracking-[0.18em] text-lilac">كن جزءًا منها</span>
          <h2 className="font-display text-4xl text-paper md:text-5xl">
            ذكّرنا بدعوة، وذكّر بها غيرك
          </h2>
          <p className="max-w-xl text-lg leading-[2] text-paper/70">
            شارك دعاء اليوم مع من تحب، أو ادعُ بوت ادْعُونِي إلى سيرفرك ليذكّر أعضاءك بالخير كل يوم.
          </p>

          <ShareButton variant="paper" size="lg">
            شارك دعاءك
          </ShareButton>
        </div>
      </Reveal>
    </div>
  </section>
);
