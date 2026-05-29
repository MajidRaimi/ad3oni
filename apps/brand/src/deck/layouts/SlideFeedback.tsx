import { CheckCircle2 } from "lucide-react"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"
import { Skeleton } from "@/components/ui/skeleton"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { SlideBody, SlideHeader } from "../primitives"

export const SlideFeedback = () => (
  <SlideBody>
    <SlideHeader no={7} ar="التغذية الراجعة" en="Feedback" title="التغذية الراجعة والبيانات" titleEn="Feedback & Data" />

    <div className="mt-11 grid flex-1 grid-cols-2 gap-10">
      <div className="flex flex-col gap-6">
        <Alert className="border-violet/30 bg-violet/[0.08]">
          <CheckCircle2 className="text-violet" />
          <AlertTitle className="text-[18px]">تم حفظ تذكيرك</AlertTitle>
          <AlertDescription className="text-[15px]">سنذكّرك بدعاء اليوم كل صباح.</AlertDescription>
        </Alert>

        <Accordion type="single" collapsible defaultValue="a1" className="rounded-2xl border border-royal/10 bg-white px-6">
          <AccordionItem value="a1">
            <AccordionTrigger className="text-[18px]">كيف أضيف دعاء؟</AccordionTrigger>
            <AccordionContent className="text-[15px] text-neutral/70">
              من زر «شاركنا دعاءك»، اكتب الدعاء ومصدره، وسيظهر بعد المراجعة.
            </AccordionContent>
          </AccordionItem>
          <AccordionItem value="a2">
            <AccordionTrigger className="text-[18px]">هل المنصة مجانية؟</AccordionTrigger>
            <AccordionContent className="text-[15px] text-neutral/70">
              نعم، ومفتوحة المصدر بالكامل.
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </div>

      <div className="flex flex-col gap-6">
        <Tabs defaultValue="today">
          <TabsList>
            <TabsTrigger value="today" className="text-[15px]">اليوم</TabsTrigger>
            <TabsTrigger value="week" className="text-[15px]">الأسبوع</TabsTrigger>
            <TabsTrigger value="all" className="text-[15px]">الكل</TabsTrigger>
          </TabsList>
          <TabsContent value="today" className="rounded-2xl border border-royal/10 bg-white p-6 text-[16px] text-neutral/70">
            دعاء اليوم وصل إلى 12,480 قلبا.
          </TabsContent>
          <TabsContent value="week" className="rounded-2xl border border-royal/10 bg-white p-6 text-[16px] text-neutral/70">
            هذا الأسبوع: 84 ألف تذكير.
          </TabsContent>
          <TabsContent value="all" className="rounded-2xl border border-royal/10 bg-white p-6 text-[16px] text-neutral/70">
            منذ البداية: أكثر من مليون دعوة.
          </TabsContent>
        </Tabs>

        <div className="flex flex-col gap-3 rounded-2xl border border-royal/10 bg-white p-6">
          <div className="flex items-center justify-between text-[15px] text-neutral/70">
            <span>تقدّم الورد اليومي</span>
            <span dir="ltr" className="font-mono text-royal">68%</span>
          </div>
          <Progress value={68} />
          <div className="mt-2 flex items-center gap-3">
            <div className="flex -space-x-3 rtl:space-x-reverse">
              {["م", "ر", "س", "ع"].map((a) => (
                <Avatar key={a} className="border-2 border-white">
                  <AvatarFallback className="bg-royal text-[14px] text-paper">{a}</AvatarFallback>
                </Avatar>
              ))}
            </div>
            <Badge variant="secondary">+٤٨ يدعون الآن</Badge>
          </div>
        </div>

        <div className="flex items-center gap-4 rounded-2xl border border-royal/10 bg-white p-6">
          <Skeleton className="h-12 w-12 rounded-full" />
          <div className="flex flex-1 flex-col gap-2">
            <Skeleton className="h-4 w-3/4" />
            <Skeleton className="h-4 w-1/2" />
          </div>
        </div>
      </div>
    </div>
  </SlideBody>
)
