import { createFileRoute } from "@tanstack/react-router"
import { SlideTypeScale } from "../deck/layouts/SlideTypeScale"

export const Route = createFileRoute("/type-scale")({ component: SlideTypeScale })
