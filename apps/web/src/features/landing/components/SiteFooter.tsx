import { navLinks } from "../data/navigation";
import { platforms } from "../data/platforms";
import { Wordmark } from "./Wordmark";

export const SiteFooter = () => (
  <footer className="night-bg border-t border-paper/10 px-6 pt-20 pb-10 text-paper">
    <div className="mx-auto max-w-6xl">
      <div className="flex flex-col gap-14 md:flex-row md:justify-between">
        <div className="flex max-w-sm flex-col gap-4">
          <Wordmark className="text-4xl text-paper" />
          <p className="text-[15px] leading-[1.9] text-paper/60">
            مبادرة خيرية مفتوحة المصدر، تذكّرك بالدعاء كل يوم. صُنعت بحب ليبني عليها كل من يريد أن يذكّر الناس بالخير.
          </p>
        </div>

        <div className="flex gap-16">
          <nav className="flex flex-col gap-4">
            <span className="text-xs tracking-[0.18em] text-paper/40">روابط</span>
            {navLinks.map((link) => (
              <a
                key={link.href}
                href={link.href}
                className="text-[15px] text-paper/75 transition-colors hover:text-paper"
              >
                {link.label}
              </a>
            ))}
          </nav>

          <nav className="flex flex-col gap-4">
            <span className="text-xs tracking-[0.18em] text-paper/40">منصّاتنا</span>
            {platforms.map((platform) => (
              <a
                key={platform.key}
                href={platform.href}
                target={platform.status === "live" ? "_blank" : undefined}
                rel={platform.status === "live" ? "noopener noreferrer" : undefined}
                className="text-[15px] text-paper/75 transition-colors hover:text-paper"
              >
                {platform.name}
              </a>
            ))}
          </nav>
        </div>
      </div>

      <div className="mt-16 flex flex-col gap-3 border-t border-paper/10 pt-8 text-sm text-paper/45 sm:flex-row sm:items-center sm:justify-between">
        <span>صُنع بحب · مفتوح المصدر</span>
        <span dir="ltr" className="font-mono tracking-wide">
          <bdi>© 2026 Ad3oni · ad3oni.com</bdi>
        </span>
      </div>
    </div>
  </footer>
);
