import axios from "axios";

const baseURL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/v1";

export const api = axios.create({
  baseURL,
  headers: { "Content-Type": "application/json" },
});

export const apiGet = async <T>(
  url: string,
  params?: Record<string, unknown>,
): Promise<T> => {
  const response = await api.get<T>(url, { params });
  return response.data;
};

export const apiPost = async <T>(url: string, body?: unknown): Promise<T> => {
  const response = await api.post<T>(url, body);
  return response.data;
};
