"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { Clock, ArrowRight, Sparkles } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { getQuizBySlug } from "@/lib/api";
import type { QuizDetail } from "@/lib/api";

export default function QuizDetailPage() {
  const params = useParams();
  const slug = params.slug as string;
  const [quiz, setQuiz] = useState<QuizDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!slug) return;
    getQuizBySlug(slug)
      .then(setQuiz)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [slug]);

  if (loading) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-12">
        <div className="animate-pulse space-y-4">
          <div className="h-5 bg-secondary rounded w-20" />
          <div className="h-8 bg-secondary rounded w-3/4" />
          <div className="h-4 bg-secondary rounded w-full" />
          <div className="h-4 bg-secondary rounded w-2/3" />
          <div className="h-12 bg-secondary rounded w-40 mt-6" />
        </div>
      </div>
    );
  }

  if (error || !quiz) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-20 text-center">
        <Sparkles className="h-10 w-10 text-muted-foreground/50 mx-auto mb-4" />
        <h2 className="text-lg font-semibold mb-2">找不到測驗</h2>
        <p className="text-sm text-muted-foreground mb-6">{error || "該測驗不存在或尚未發布。"}</p>
        <Link href="/">
          <Button variant="outline">返回首頁</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-2xl px-4 py-8 space-y-8">
      {/* Quiz intro */}
      <section className="space-y-4">
        {quiz.topic && (
          <span className="inline-block text-xs font-medium text-primary bg-primary/10 rounded-full px-3 py-1">
            {quiz.topic}
          </span>
        )}
        <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-foreground">
          {quiz.title}
        </h1>
        {quiz.summary && (
          <p className="text-muted-foreground leading-relaxed">{quiz.summary}</p>
        )}
      </section>

      {/* Quiz info card */}
      <Card>
        <CardContent className="p-6 space-y-4">
          {quiz.intro_text && (
            <p className="text-sm text-foreground/80 leading-relaxed">{quiz.intro_text}</p>
          )}
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <span className="flex items-center gap-1.5">
              <Clock className="h-4 w-4" />
              約 {quiz.estimated_minutes} 分鐘
            </span>
            <span className="flex items-center gap-1.5">
              <Sparkles className="h-4 w-4" />
              {quiz.questions.length} 道題目
            </span>
          </div>
          <Link href={`/quiz/${quiz.slug}/play`}>
            <Button size="lg" className="w-full gap-2 mt-2">
              開始作答
              <ArrowRight className="h-5 w-5" />
            </Button>
          </Link>
        </CardContent>
      </Card>

      {/* Disclaimer */}
      <div className="rounded-xl bg-secondary/50 p-4 text-center">
        <p className="text-xs text-muted-foreground leading-relaxed">
          本測驗僅供自我探索與生活反思，不構成任何醫療或心理診斷建議。
        </p>
      </div>
    </div>
  );
}
