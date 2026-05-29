import { createFileRoute } from "@tanstack/react-router"
import { SlideForms } from "../deck/layouts/SlideForms"

export const Route = createFileRoute("/forms")({ component: SlideForms })
