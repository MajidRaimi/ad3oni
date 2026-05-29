import { createFileRoute } from "@tanstack/react-router"
import { SlideTokens } from "../deck/layouts/SlideTokens"

export const Route = createFileRoute("/tokens")({ component: SlideTokens })
