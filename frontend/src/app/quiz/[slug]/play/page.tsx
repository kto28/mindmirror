"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, ArrowRight, Loader2, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { getQuizBySlug, submitQuiz } from "@/lib/api";
import type { QuizDetail } from "@/lib/api";
import { cn } from "@/lib/utils";
import Link from "next/link";

export default function QuizPlayPage() {
  const params = useParams();
  const router = useRouter();
  const slug = params.slug as string;

  const [quiz, setQuiz] = useState<QuizDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!slug) return;
    getQuizBySlug(slug)
      .then(setQuiz)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [slug]);

  const questions = quiz?.questions || [];
  const currentQuestion = questions[currentIndex];
  const totalQuestions = questions.length;
  const progress = totalQuestions > 0 ? ((currentIndex + 1) / totalQuestions) * 100 : 0;
  const allAnswered = questions.every((q) => answers[q.id] !== undefined);
  const currentAnswered = currentQuestion ? answers[currentQuestion.id] !== undefined : false;

  const selectOption = useCallback((questionId: number, optionId: number) => {
    setAnswers((prev) => ({ ...prev, [questionId]: optionId }));
  }, []);

  const goNext = useCallback(() => {
    if (currentIndex < totalQuestions - 1) {
      setCurrentIndex((i) => i + 1);
    }
  }, [currentIndex, totalQuestions]);

  const goPrev = useCallback(() => {
    if (currentIndex > 0) {
      setCurrentIndex((i) => i - 1);
    }
  }, [currentIndex]);

  const handleSubmit = useCallback(async () => {
    if (!quiz || !allAnswered) return;
    setSubmitting(true);
    try {
      const answerList = Object.entries(answers).map(([qid, oid]) => ({
        question_id: parseInt(qid),
        selected_option_id: oid,
      }));
      const result = await submitQuiz(slug, answerList);
      router.push(`/result/${result.session_id}`);
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "提交失敗";
      setError(msg);
      setSubmitting(false);
    }
  }, [quiz, allAnswered, answers, slug, router]);

  if (loading) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-20 text-center">
        <Loader2 className="h-8 w-8 text-primary mx-auto animate-spin" />
        <p className="text-sm text-muted-foreground mt-3">載入題目中...</p>
      </div>
    );
  }

  if (error || !quiz) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-20 text-center">
        <Sparkles className="h-10 w-10 text-muted-foreground/50 mx-auto mb-4" />
        <h2 className="text-lg font-semibold mb-2">載入失敗</h2>
        <p className="text-sm text-muted-foreground mb-6">{error}</p>
        <Link href="/">
          <Button variant="outline">返回首頁</Button>
        </Link>
      </div>
    );
  }

  if (!currentQuestion) return null;

  return (
    <div className="mx-auto max-w-2xl px-4 py-6 space-y-6">
      {/* Progress bar */}
      <div className="space-y-2">
        <div className="flex items-center justify-between text-xs text-muted-foreground">
          <span>{quiz.title}</span>
          <span>{currentIndex + 1} / {totalQuestions}</span>
        </div>
        <Progress value={progress} />
      </div>

      {/* Question card */}
      <Card className="border-0 shadow-md">
        <CardContent className="p-6 sm:p-8">
          <h2 className="text-lg sm:text-xl font-semibold text-foreground leading-snug mb-6">
            {currentQuestion.question_text}
          </h2>

          <div className="space-y-3">
            {currentQuestion.options.map((option) => {
              const isSelected = answers[currentQuestion.id] === option.id;
              return (
                <button
                  key={option.id}
                  onClick={() => selectOption(currentQuestion.id, option.id)}
                  className={cn(
                    "w-full text-left rounded-xl border-2 p-4 transition-all duration-200",
                    "hover:border-primary/40 hover:bg-primary/5",
                    "active:scale-[0.98]",
                    isSelected
                      ? "border-primary bg-primary/10 shadow-sm"
                      : "border-border bg-card"
                  )}
                >
                  <span className={cn(
                    "text-sm leading-relaxed",
                    isSelected ? "text-foreground font-medium" : "text-foreground/80"
                  )}>
                    {option.option_text}
                  </span>
                </button>
              );
            })}
          </div>
        </CardContent>
      </Card>

      {/* Navigation */}
      <div className="flex items-center justify-between gap-3 pb-4">
        <Button
          variant="outline"
          onClick={goPrev}
          disabled={currentIndex === 0}
          className="gap-1.5"
        >
          <ArrowLeft className="h-4 w-4" />
          上一題
        </Button>

        {currentIndex < totalQuestions - 1 ? (
          <Button
            onClick={goNext}
            disabled={!currentAnswered}
            className="gap-1.5"
          >
            下一題
            <ArrowRight className="h-4 w-4" />
          </Button>
        ) : (
          <Button
            onClick={handleSubmit}
            disabled={!allAnswered || submitting}
            className="gap-1.5"
          >
            {submitting ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                計算中...
              </>
            ) : (
              <>
                查看結果
                <Sparkles className="h-4 w-4" />
              </>
            )}
          </Button>
        )}
      </div>
    </div>
  );
}
