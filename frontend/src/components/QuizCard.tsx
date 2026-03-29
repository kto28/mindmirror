"use client";

import Link from "next/link";
import { Clock, ArrowRight } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import type { QuizCard as QuizCardType } from "@/lib/api";

export default function QuizCard({ quiz, featured = false }: { quiz: QuizCardType; featured?: boolean }) {
  return (
    <Card className={featured ? "border-primary/20 shadow-md" : ""}>
      <CardContent className={featured ? "p-6" : "p-4"}>
        {quiz.topic && (
          <span className="inline-block text-xs font-medium text-primary bg-primary/10 rounded-full px-2.5 py-0.5 mb-3">
            {quiz.topic}
          </span>
        )}
        <h3 className={featured ? "text-xl font-semibold mb-2" : "text-base font-semibold mb-1.5"}>
          {quiz.title}
        </h3>
        {quiz.summary && (
          <p className="text-sm text-muted-foreground leading-relaxed mb-4">
            {quiz.summary}
          </p>
        )}
        <div className="flex items-center justify-between">
          <span className="flex items-center gap-1 text-xs text-muted-foreground">
            <Clock className="h-3.5 w-3.5" />
            約 {quiz.estimated_minutes} 分鐘
          </span>
          <Link href={`/quiz/${quiz.slug}`}>
            <Button size={featured ? "default" : "sm"} className="gap-1.5">
              開始測驗
              <ArrowRight className="h-4 w-4" />
            </Button>
          </Link>
        </div>
      </CardContent>
    </Card>
  );
}
