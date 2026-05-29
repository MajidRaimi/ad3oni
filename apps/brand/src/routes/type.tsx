import { createFileRoute } from "@tanstack/react-router"
import { SlideTypeSystem } from "../deck/layouts/SlideTypeSystem"

export const Route = createFileRoute("/type")({ component: SlideTypeSystem })
