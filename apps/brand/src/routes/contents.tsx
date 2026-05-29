import { createFileRoute } from "@tanstack/react-router"
import { SlideContents } from "../deck/layouts/SlideContents"

export const Route = createFileRoute("/contents")({ component: SlideContents })
