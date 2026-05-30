import { ghafirVerse } from "../data/prayer";
import { BracePrayer } from "./BracePrayer";
import { Reveal } from "./Reveal";

const paragraphs = [
  "ادْعُونِي مبادرة خيرية مفتوحة المصدر، تهدف إلى تذكير الناس بالدعاء وذكر الله. بدأت بفكرة بسيطة وجميلة: أن يصلك دعاء كل يوم عبر منصّاتك المفضلة.",
  "هو أكثر من مجرّد بوت؛ مشروع يجمع بين التقنية والمعنى، ويذكّر الناس في كل مكان بأن يرفعوا أكفّهم بدعوة صادقة، كل يوم.",
];

export const AboutSection = () => (
  <section id="about" className="bg-paper px-6 py-28 md:py-36">
    <div className="mx-auto max-w-6xl">
      <Reveal>
        <div className="mb-16 flex flex-col items-center gap-3 text-center">
          <span className="text-sm tracking-[0.18em] text-violet">عن المبادرة</span>
          <h2 className="font-display text-4xl text-royal md:text-5xl">
            عن ادْعُونِي
          </h2>
        </div>
      </Reveal>

      <div className="grid items-stretch gap-8 lg:grid-cols-2">
        <Reveal>
          <div className="dotted-bg flex h-full items-center justify-center rounded-3xl p-10 text-paper shadow-royal md:p-14">
            <div className="flex flex-col items-center gap-6">
              <BracePrayer braceClassName="md:text-[110px]">
                <p className="font-display text-2xl text-paper md:text-[28px]">
                  {ghafirVerse.text}
                </p>
              </BracePrayer>
              <span className="text-sm text-paper/60">
                <bdi>{ghafirVerse.source}</bdi>
              </span>
            </div>
          </div>
        </Reveal>

        <Reveal delay={0.12}>
          <div className="flex h-full flex-col justify-center gap-6">
            {paragraphs.map((paragraph) => (
              <p
                key={paragraph}
                className="text-xl leading-[2] text-neutral md:text-[22px]"
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
