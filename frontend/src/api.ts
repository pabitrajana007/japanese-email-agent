const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export interface EmailVariant {
  subject: string;
  body: string;
  explanation: string;
  politeness_level: number;
}

export interface EmailResponse {
  formal: EmailVariant;
  keigo: EmailVariant;
  sonkeigo: EmailVariant;
  cultural_tip: string;
}

export async function generateEmail(
  message: string,
  recipient: string
): Promise<EmailResponse> {
  const res = await fetch(`${API_URL}/api/email/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, recipient }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(err.detail ?? "Something went wrong");
  }

  return res.json();
}
