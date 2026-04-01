import axios from "axios";
import type { ApiErrorResponse } from "../types/api";

export const apiClient = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
});

// Parse the error envelope so callers always get a structured ApiError
apiClient.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (axios.isAxiosError(error) && error.response) {
      const data = error.response.data as ApiErrorResponse;
      if (data?.error) {
        return Promise.reject(data.error);
      }
    }
    return Promise.reject({
      code: "NETWORK_ERROR",
      message: "A network error occurred. Please try again.",
    });
  }
);
