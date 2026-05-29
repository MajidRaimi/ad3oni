import { createFileRoute } from "@tanstack/react-router"
import { SlideStory } from "../deck/layouts/SlideStory"

export const Route = createFileRoute("/story")({ component: SlideStory })
