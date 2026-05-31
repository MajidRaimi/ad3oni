export type HowItWorksStep = {
  key: string;
  title: string;
  description: string;
};

export const howItWorksSteps: HowItWorksStep[] = [
  {
    key: "write",
    title: "اكتب دعاءك",
    description:
      "شارك دعاءً صادقًا من قلبك، بكلماتك أنت. كل دعاء جميل يستحق أن يصل غيرك.",
  },
  {
    key: "deliver",
    title: "نوصله إلى الناس",
    description:
      "ننشر دعاءك عبر منصّاتنا: إكس، وبوت ديسكورد، والموقع، والتطبيقات القادمة.",
  },
  {
    key: "reward",
    title: "يُدعى به فيصلك الأجر",
    description:
      "كلما دعا به أحدٌ تذكّر ربه، نلت مثل أجره بإذن الله، دون أن ينقص من أجره شيء.",
  },
];
