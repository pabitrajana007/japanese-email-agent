import { useState } from "react";
import { generateEmail } from "../services/emailService";
import type { EmailRequest, EmailResponse, RecipientContext, ToneKey } from "../types/email";

interface State {
  message: string;
  recipientContext: RecipientContext;
  activeTab: ToneKey;
  result: EmailResponse | null;
  loading: boolean;
  error: string;
}

const INITIAL_STATE: State = {
  message: "",
  recipientContext: "colleague",
  activeTab: "formal",
  result: null,
  loading: false,
  error: "",
};

export function useEmailGenerator() {
  const [state, setState] = useState<State>(INITIAL_STATE);

  function setMessage(message: string) {
    setState((s) => ({ ...s, message }));
  }

  function setRecipientContext(recipientContext: RecipientContext) {
    setState((s) => ({ ...s, recipientContext }));
  }

  function setActiveTab(activeTab: ToneKey) {
    setState((s) => ({ ...s, activeTab }));
  }

  async function generate() {
    if (!state.message.trim()) return;

    setState((s) => ({ ...s, loading: true, error: "", result: null }));

    const request: EmailRequest = {
      message: state.message,
      recipient_context: state.recipientContext,
    };

    try {
      const result = await generateEmail(request);
      setState((s) => ({ ...s, result, loading: false, activeTab: "formal" }));
    } catch (e) {
      const error = e instanceof Error ? e.message : "Something went wrong";
      setState((s) => ({ ...s, error, loading: false }));
    }
  }

  return { state, setMessage, setRecipientContext, setActiveTab, generate };
}
