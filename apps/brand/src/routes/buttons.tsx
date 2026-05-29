import { createFileRoute } from "@tanstack/react-router"
import { SlideButtons } from "../deck/layouts/SlideButtons"

export const Route = createFileRoute("/buttons")({ component: SlideButtons })
