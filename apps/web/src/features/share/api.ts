import { apiPost } from "@/shared/api/axios";

export type SubmitPrayerInput = {
  text: string;
  category?: string;
  type?: string;
};

export type SubmitPrayerResponse = {
  id: string;
  status: string;
  created: string;
};

export const submitPrayer = (input: SubmitPrayerInput) =>
  apiPost<SubmitPrayerResponse>("/prayers", input);
