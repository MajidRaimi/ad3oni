import { dehydrate, HydrationBoundary } from "@tanstack/react-query";
import { getQueryClient } from "@/shared/api/query-client";
import {
  prayersQueryOptions,
  randomPrayerQueryOptions,
} from "@/features/prayers/queries";
import { LandingPage } from "@/features/landing/LandingPage";

export const dynamic = "force-dynamic";

export default async function Home() {
  const queryClient = getQueryClient();

  await Promise.all([
    queryClient.prefetchQuery(randomPrayerQueryOptions()),
    queryClient.prefetchQuery(
      prayersQueryOptions({ perPage: 14, sort: "-created" }),
    ),
  ]);

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <LandingPage />
    </HydrationBoundary>
  );
}
