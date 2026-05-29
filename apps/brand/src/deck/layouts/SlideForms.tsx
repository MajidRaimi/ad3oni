import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Checkbox } from "@/components/ui/checkbox"
import { SlideBody, SlideHeader } from "../primitives"

export const SlideForms = () => (
  <SlideBody>
    <SlideHeader no={7} ar="النماذج" en="Forms" title="النماذج والحقول" titleEn="Forms & Inputs" />

    <div className="mt-11 grid flex-1 grid-cols-2 gap-10">
      <div className="flex flex-col gap-6 rounded-3xl border border-royal/10 bg-white p-9 shadow-[0_18px_44px_rgba(7,1,42,0.07)]">
        <div className="flex flex-col gap-2">
          <Label htmlFor="name" className="text-[16px]">الاسم</Label>
          <Input id="name" placeholder="اكتب اسمك" defaultValue="ماجد" className="h-11 text-[16px]" />
        </div>
        <div className="flex flex-col gap-2">
          <Label htmlFor="dua" className="text-[16px]">شاركنا دعاءك</Label>
          <Textarea id="dua" placeholder="اكتب دعاءك هنا…" className="min-h-[110px] text-[16px]" />
          <span className="text-[13px] text-neutral/50">يظهر للجميع بعد المراجعة.</span>
        </div>
        <div className="flex flex-col gap-2">
          <Label htmlFor="err" className="text-[16px]">البريد</Label>
          <Input id="err" aria-invalid defaultValue="majid@" className="h-11 text-[16px]" />
          <span className="text-[13px] text-destructive">صيغة البريد غير صحيحة.</span>
        </div>
      </div>

      <div className="flex flex-col gap-6">
        <div className="flex flex-col gap-5 rounded-3xl border border-royal/10 bg-royal/[0.03] p-9">
          <span className="text-[17px] font-bold text-royal">الخيارات</span>
          <div className="flex items-center justify-between">
            <Label htmlFor="daily" className="text-[17px] text-neutral/80">تذكير يومي</Label>
            <Switch id="daily" defaultChecked />
          </div>
          <div className="flex items-center justify-between">
            <Label htmlFor="night" className="text-[17px] text-neutral/80">دعاء قبل النوم</Label>
            <Switch id="night" />
          </div>
          <div className="h-px bg-royal/10" />
          <div className="flex items-center gap-3">
            <Checkbox id="agree" defaultChecked />
            <Label htmlFor="agree" className="text-[17px] text-neutral/80">أوافق على شروط المشاركة</Label>
          </div>
          <div className="flex items-center gap-3">
            <Checkbox id="news" />
            <Label htmlFor="news" className="text-[17px] text-neutral/80">أرسلوا لي الجديد</Label>
          </div>
        </div>
        <Button size="lg" className="h-12 text-[17px]">احفظ التفضيلات</Button>
      </div>
    </div>
  </SlideBody>
)
