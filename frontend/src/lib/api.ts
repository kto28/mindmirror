const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

async function fetchAPI<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || "API Error");
  }
  return res.json();
}

export interface QuizCard {
  id: number;
  title: string;
  slug: string;
  topic: string | null;
  summary: string | null;
  cover_image_url: string | null;
  estimated_minutes: number;
  publish_date: string | null;
}

export interface QuizOption {
  id: number;
  option_text: string;
  option_value_code: string;
  order_index: number;
}

export interface QuizQuestion {
  id: number;
  question_text: string;
  order_index: number;
  options: QuizOption[];
}

export interface ResultProfile {
  code: string;
  title: string;
  short_label: string | null;
  description: string | null;
  strengths: string[] | null;
  growth_tips: string[] | null;
  encouragement: string | null;
  share_text: string | null;
}

export interface QuizDetail extends QuizCard {
  intro_text: string | null;
  questions: QuizQuestion[];
  result_profiles: ResultProfile[];
}

export interface SessionResult {
  session_id: string;
  quiz_id: number;
  quiz_title: string;
  quiz_slug: string;
  result_profile: ResultProfile;
  created_at: string;
}

export interface LeadPayload {
  quiz_id?: number;
  session_id?: string;
  name?: string;
  email?: string;
  whatsapp?: string;
  consent: boolean;
}

// --- Public API ---

export function getTodayQuiz(): Promise<QuizCard | null> {
  return fetchAPI("/api/quizzes/today");
}

export function getQuizzes(limit = 20, offset = 0): Promise<QuizCard[]> {
  return fetchAPI(`/api/quizzes?limit=${limit}&offset=${offset}`);
}

export function getQuizBySlug(slug: string): Promise<QuizDetail> {
  return fetchAPI(`/api/quizzes/${slug}`);
}

export function submitQuiz(
  slug: string,
  answers: { question_id: number; selected_option_id: number }[]
): Promise<SessionResult> {
  return fetchAPI(`/api/quizzes/${slug}/submit`, {
    method: "POST",
    body: JSON.stringify({ answers }),
  });
}

export function getResult(sessionId: string): Promise<SessionResult> {
  return fetchAPI(`/api/results/${sessionId}`);
}

export function createLead(data: LeadPayload): Promise<{ id: number }> {
  return fetchAPI("/api/leads", {
    method: "POST",
    body: JSON.stringify(data),
  });
}
