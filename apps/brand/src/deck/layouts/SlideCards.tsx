import { HandHeart, Share2 } from "lucide-react"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { SlideBody, SlideHeader } from "../primitives"

export const SlideCards = () => (
  <SlideBody>
    <SlideHeader no={7} ar="البطاقات" en="Cards" title="البطاقات" titleEn="Cards" />

    <div className="mt-11 grid flex-1 grid-cols-3 gap-8">
      <Card className="justify-between">
        <CardHeader>
          <Badge variant="secondary" className="w-fit">دعاء اليوم</Badge>
          <CardTitle className="mt-2 font-display text-[34px] leading-[1.5] font-normal text-royal">
            اللهم إنك عفو تحب العفو فاعف عني
          </CardTitle>
          <CardDescription className="text-[15px]">رواه الترمذي</CardDescription>
        </CardHeader>
        <CardFooter className="gap-3">
          <Button className="flex-1"><HandHeart /> أمّن</Button>
          <Button variant="outline" size="icon" aria-label="مشاركة"><Share2 /></Button>
        </CardFooter>
      </Card>

      <Card className="border-royal/20 bg-royal/[0.04]">
        <CardHeader>
          <CardTitle className="text-[24px] text-royal">بطاقة مميزة</CardTitle>
          <CardDescription className="text-[15px]">سطح بلكنة أرجوانية خفيفة للبطاقات البارزة.</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-3">
          <div className="flex items-center gap-2">
            <Badge>جديد</Badge>
            <Badge variant="outline">موثّق</Badge>
            <Badge variant="secondary">مميز</Badge>
          </div>
          <p className="m-0 text-[16px] leading-[1.7] text-neutral/70">
            تستعمل لإبراز محتوى مختار دون كسر الإيقاع البصري للصفحة.
          </p>
        </CardContent>
        <CardFooter>
          <Button variant="secondary" className="w-full">اعرف أكثر</Button>
        </CardFooter>
      </Card>

      <div className="dark">
        <Card className="h-full justify-between bg-night">
          <CardHeader>
            <Badge className="w-fit">ليلي</Badge>
            <CardTitle className="mt-2 text-[24px]">بطاقة داكنة</CardTitle>
            <CardDescription className="text-[15px]">نفس المكوّن، سطح ليلي عبر صنف dark.</CardDescription>
          </CardHeader>
          <CardContent>
            <p className="m-0 text-[16px] leading-[1.7] text-card-foreground/70">
              الهوية تتكيف تلقائيا: الذهبي يصبح اللون الأساسي على الخلفيات الداكنة.
            </p>
          </CardContent>
          <CardFooter>
            <Button className="w-full">ادعُ معنا</Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  </SlideBody>
)
