import { createFileRoute } from "@tanstack/react-router"
import { SlideRadius } from "../deck/layouts/SlideRadius"

export const Route = createFileRoute("/radius")({ component: SlideRadius })
