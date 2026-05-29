import { createFileRoute } from "@tanstack/react-router"
import { SlideVoice } from "../deck/layouts/SlideVoice"

export const Route = createFileRoute("/voice")({ component: SlideVoice })
