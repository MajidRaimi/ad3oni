import { cn } from "@/shared/lib/utils";
import { Reveal } from "./Reveal";

type SectionHeadingProps = {
  label: string;
  title: string;
  subtitle?: string;
  tone?: "light" | "dark";
};

export const SectionHeading = ({
  label,
  title,
  subtitle,
  tone = "light",
}: SectionHeadingProps) => (
  <Reveal>
    <div className="mb-12 flex flex-col items-center gap-3 text-center md:mb-16">
      <span
        className={cn(
          "text-sm tracking-[0.18em]",
          tone === "dark" ? "text-lilac" : "text-violet",
        )}
      >
        {label}
      </span>
      <h2
        className={cn(
          "font-display text-4xl md:text-5xl",
          tone === "dark" ? "text-paper" : "text-royal",
        )}
      >
        {title}
      </h2>
      {subtitle ? (
        <p
          className={cn(
            "max-w-xl text-lg leading-[1.9]",
            tone === "dark" ? "text-paper/70" : "text-neutral",
          )}
        >
          {subtitle}
        </p>
      ) : null}
    </div>
  </Reveal>
);
