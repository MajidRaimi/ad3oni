export type Group = {
  id: string;
  name: string;
  slug: string;
};

export type Category = {
  id: string;
  name: string;
  slug: string;
  group?: Group | null;
};

export type PrayerType = {
  id: string;
  name: string;
  slug: string;
};

export type Prayer = {
  id: string;
  text: string;
  status: string;
  category?: Category | null;
  type?: PrayerType | null;
  created: string;
  updated: string;
};

export type Page<T> = {
  items: T[];
  page: number;
  perPage: number;
  totalItems: number;
  totalPages: number;
};

export type PrayerSort = "-created" | "created" | "-updated" | "updated";

export type PrayerListParams = {
  category?: string;
  type?: string;
  group?: string;
  q?: string;
  page?: number;
  perPage?: number;
  sort?: PrayerSort;
};

export type RandomPrayerParams = {
  category?: string;
  type?: string;
};
