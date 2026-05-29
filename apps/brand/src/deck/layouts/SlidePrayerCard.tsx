import { Bell, HandHeart, Share2 } from "lucide-react"
import { Wordmark } from "../Wordmark"
import { SlideBody, SlideHeader } from "../primitives"

export const SlidePrayerCard = () => (
  <SlideBody>
    <SlideHeader no={9} ar="بطاقة الدعاء" en="Prayer Card" title="بطاقة دعاء اليوم" titleEn="Daily Du'a Card" />

    <div className="mt-10 grid flex-1 grid-cols-[1fr_1.3fr] items-center gap-16">
      <div className="flex justify-center">
        <div className="night-bg flex w-[360px] flex-col gap-7 rounded-[40px] p-9 text-paper shadow-[0_30px_70px_rgba(7,1,42,0.4)]">
          <div className="flex items-center justify-between">
            <Wordmark color="paper" size={36} />
            <Bell size={22} className="text-paper/60" />
          </div>
          <div className="flex flex-col items-center gap-4 py-4 text-center">
            <span className="font-mono text-[12px] tracking-[0.3em] text-lilac uppercase">دعاء اليوم</span>
            <div className="flex items-center gap-3" dir="rtl">
              <span className="font-display text-[56px] leading-none text-paper/60">&#123;</span>
              <p className="m-0 font-display text-[30px] leading-[1.7] text-paper">
                اللهم اجعل القرآن ربيع قلبي
              </p>
              <span className="font-display text-[56px] leading-none text-paper/60">&#125;</span>
            </div>
          </div>
          <div className="flex gap-3">
            <button className="flex flex-1 items-center justify-center gap-2 rounded-full bg-lilac py-3 text-[16px] font-bold text-night">
              <HandHeart size={18} /> أمّن
            </button>
            <button className="flex items-center justify-center rounded-full border border-paper/25 px-4 text-paper">
              <Share2 size={18} />
            </button>
          </div>
        </div>
      </div>

      <div className="flex flex-col gap-7">
        <p className="m-0 text-[24px] leading-[1.9] text-neutral/80">
          كل عناصر الهوية تجتمع هنا: الكلمة علامة، القوسان، الخط، والألوان. بطاقة واحدة تختصر العلامة كلها،
          جاهزة للمشاركة على أي منصة.
        </p>
        <div className="grid grid-cols-2 gap-5">
          <div className="flex flex-col gap-2 rounded-2xl border border-royal/10 bg-royal/[0.03] p-6">
            <span className="text-[17px] font-bold text-royal">بطاقة مشاركة</span>
            <span className="text-[15px] leading-[1.7] text-neutral/65">مربعة 1:1 للسوشال، خلفية ليلية وقوسان فيروزيان.</span>
          </div>
          <div className="flex flex-col gap-2 rounded-2xl border border-royal/10 bg-royal/[0.03] p-6">
            <span className="text-[17px] font-bold text-royal">إشعار يومي</span>
            <span className="text-[15px] leading-[1.7] text-neutral/65">نبرة لطيفة، أيقونة جرس، ووقت يختاره المستخدم.</span>
          </div>
        </div>
      </div>
    </div>
  </SlideBody>
)
