import { createFileRoute } from "@tanstack/react-router"
import { SlideColorPalette } from "../deck/layouts/SlideColorPalette"

export const Route = createFileRoute("/color")({ component: SlideColorPalette })
