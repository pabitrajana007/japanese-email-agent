export type RecipientContext =
  | "colleague"
  | "direct manager"
  | "senior executive"
  | "external client"
  | "new business contact";

export interface EmailRequest {
  message: string;
  recipient_context: RecipientContext;
}

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

export type ToneKey = "formal" | "keigo" | "sonkeigo";

export interface ToneOption {
  key: ToneKey;
  label: string;
  jp: string;
  desc: string;
}
