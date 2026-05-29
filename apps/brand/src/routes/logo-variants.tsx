import { createFileRoute } from "@tanstack/react-router"
import { SlideLogoVariants } from "../deck/layouts/SlideLogoVariants"

export const Route = createFileRoute("/logo-variants")({ component: SlideLogoVariants })
