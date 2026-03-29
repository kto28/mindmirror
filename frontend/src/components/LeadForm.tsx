"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { createLead } from "@/lib/api";
import { Heart, CheckCircle } from "lucide-react";

interface LeadFormProps {
  quizId?: number;
  sessionId?: string;
}

export default function LeadForm({ quizId, sessionId }: LeadFormProps) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [whatsapp, setWhatsapp] = useState("");
  const [consent, setConsent] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!consent) return;
    setLoading(true);
    try {
      await createLead({ quiz_id: quizId, session_id: sessionId, name, email, whatsapp, consent });
      setSubmitted(true);
    } catch {
      // silently fail for leads
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <Card className="border-primary/20 bg-primary/5">
        <CardContent className="p-6 text-center">
          <CheckCircle className="h-8 w-8 text-primary mx-auto mb-3" />
          <p className="font-medium text-foreground">感謝你的訂閱！</p>
          <p className="text-sm text-muted-foreground mt-1">我們會將每日測驗推送給你。</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center gap-2 mb-4">
          <Heart className="h-5 w-5 text-primary" />
          <h3 className="font-semibold text-foreground">訂閱每日測驗提醒</h3>
        </div>
        <p className="text-sm text-muted-foreground mb-4">
          留下你的聯絡方式，我們會定期推送新的自我探索測驗。
        </p>
        <form onSubmit={handleSubmit} className="space-y-3">
          <input
            type="text"
            placeholder="你的名字（選填）"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full h-11 rounded-lg border border-input bg-background px-3 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
          <input
            type="email"
            placeholder="Email（選填）"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full h-11 rounded-lg border border-input bg-background px-3 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
          <input
            type="tel"
            placeholder="WhatsApp 號碼（選填）"
            value={whatsapp}
            onChange={(e) => setWhatsapp(e.target.value)}
            className="w-full h-11 rounded-lg border border-input bg-background px-3 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          />
          <label className="flex items-start gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={consent}
              onChange={(e) => setConsent(e.target.checked)}
              className="mt-1 h-4 w-4 rounded border-input accent-primary"
            />
            <span className="text-xs text-muted-foreground leading-relaxed">
              我同意接收 MindMirror 的測驗推送通知，並了解可以隨時取消訂閱。
            </span>
          </label>
          <Button type="submit" disabled={!consent || loading} className="w-full">
            {loading ? "提交中..." : "訂閱"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
