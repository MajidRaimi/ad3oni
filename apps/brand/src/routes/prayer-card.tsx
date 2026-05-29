import { createFileRoute } from "@tanstack/react-router"
import { SlidePrayerCard } from "../deck/layouts/SlidePrayerCard"

export const Route = createFileRoute("/prayer-card")({ component: SlidePrayerCard })
