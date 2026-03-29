"use client";

import { useEffect, useState } from "react";
import { Clock, Sparkles } from "lucide-react";
import QuizCard from "@/components/QuizCard";
import { getQuizzes } from "@/lib/api";
import type { QuizCard as QuizCardType } from "@/lib/api";

export default function HistoryPage() {
  const [quizzes, setQuizzes] = useState<QuizCardType[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getQuizzes(50)
      .then(setQuizzes)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="mx-auto max-w-2xl px-4 py-8 space-y-6">
      <section className="space-y-1">
        <div className="flex items-center gap-2">
          <Clock className="h-5 w-5 text-primary" />
          <h1 className="text-2xl font-bold tracking-tight text-foreground">歷史測驗</h1>
        </div>
        <p className="text-sm text-muted-foreground">所有已發布的測驗，按日期排序。</p>
      </section>

      {loading ? (
        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="rounded-xl border bg-card p-4 animate-pulse">
              <div className="h-4 bg-secondary rounded w-20 mb-3" />
              <div className="h-5 bg-secondary rounded w-3/4 mb-2" />
              <div className="h-4 bg-secondary rounded w-full" />
            </div>
          ))}
        </div>
      ) : quizzes.length > 0 ? (
        <div className="space-y-3">
          {quizzes.map((quiz) => (
            <QuizCard key={quiz.id} quiz={quiz} />
          ))}
        </div>
      ) : (
        <div className="rounded-xl border border-dashed bg-card p-8 text-center">
          <Sparkles className="h-8 w-8 text-muted-foreground/50 mx-auto mb-3" />
          <p className="text-sm text-muted-foreground">暫時沒有已發布的測驗。</p>
        </div>
      )}
    </div>
  );
}
