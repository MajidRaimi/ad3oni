import { createFileRoute } from "@tanstack/react-router"
import { SlideWordmark } from "../deck/layouts/SlideWordmark"

export const Route = createFileRoute("/wordmark")({ component: SlideWordmark })
