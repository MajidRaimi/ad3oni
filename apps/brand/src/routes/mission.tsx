import { createFileRoute } from "@tanstack/react-router"
import { SlideMission } from "../deck/layouts/SlideMission"

export const Route = createFileRoute("/mission")({ component: SlideMission })
