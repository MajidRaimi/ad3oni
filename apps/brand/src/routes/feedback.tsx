import { createFileRoute } from "@tanstack/react-router"
import { SlideFeedback } from "../deck/layouts/SlideFeedback"

export const Route = createFileRoute("/feedback")({ component: SlideFeedback })
