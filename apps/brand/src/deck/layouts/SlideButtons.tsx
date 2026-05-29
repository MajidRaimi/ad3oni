import { ArrowLeft, Bell, HandHeart } from "lucide-react"
import { Button } from "@/components/ui/button"
import { SlideBody, SlideHeader } from "../primitives"

const variants = [
  { v: "default" as const, ar: "أساسي" },
  { v: "secondary" as const, ar: "ثانوي" },
  { v: "outline" as const, ar: "محدد" },
  { v: "ghost" as const, ar: "شبحي" },
  { v: "link" as const, ar: "رابط" },
  { v: "destructive" as const, ar: "تحذيري" },
]

export const SlideButtons = () => (
  <SlideBody>
    <SlideHeader no={7} ar="الأزرار" en="Buttons" title="الأزرار" titleEn="Buttons" />

    <div className="mt-11 grid flex-1 grid-cols-[1.4fr_1fr] gap-10">
      <div className="flex flex-col gap-8">
        <div className="flex flex-col gap-4">
          <span className="text-[17px] font-bold text-royal">الأنواع</span>
          <div className="flex flex-wrap items-center gap-4">
            {variants.map((x) => (
              <div key={x.v} className="flex flex-col items-center gap-2">
                <Button variant={x.v}>ادعُ الآن</Button>
                <span className="text-[13px] text-neutral/55">{x.ar}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="flex flex-col gap-4">
          <span className="text-[17px] font-bold text-royal">الأحجام والأيقونات</span>
          <div className="flex flex-wrap items-center gap-4">
            <Button size="sm">صغير</Button>
            <Button size="default">عادي</Button>
            <Button size="lg">كبير</Button>
            <Button size="icon" aria-label="تذكير"><Bell /></Button>
            <Button><HandHeart /> مع أيقونة</Button>
            <Button variant="secondary">التالي <ArrowLeft /></Button>
            <Button disabled>معطّل</Button>
          </div>
        </div>
      </div>

      <div className="dark flex flex-col gap-5 rounded-3xl bg-night p-9">
        <span className="text-[15px] font-bold text-lilac">على سطح ليلي</span>
        <div className="flex flex-col gap-4">
          <Button className="w-full">ادعُ الآن</Button>
          <Button variant="secondary" className="w-full">أضف تذكيرا</Button>
          <Button variant="outline" className="w-full">شارك الدعاء</Button>
          <Button variant="ghost" className="w-full">لاحقا</Button>
        </div>
      </div>
    </div>
  </SlideBody>
)
