import Link from "next/link";
import { Wordmark } from "@/features/landing/components/Wordmark";
import { buttonVariants } from "@/shared/ui/button";

export default function NotFound() {
  return (
    <main className="night-bg flex min-h-svh flex-col items-center justify-center gap-8 px-6 py-20 text-center text-paper">
      <Wordmark className="text-5xl text-paper" />

      <div className="flex flex-col items-center gap-3">
        <span className="font-mono text-sm tracking-[0.3em] text-lilac" dir="ltr">
          <bdi>404</bdi>
        </span>
        <h1 className="font-display text-4xl text-paper md:text-5xl">
          لم نجد هذه الصفحة
        </h1>
        <p className="max-w-lg text-lg leading-[1.9] text-paper/65">
          ربما حُذف الرابط أو تغيّر. عُد إلى الصفحة الرئيسة لتقرأ دعاء اليوم.
        </p>
      </div>

      <Link href="/" className={buttonVariants({ variant: "paper", size: "lg" })}>
        العودة إلى الرئيسة
      </Link>
    </main>
  );
}
