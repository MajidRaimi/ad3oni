import { Braces, Download, FileJson, Github, Type } from "lucide-react"
import { Button } from "@/components/ui/button"
import { buildTokensCss, buildTokensJson, downloadFile } from "../downloads"
import { SlideBody, SlideHeader } from "../primitives"

const REPO = "https://github.com/MajidRaimi/ad3oni"

export const SlideResources = () => (
  <SlideBody>
    <SlideHeader no={10} ar="المصادر" en="Resources" title="المصادر والتنزيلات" titleEn="Resources & Downloads" />

    <div className="mt-12 grid flex-1 grid-cols-3 gap-7">
      <div className="flex flex-col justify-between rounded-3xl border border-royal/10 bg-royal/[0.03] p-9">
        <div className="flex flex-col gap-3">
          <Braces size={34} className="text-royal" />
          <span className="text-[22px] font-bold text-royal">رموز Tailwind</span>
          <span className="text-[16px] leading-[1.7] text-neutral/65">كتلة <span dir="ltr" className="font-mono">@theme</span> جاهزة للصق في Tailwind v4.</span>
        </div>
        <Button className="mt-6 w-full" onClick={() => downloadFile("ad3oni-theme.css", buildTokensCss(), "text/css")}>
          <Download /> theme.css
        </Button>
      </div>

      <div className="flex flex-col justify-between rounded-3xl border border-royal/10 bg-royal/[0.03] p-9">
        <div className="flex flex-col gap-3">
          <FileJson size={34} className="text-royal" />
          <span className="text-[22px] font-bold text-royal">رموز JSON</span>
          <span className="text-[16px] leading-[1.7] text-neutral/65">الألوان والخطوط والمقاييس كـ JSON لأي أداة.</span>
        </div>
        <Button variant="secondary" className="mt-6 w-full" onClick={() => downloadFile("ad3oni-tokens.json", buildTokensJson(), "application/json")}>
          <Download /> tokens.json
        </Button>
      </div>

      <div className="flex flex-col justify-between rounded-3xl border border-royal/10 bg-royal/[0.03] p-9">
        <div className="flex flex-col gap-3">
          <Type size={34} className="text-royal" />
          <span className="text-[22px] font-bold text-royal">الخطوط</span>
          <span className="text-[16px] leading-[1.7] text-neutral/65">رقعة وتجوال، مفتوحة المصدر عبر Google Fonts.</span>
        </div>
        <div className="mt-6 flex flex-col gap-3">
          <Button variant="outline" className="w-full" asChild>
            <a href="https://fonts.google.com/specimen/Rakkas" target="_blank" rel="noreferrer">رقعة · Rakkas</a>
          </Button>
          <Button variant="outline" className="w-full" asChild>
            <a href="https://fonts.google.com/specimen/Tajawal" target="_blank" rel="noreferrer">تجوال · Tajawal</a>
          </Button>
        </div>
      </div>
    </div>

    <a
      href={REPO}
      target="_blank"
      rel="noreferrer"
      className="mt-7 flex items-center justify-center gap-3 rounded-2xl bg-night py-5 text-[18px] font-medium text-paper transition-colors hover:bg-royal"
    >
      <Github size={22} /> المستودع المفتوح · github.com/MajidRaimi/ad3oni
    </a>
  </SlideBody>
)
