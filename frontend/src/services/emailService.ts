import type { EmailRequest, EmailResponse } from "../types/email";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function generateEmail(request: EmailRequest): Promise<EmailResponse> {
  const res = await fetch(`${BASE_URL}/api/v1/email/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(error.detail ?? `Request failed: ${res.status}`);
  }

  return res.json();
}
