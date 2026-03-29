"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import {
  Sparkles,
  Star,
  TrendingUp,
  Heart,
  Share2,
  Link2,
  CheckCircle,
  Loader2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { getResult } from "@/lib/api";
import type { SessionResult } from "@/lib/api";
import LeadForm from "@/components/LeadForm";

export default function ResultPage() {
  const params = useParams();
  const sessionId = params.sessionId as string;
  const [result, setResult] = useState<SessionResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (!sessionId) return;
    getResult(sessionId)
      .then(setResult)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [sessionId]);

  const handleShare = async () => {
    const url = window.location.href;
    const text = result
      ? `我在 MindMirror 測出了「${result.result_profile.title}」！${result.result_profile.share_text || ""}`
      : "來試試 MindMirror 的每日心理測驗！";

    if (navigator.share) {
      try {
        await navigator.share({ title: "MindMirror 測驗結果", text, url });
      } catch {
        // user cancelled
      }
    } else {
      handleCopyLink();
    }
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(window.location.href).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  if (loading) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-20 text-center">
        <Loader2 className="h-8 w-8 text-primary mx-auto animate-spin" />
        <p className="text-sm text-muted-foreground mt-3">載入結果中...</p>
      </div>
    );
  }

  if (error || !result) {
    return (
      <div className="mx-auto max-w-2xl px-4 py-20 text-center">
        <Sparkles className="h-10 w-10 text-muted-foreground/50 mx-auto mb-4" />
        <h2 className="text-lg font-semibold mb-2">找不到結果</h2>
        <p className="text-sm text-muted-foreground mb-6">{error || "該結果不存在。"}</p>
        <Link href="/">
          <Button variant="outline">返回首頁</Button>
        </Link>
      </div>
    );
  }

  const profile = result.result_profile;

  return (
    <div className="mx-auto max-w-2xl px-4 py-8 space-y-6">
      {/* Result hero — ceremonial feel */}
      <section className="text-center space-y-4 py-6">
        <div className="flex justify-center">
          <div className="h-20 w-20 rounded-full bg-gradient-to-br from-primary/20 via-accent to-primary/10 flex items-center justify-center">
            <Sparkles className="h-10 w-10 text-primary" />
          </div>
        </div>
        <p className="text-sm text-muted-foreground">{result.quiz_title}</p>
        <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-foreground">
          {profile.title}
        </h1>
        {profile.short_label && (
          <span className="inline-block text-sm font-medium text-primary bg-primary/10 rounded-full px-4 py-1">
            {profile.short_label}
          </span>
        )}
      </section>

      {/* Description */}
      {profile.description && (
        <Card>
          <CardContent className="p-6">
            <p className="text-sm text-foreground/85 leading-relaxed">
              {profile.description}
            </p>
          </CardContent>
        </Card>
      )}

      {/* Strengths */}
      {profile.strengths && profile.strengths.length > 0 && (
        <Card className="border-primary/15">
          <CardContent className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <Star className="h-5 w-5 text-primary" />
              <h2 className="font-semibold text-foreground">你的優勢</h2>
            </div>
            <ul className="space-y-3">
              {profile.strengths.map((s, i) => (
                <li key={i} className="flex items-start gap-3">
                  <CheckCircle className="h-4 w-4 text-primary mt-0.5 shrink-0" />
                  <span className="text-sm text-foreground/80 leading-relaxed">{s}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {/* Growth tips */}
      {profile.growth_tips && profile.growth_tips.length > 0 && (
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="h-5 w-5 text-primary" />
              <h2 className="font-semibold text-foreground">可提升方向</h2>
            </div>
            <ul className="space-y-3">
              {profile.growth_tips.map((tip, i) => (
                <li key={i} className="flex items-start gap-3">
                  <span className="flex h-5 w-5 items-center justify-center rounded-full bg-accent text-xs font-medium text-accent-foreground shrink-0">
                    {i + 1}
                  </span>
                  <span className="text-sm text-foreground/80 leading-relaxed">{tip}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      {/* Encouragement */}
      {profile.encouragement && (
        <Card className="border-primary/15 bg-gradient-to-br from-card to-accent/20">
          <CardContent className="p-6 text-center">
            <Heart className="h-6 w-6 text-primary mx-auto mb-3" />
            <p className="text-sm text-foreground/85 leading-relaxed italic">
              {profile.encouragement}
            </p>
          </CardContent>
        </Card>
      )}

      {/* Share buttons */}
      <div className="flex gap-3">
        <Button onClick={handleShare} className="flex-1 gap-2">
          <Share2 className="h-4 w-4" />
          分享結果
        </Button>
        <Button variant="outline" onClick={handleCopyLink} className="gap-2">
          <Link2 className="h-4 w-4" />
          {copied ? "已複製！" : "複製連結"}
        </Button>
      </div>

      {/* CTA */}
      <div className="flex flex-col sm:flex-row gap-3">
        <Link href="/" className="flex-1">
          <Button variant="outline" size="lg" className="w-full">
            再做其他測驗
          </Button>
        </Link>
        <Link href="/history" className="flex-1">
          <Button variant="secondary" size="lg" className="w-full">
            查看歷史測驗
          </Button>
        </Link>
      </div>

      {/* Lead collection form */}
      <LeadForm quizId={result.quiz_id} sessionId={result.session_id} />

      {/* Disclaimer */}
      <div className="rounded-xl bg-secondary/50 p-4 text-center">
        <p className="text-xs text-muted-foreground leading-relaxed">
          本測驗僅供自我探索與生活反思，不構成任何醫療或心理診斷建議。
        </p>
      </div>
    </div>
  );
}
