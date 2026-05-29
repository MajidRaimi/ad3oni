import { createFileRoute } from "@tanstack/react-router"
import { SlideCards } from "../deck/layouts/SlideCards"

export const Route = createFileRoute("/cards")({ component: SlideCards })
