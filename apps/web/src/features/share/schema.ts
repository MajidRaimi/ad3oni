import { z } from "zod";

export const MIN_LENGTH = 3;
export const MAX_LENGTH = 280;

const allowedPattern =
  /^[؀-ۿݐ-ݿࢠ-ࣿﭐ-﷿ﹰ-﻿\s،؛؟!.…«»()ـ]+$/u;
const arabicLetter = /[ء-يٱ-ۓۺ-ۼ]/u;

export const sharePrayerSchema = z.object({
  text: z
    .string()
    .superRefine((raw, ctx) => {
      const value = raw.trim();

      if (value.length > 0 && !allowedPattern.test(value)) {
        ctx.addIssue({ code: "custom", message: "اكتب بالعربية فقط" });
        return;
      }
      if (value.length > 0 && !arabicLetter.test(value)) {
        ctx.addIssue({ code: "custom", message: "اكتب دعاءً بالعربية" });
        return;
      }
      if (value.length < MIN_LENGTH) {
        ctx.addIssue({ code: "custom", message: "الدعاء قصير جدًا" });
        return;
      }
      if (value.length > MAX_LENGTH) {
        ctx.addIssue({ code: "custom", message: "تجاوزت الحد المسموح به" });
      }
    })
    .transform((raw) => raw.trim()),
});

export type SharePrayerValues = z.infer<typeof sharePrayerSchema>;
