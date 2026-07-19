"use client";

import "./globals.css";

type GlobalErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function GlobalError({ error, reset }: GlobalErrorProps) {
  return (
    <html lang="ar" dir="rtl">
      <body className="min-h-full">
        <main className="night-bg flex min-h-svh flex-col items-center justify-center gap-8 px-6 py-20 text-center text-paper">
          <span className="font-display text-5xl leading-none text-paper">
            ادْعُونِي
          </span>

          <div className="flex flex-col items-center gap-3">
            <h1 className="font-display text-4xl text-paper md:text-5xl">
              حدث خطأ غير متوقع
            </h1>
            <p className="max-w-lg text-lg leading-[1.9] text-paper/65">
              تعذّر تحميل الموقع. حاول مرة أخرى بعد قليل.
            </p>
            {error.digest ? (
              <span className="font-mono text-xs text-paper/35" dir="ltr">
                <bdi>{error.digest}</bdi>
              </span>
            ) : null}
          </div>

          <button
            type="button"
            onClick={reset}
            className="inline-flex h-13 shrink-0 items-center justify-center rounded-full bg-paper px-9 text-base font-medium text-royal transition-all hover:scale-[1.03]"
          >
            حاول مرة أخرى
          </button>
        </main>
      </body>
    </html>
  );
}
