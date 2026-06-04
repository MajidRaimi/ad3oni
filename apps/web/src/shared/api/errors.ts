import axios from "axios";

export type ApiErrorCode = "rate_limited" | "validation_error" | "unknown";

export type ApiError = {
  code: ApiErrorCode;
  message: string;
  status?: number;
};

type ApiErrorPayload = {
  error?: { code?: string; message?: string };
};

export const toApiError = (error: unknown): ApiError => {
  if (axios.isAxiosError(error)) {
    const payload = error.response?.data as ApiErrorPayload | undefined;
    const code = payload?.error?.code;
    return {
      code:
        code === "rate_limited" || code === "validation_error"
          ? code
          : "unknown",
      message: payload?.error?.message ?? error.message,
      status: error.response?.status,
    };
  }
  return { code: "unknown", message: "حدث خطأ غير متوقع" };
};
