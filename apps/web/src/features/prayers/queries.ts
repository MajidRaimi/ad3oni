import { queryOptions } from "@tanstack/react-query";
import { fetchPrayers, fetchRandomPrayer } from "./api";
import type { PrayerListParams, RandomPrayerParams } from "./types";

export const prayersQueryOptions = (params: PrayerListParams = {}) =>
  queryOptions({
    queryKey: ["prayers", "list", params],
    queryFn: () => fetchPrayers(params),
    staleTime: 60_000,
  });

export const randomPrayerQueryOptions = (params: RandomPrayerParams = {}) =>
  queryOptions({
    queryKey: ["prayers", "random", params],
    queryFn: () => fetchRandomPrayer(params),
    staleTime: Infinity,
  });
