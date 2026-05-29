import { createFileRoute } from "@tanstack/react-router"
import { SlideMotion } from "../deck/layouts/SlideMotion"

export const Route = createFileRoute("/motion")({ component: SlideMotion })
