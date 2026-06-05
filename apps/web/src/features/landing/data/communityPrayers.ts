export type CommunityPrayer = {
  id: string;
  text: string;
  category: string;
  source?: string;
};

export const communityPrayers: CommunityPrayer[] = [
  {
    id: "sample-1",
    text: "اللهم اشرح صدري، ويسّر أمري، وارزقني طمأنينة.",
    category: "القلق والهمّ",
  },
  {
    id: "sample-2",
    text: "اللهم لك الحمد على نعمك، واجعلني من الشاكرين.",
    category: "الشكر",
  },
  {
    id: "sample-3",
    text: "اللهم ارزقني رزقًا حلالًا طيبًا واسعًا مباركًا.",
    category: "الرزق",
  },
  {
    id: "sample-4",
    text: "اللهم احفظ والديّ، واجعلني بارًّا بهما.",
    category: "الوالدان",
  },
  {
    id: "sample-5",
    text: "اللهم ثبّت قلبي على دينك حتى ألقاك.",
    category: "الثبات",
  },
  {
    id: "sample-6",
    text: "اللهم اشفِ كل مريض، وفرّج همّ كل مكروب.",
    category: "الشفاء",
  },
  {
    id: "sample-7",
    text: "اللهم وفّقني لما تحب وترضى.",
    category: "التوفيق",
  },
  {
    id: "sample-8",
    text: "اللهم إنك عفوٌّ كريم تحب العفو فاعفُ عني.",
    category: "المغفرة",
  },
  {
    id: "sample-9",
    text: "اللهم انفعني بما علّمتني، وزدني علمًا نافعًا.",
    category: "العلم",
  },
  {
    id: "sample-10",
    text: "اللهم ارزقني صبرًا جميلًا ورضًا بقضائك.",
    category: "الصبر",
  },
  {
    id: "sample-11",
    text: "اللهم اهدني وسدّدني، واجعلني هاديًا مهديًّا.",
    category: "الهداية",
  },
  {
    id: "sample-12",
    text: "اللهم اختم لي بخير، واجعل خير أيامي يوم ألقاك.",
    category: "حسن الخاتمة",
  },
  {
    id: "sample-13",
    text: "اللهم ارزقني ذريةً صالحةً تقرّ بها عيني.",
    category: "الذرية",
  },
  {
    id: "sample-14",
    text: "اللهم أنزل على قلبي سكينة، وثبّتني عند الفتن.",
    category: "السكينة",
  },
];
