import { isAxiosError } from 'axios';

export function getApiErrorMessage(err: unknown, fallback: string): string {
  if (isAxiosError<{ detail?: string }>(err)) {
    const detail = err.response?.data?.detail;
    if (typeof detail === 'string') return detail;
  }
  return fallback;
}