import { Check, X } from "lucide-react"
import type { ReactNode } from "react"
import { Wordmark } from "../Wordmark"
import { SlideBody, SlideHeader } from "../primitives"

const dos: Array<{ ar: string; node: ReactNode }> = [
  { ar: "اترك مساحة سلبية وفيرة حول الدعاء.", node: <div className="flex h-full items-center justify-center"><Wordmark color="royal" size={40} /></div> },
  { ar: "أرجواني مهيمن، بنفسجي وليلكي لكنة.", node: (
    <div className="flex h-full overflow-hidden rounded-lg"><div className="flex-[6] bg-royal" /><div className="flex-1 bg-violet" /><div className="flex-1 bg-lilac" /></div>
  ) },
  { ar: "تباين عالٍ بين النص والخلفية.", node: <div className="flex h-full items-center justify-center rounded-lg bg-night"><span className="text-[22px] font-bold text-paper">دعاء اليوم</span></div> },
]
const donts: Array<{ ar: string; node: ReactNode }> = [
  { ar: "لا تزدحم العناصر دون تنفّس.", node: <div className="grid h-full grid-cols-4 content-center gap-1 p-2">{Array.from({ length: 12 }).map((_, i) => <div key={i} className="h-4 rounded-sm bg-royal/40" />)}</div> },
  { ar: "لا تجعل الألوان متساوية بلا تراتب.", node: (
    <div className="flex h-full overflow-hidden rounded-lg"><div className="flex-1 bg-royal" /><div className="flex-1 bg-violet" /><div className="flex-1 bg-lilac" /><div className="flex-1 bg-destructive" /></div>
  ) },
  { ar: "لا تستخدم تباينا منخفضا.", node: <div className="flex h-full items-center justify-center rounded-lg bg-royal/20"><span className="text-[22px] font-bold text-royal/35">دعاء اليوم</span></div> },
]

const Example = ({ d, tone }: { d: { ar: string; node: ReactNode }; tone: "do" | "dont" }) => (
  <div
    className={`flex h-[136px] items-center gap-5 rounded-2xl border p-4 ${
      tone === "do" ? "border-violet/20 bg-violet/[0.05]" : "border-destructive/20 bg-destructive/[0.04]"
    }`}
  >
    <div className="h-[104px] w-[170px] shrink-0 overflow-hidden rounded-lg border border-royal/10 bg-white">{d.node}</div>
    <span className="text-[18px] leading-[1.6] text-neutral/75">{d.ar}</span>
  </div>
)

const Pill = ({ tone }: { tone: "do" | "dont" }) => (
  <div className="flex items-center gap-3">
    <span className={`flex h-10 w-10 items-center justify-center rounded-full text-paper ${tone === "do" ? "bg-violet" : "bg-destructive"}`}>
      {tone === "do" ? <Check size={20} strokeWidth={3} /> : <X size={20} strokeWidth={3} />}
    </span>
    <span className={`text-[22px] font-bold ${tone === "do" ? "text-violet" : "text-destructive"}`}>
      {tone === "do" ? "افعل" : "لا تفعل"}
    </span>
  </div>
)

export const SlideDosDonts = () => (
  <SlideBody>
    <SlideHeader no={8} ar="افعل ولا تفعل" en="Do / Don't" title="افعل ولا تفعل" titleEn="Do & Don't" />

    <div className="mt-10 flex flex-1 flex-col gap-5">
      <div className="grid grid-cols-2 gap-12">
        <Pill tone="do" />
        <Pill tone="dont" />
      </div>
      {[0, 1, 2].map((i) => (
        <div key={i} className="grid grid-cols-2 gap-12">
          <Example d={dos[i]} tone="do" />
          <Example d={donts[i]} tone="dont" />
        </div>
      ))}
    </div>
  </SlideBody>
)
