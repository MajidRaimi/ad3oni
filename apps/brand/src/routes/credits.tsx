import { createFileRoute } from "@tanstack/react-router"
import { SlideCredits } from "../deck/layouts/SlideCredits"

export const Route = createFileRoute("/credits")({ component: SlideCredits })
