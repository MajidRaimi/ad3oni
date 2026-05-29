import { createFileRoute } from "@tanstack/react-router"
import { SlideColorRatios } from "../deck/layouts/SlideColorRatios"

export const Route = createFileRoute("/color-ratios")({ component: SlideColorRatios })
