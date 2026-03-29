"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getTodayQuiz } from "@/lib/api";

export default function TodayQuizPage() {
  const router = useRouter();

  useEffect(() => {
    getTodayQuiz()
      .then((quiz) => {
        if (quiz) {
          router.replace(`/quiz/${quiz.slug}`);
        } else {
          router.replace("/");
        }
      })
      .catch(() => router.replace("/"));
  }, [router]);

  return (
    <div className="mx-auto max-w-2xl px-4 py-20 text-center">
      <div className="animate-pulse space-y-3">
        <div className="h-6 bg-secondary rounded w-48 mx-auto" />
        <div className="h-4 bg-secondary rounded w-32 mx-auto" />
      </div>
    </div>
  );
}
