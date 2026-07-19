"use client";

import { Wordmark } from "@/features/landing/components/Wordmark";
import { Button } from "@/shared/ui/button";

type ErrorPageProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function ErrorPage({ error, reset }: ErrorPageProps) {
  return (
    <main className="night-bg flex min-h-svh flex-col items-center justify-center gap-8 px-6 py-20 text-center text-paper">
      <Wordmark className="text-5xl text-paper" />

      <div className="flex flex-col items-center gap-3">
        <h1 className="font-display text-4xl text-paper md:text-5xl">
          حدث خطأ غير متوقع
        </h1>
        <p className="max-w-lg text-lg leading-[1.9] text-paper/65">
          تعذّر عرض هذه الصفحة. حاول مرة أخرى، وإن تكرّر الأمر فعُد بعد قليل.
        </p>
        {error.digest ? (
          <span className="font-mono text-xs text-paper/35" dir="ltr">
            <bdi>{error.digest}</bdi>
          </span>
        ) : null}
      </div>

      <Button type="button" variant="paper" size="lg" onClick={reset}>
        حاول مرة أخرى
      </Button>
    </main>
  );
}
