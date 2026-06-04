"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm, useWatch } from "react-hook-form";
import { cn } from "@/shared/lib/utils";
import { toArabicIndex } from "@/shared/lib/arabic";
import { toApiError } from "@/shared/api/errors";
import { Button } from "@/shared/ui/button";
import { MAX_LENGTH, sharePrayerSchema, type SharePrayerValues } from "../schema";
import { useShareModal } from "../store";
import { useSubmitPrayer } from "../useSubmitPrayer";

export const SharePrayerForm = () => {
  const {
    register,
    handleSubmit,
    control,
    formState: { errors, isValid },
  } = useForm<SharePrayerValues>({
    resolver: zodResolver(sharePrayerSchema),
    mode: "onChange",
    defaultValues: { text: "" },
  });

  const value = useWatch({ control, name: "text" }) ?? "";
  const used = value.length;
  const ratio = Math.min(used / MAX_LENGTH, 1);
  const warning = ratio >= 0.8 && ratio < 1;
  const full = ratio >= 1;

  const mutation = useSubmitPrayer();
  const showSuccess = useShareModal((state) => state.showSuccess);

  const onSubmit = handleSubmit((values) =>
    mutation.mutate(
      { text: values.text },
      { onSuccess: () => showSuccess() },
    ),
  );

  const submitError = mutation.isError ? toApiError(mutation.error) : null;
  const submitMessage =
    submitError?.code === "rate_limited"
      ? "لقد أرسلت عدة أدعية. انتظر قليلًا ثم حاول مرة أخرى."
      : submitError
        ? "تعذّر إرسال دعائك. حاول مرة أخرى."
        : null;

  return (
    <form onSubmit={onSubmit} className="flex flex-col gap-5">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <label htmlFor="prayer-text" className="text-sm font-medium text-royal">
            دعاؤك
          </label>
          <span
            dir="ltr"
            className={cn(
              "text-xs tabular-nums",
              full ? "text-red-600" : warning ? "text-amber-600" : "text-neutral/60",
            )}
          >
            <bdi>
              {toArabicIndex(used)} / {toArabicIndex(MAX_LENGTH)}
            </bdi>
          </span>
        </div>

        <textarea
          id="prayer-text"
          rows={5}
          maxLength={MAX_LENGTH}
          autoFocus
          placeholder="اللهم اشرح صدري، ويسّر أمري…"
          aria-invalid={Boolean(errors.text)}
          {...register("text")}
          className={cn(
            "w-full resize-none rounded-2xl border bg-paper p-4 text-[15px] leading-[1.9] text-royal outline-none transition-colors placeholder:text-neutral/45",
            errors.text
              ? "border-red-400 focus:border-red-500 focus:ring-[3px] focus:ring-red-500/15"
              : "border-border focus:border-violet focus:ring-[3px] focus:ring-violet/15",
          )}
        />

        <div className="h-1 w-full overflow-hidden rounded-full bg-muted">
          <div
            className={cn(
              "h-full rounded-full transition-all duration-300",
              full ? "bg-red-500" : warning ? "bg-amber-500" : "bg-violet",
            )}
            style={{ width: `${ratio * 100}%` }}
          />
        </div>

        {errors.text ? (
          <p className="text-xs text-red-600">{errors.text.message}</p>
        ) : submitMessage ? (
          <p className="text-xs text-red-600">{submitMessage}</p>
        ) : (
          <p className="text-xs text-neutral/55">يظهر دعاؤك للجميع بعد المراجعة.</p>
        )}
      </div>

      <Button type="submit" size="lg" disabled={!isValid || mutation.isPending}>
        {mutation.isPending ? "جارٍ الإرسال…" : "أرسل دعاءك"}
      </Button>
    </form>
  );
};
