"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Sparkles, ArrowRight, Clock, BookOpen } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import QuizCard from "@/components/QuizCard";
import type { QuizCard as QuizCardType } from "@/lib/api";
import { getTodayQuiz, getQuizzes } from "@/lib/api";

export default function HomePage() {
  const [todayQuiz, setTodayQuiz] = useState<QuizCardType | null>(null);
  const [recentQuizzes, setRecentQuizzes] = useState<QuizCardType[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [today, recent] = await Promise.all([
          getTodayQuiz().catch(() => null),
          getQuizzes(7).catch(() => []),
        ]);
        setTodayQuiz(today);
        setRecentQuizzes(recent);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <div className="mx-auto max-w-2xl px-4 py-8 space-y-10">
      {/* Hero */}
      <section className="text-center space-y-4 pt-4 pb-2">
        <div className="flex justify-center">
          <div className="h-16 w-16 rounded-2xl bg-gradient-to-br from-primary/20 to-accent flex items-center justify-center">
            <Sparkles className="h-8 w-8 text-primary" />
          </div>
        </div>
        <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-foreground">
          MindMirror
        </h1>
        <p className="text-lg text-muted-foreground">
          每日一測，更了解自己。
        </p>
        <p className="text-sm text-muted-foreground max-w-md mx-auto leading-relaxed">
          透過輕鬆有趣的正向心理測驗，探索你的內在傾向、生活風格與成長方向。
        </p>
      </section>

      {/* Today's Quiz CTA */}
      {loading ? (
        <Card>
          <CardContent className="p-6">
            <div className="animate-pulse space-y-3">
              <div className="h-5 bg-secondary rounded w-24" />
              <div className="h-6 bg-secondary rounded w-3/4" />
              <div className="h-4 bg-secondary rounded w-full" />
              <div className="h-11 bg-secondary rounded w-32 mt-4" />
            </div>
          </CardContent>
        </Card>
      ) : todayQuiz ? (
        <section className="space-y-3">
          <div className="flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-primary" />
            <h2 className="text-lg font-semibold text-foreground">今日測驗</h2>
          </div>
          <QuizCard quiz={todayQuiz} featured />
        </section>
      ) : (
        <Card className="border-dashed">
          <CardContent className="p-6 text-center">
            <Sparkles className="h-8 w-8 text-muted-foreground/50 mx-auto mb-3" />
            <p className="text-sm text-muted-foreground">今天的測驗準備中，請稍後再來看看。</p>
          </CardContent>
        </Card>
      )}

      {/* Recent Quizzes */}
      {recentQuizzes.length > 0 && (
        <section className="space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Clock className="h-5 w-5 text-primary" />
              <h2 className="text-lg font-semibold text-foreground">最近測驗</h2>
            </div>
            <Link href="/history">
              <Button variant="ghost" size="sm" className="text-muted-foreground gap-1">
                查看全部
                <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </div>
          <div className="space-y-3">
            {recentQuizzes
              .filter((q) => q.slug !== todayQuiz?.slug)
              .slice(0, 5)
              .map((quiz) => (
                <QuizCard key={quiz.id} quiz={quiz} />
              ))}
          </div>
        </section>
      )}

      {/* CTA buttons */}
      <section className="flex flex-col sm:flex-row gap-3 pt-2">
        {todayQuiz && (
          <Link href={`/quiz/${todayQuiz.slug}`} className="flex-1">
            <Button size="lg" className="w-full gap-2">
              <Sparkles className="h-5 w-5" />
              開始今日測驗
            </Button>
          </Link>
        )}
        <Link href="/history" className="flex-1">
          <Button size="lg" variant="outline" className="w-full gap-2">
            <Clock className="h-5 w-5" />
            查看歷史測驗
          </Button>
        </Link>
      </section>

      {/* Disclaimer */}
      <section className="rounded-xl bg-secondary/50 p-4 text-center">
        <p className="text-xs text-muted-foreground leading-relaxed">
          本平台內容僅供自我探索與生活反思，不構成任何醫療或心理診斷建議。
        </p>
      </section>
    </div>
  );
}
