import { createFileRoute } from "@tanstack/react-router"
import { SlideResources } from "../deck/layouts/SlideResources"

export const Route = createFileRoute("/resources")({ component: SlideResources })
