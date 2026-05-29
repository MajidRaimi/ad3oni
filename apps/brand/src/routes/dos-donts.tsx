import { createFileRoute } from "@tanstack/react-router"
import { SlideDosDonts } from "../deck/layouts/SlideDosDonts"

export const Route = createFileRoute("/dos-donts")({ component: SlideDosDonts })
