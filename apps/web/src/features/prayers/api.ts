import { apiGet } from "@/shared/api/axios";
import type {
  Page,
  Prayer,
  PrayerListParams,
  RandomPrayerParams,
} from "./types";

export const fetchPrayers = (params: PrayerListParams = {}) =>
  apiGet<Page<Prayer>>("/prayers", params);

export const fetchRandomPrayer = (params: RandomPrayerParams = {}) =>
  apiGet<Prayer>("/prayers/random", params);
