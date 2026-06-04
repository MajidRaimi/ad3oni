"use client";

import { useMutation } from "@tanstack/react-query";
import { submitPrayer, type SubmitPrayerInput } from "./api";

export const useSubmitPrayer = () =>
  useMutation({
    mutationFn: (input: SubmitPrayerInput) => submitPrayer(input),
  });
