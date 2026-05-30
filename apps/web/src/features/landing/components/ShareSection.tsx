import { buttonVariants } from "@/shared/ui/button";
import { Reveal } from "./Reveal";
import { DiscordIcon, XIcon } from "./icons";

const tweetText = encodeURIComponent("ادْعُونِي · تذكير يومي بالدعاء");
const tweetIntent = `https://twitter.com/intent/tweet?text=${tweetText}&url=https://www.ad3oni.com`;
const discordInvite =
  "https://discord.com/api/oauth2/authorize?client_id=1159198588782518292&permissions=26624&scope=bot%20applications.commands";

export const ShareSection = () => (
  <section id="share" className="night-bg px-6 py-28 text-paper md:py-36">
    <Reveal>
      <div className="mx-auto flex max-w-3xl flex-col items-center gap-8 text-center">
        <span className="text-sm tracking-[0.18em] text-lilac">كن جزءًا منها</span>
        <h2 className="font-display text-4xl text-paper md:text-5xl">
          ذكّرنا بدعوة، وذكّر بها غيرك
        </h2>
        <p className="max-w-xl text-lg leading-[2] text-paper/70">
          شارك دعاء اليوم مع من تحب، أو ادعُ بوت ادْعُونِي إلى خادمك ليذكّر أعضاءك بالخير كل يوم.
        </p>

        <div className="flex flex-col items-center gap-3 sm:flex-row">
          <a
            href={tweetIntent}
            target="_blank"
            rel="noopener noreferrer"
            className={buttonVariants({ variant: "paper", size: "lg" })}
          >
            <XIcon className="size-4" />
            شاركه على إكس
          </a>
          <a
            href={discordInvite}
            target="_blank"
            rel="noopener noreferrer"
            className={buttonVariants({ variant: "outline", size: "lg", className: "text-paper" })}
          >
            <DiscordIcon className="size-5" />
            ادعُ البوت لخادمك
          </a>
        </div>
      </div>
    </Reveal>
  </section>
);
