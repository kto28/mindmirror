"use client";

import { useState, useEffect, useCallback } from "react";
import {
  Sparkles,
  LogIn,
  LogOut,
  Eye,
  Archive,
  Send,
  Users,
  BookOpen,
  Loader2,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface AdminQuiz {
  id: number;
  title: string;
  slug: string;
  topic: string | null;
  status: string;
  publish_date: string | null;
  session_count: number;
  lead_count: number;
  created_at: string | null;
}

export default function AdminPage() {
  const [token, setToken] = useState<string | null>(null);
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState("");
  const [quizzes, setQuizzes] = useState<AdminQuiz[]>([]);
  const [loading, setLoading] = useState(false);

  const adminFetch = useCallback(
    async (path: string, options?: RequestInit) => {
      const res = await fetch(`${API_BASE}${path}`, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
          ...options?.headers,
        },
        ...options,
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail || "API Error");
      }
      return res.json();
    },
    [token]
  );

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError("");
    try {
      const res = await fetch(`${API_BASE}/api/admin/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Login failed");
      }
      const data = await res.json();
      setToken(data.token);
      localStorage.setItem("mm_admin_token", data.token);
    } catch (e: unknown) {
      setLoginError(e instanceof Error ? e.message : "Login failed");
    }
  };

  const loadQuizzes = useCallback(async () => {
    if (!token) return;
    setLoading(true);
    try {
      const data = await adminFetch("/api/admin/quizzes");
      setQuizzes(data);
    } catch {
      // token expired
      setToken(null);
      localStorage.removeItem("mm_admin_token");
    } finally {
      setLoading(false);
    }
  }, [token, adminFetch]);

  useEffect(() => {
    const saved = localStorage.getItem("mm_admin_token");
    if (saved) setToken(saved);
  }, []);

  useEffect(() => {
    if (token) loadQuizzes();
  }, [token, loadQuizzes]);

  const handlePublish = async (quizId: number) => {
    await adminFetch(`/api/admin/quizzes/${quizId}/publish`, { method: "POST" });
    loadQuizzes();
  };

  const handleArchive = async (quizId: number) => {
    await adminFetch(`/api/admin/quizzes/${quizId}/archive`, { method: "POST" });
    loadQuizzes();
  };

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem("mm_admin_token");
  };

  // Login screen
  if (!token) {
    return (
      <div className="mx-auto max-w-sm px-4 py-20">
        <Card>
          <CardContent className="p-6 space-y-4">
            <div className="text-center space-y-2">
              <Sparkles className="h-8 w-8 text-primary mx-auto" />
              <h1 className="text-xl font-bold">管理後台</h1>
              <p className="text-sm text-muted-foreground">請輸入管理員密碼</p>
            </div>
            <form onSubmit={handleLogin} className="space-y-3">
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="密碼"
                className="w-full h-11 rounded-lg border border-input bg-background px-3 text-sm focus:outline-none focus:ring-2 focus:ring-ring"
              />
              {loginError && <p className="text-xs text-destructive">{loginError}</p>}
              <Button type="submit" className="w-full gap-2">
                <LogIn className="h-4 w-4" />
                登入
              </Button>
            </form>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Admin dashboard
  const statusConfig: Record<string, { label: string; color: string }> = {
    draft: { label: "草稿", color: "bg-yellow-100 text-yellow-700" },
    published: { label: "已發布", color: "bg-green-100 text-green-700" },
    archived: { label: "已下架", color: "bg-gray-100 text-gray-500" },
  };

  const todayQuiz = quizzes.find((q) => q.status === "published");
  const totalSessions = quizzes.reduce((sum, q) => sum + q.session_count, 0);
  const totalLeads = quizzes.reduce((sum, q) => sum + q.lead_count, 0);

  return (
    <div className="mx-auto max-w-3xl px-4 py-8 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">管理後台</h1>
          <p className="text-sm text-muted-foreground">MindMirror 測驗管理</p>
        </div>
        <Button variant="outline" size="sm" onClick={handleLogout} className="gap-1.5">
          <LogOut className="h-4 w-4" />
          登出
        </Button>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-3 gap-3">
        <Card>
          <CardContent className="p-4 text-center">
            <BookOpen className="h-5 w-5 text-primary mx-auto mb-1" />
            <div className="text-2xl font-bold">{quizzes.length}</div>
            <div className="text-xs text-muted-foreground">測驗總數</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 text-center">
            <Users className="h-5 w-5 text-primary mx-auto mb-1" />
            <div className="text-2xl font-bold">{totalSessions}</div>
            <div className="text-xs text-muted-foreground">完成次數</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4 text-center">
            <Send className="h-5 w-5 text-primary mx-auto mb-1" />
            <div className="text-2xl font-bold">{totalLeads}</div>
            <div className="text-xs text-muted-foreground">Leads</div>
          </CardContent>
        </Card>
      </div>

      {/* Today status */}
      <Card className={todayQuiz ? "border-green-200" : "border-yellow-200"}>
        <CardContent className="p-4 flex items-center gap-3">
          <div className={`h-3 w-3 rounded-full ${todayQuiz ? "bg-green-500" : "bg-yellow-500 animate-pulse"}`} />
          <span className="text-sm">
            {todayQuiz ? `今日測驗已發布：${todayQuiz.title}` : "今日尚未發布測驗"}
          </span>
        </CardContent>
      </Card>

      {/* Quiz list */}
      <div className="space-y-2">
        <h2 className="font-semibold text-foreground">所有測驗</h2>
        {loading ? (
          <div className="text-center py-8">
            <Loader2 className="h-6 w-6 text-primary mx-auto animate-spin" />
          </div>
        ) : (
          <div className="space-y-2">
            {quizzes.map((quiz) => {
              const sc = statusConfig[quiz.status] || statusConfig.draft;
              return (
                <Card key={quiz.id}>
                  <CardContent className="p-4">
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${sc.color}`}>
                            {sc.label}
                          </span>
                          {quiz.topic && (
                            <span className="text-xs text-muted-foreground">{quiz.topic}</span>
                          )}
                        </div>
                        <h3 className="font-medium text-sm truncate">{quiz.title}</h3>
                        <div className="flex gap-3 mt-1 text-xs text-muted-foreground">
                          <span>{quiz.session_count} 次完成</span>
                          <span>{quiz.lead_count} leads</span>
                          {quiz.publish_date && <span>{quiz.publish_date}</span>}
                        </div>
                      </div>
                      <div className="flex gap-1.5 shrink-0">
                        {quiz.status === "draft" && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handlePublish(quiz.id)}
                            className="h-8 text-xs gap-1"
                          >
                            <Eye className="h-3 w-3" />
                            發布
                          </Button>
                        )}
                        {quiz.status === "published" && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleArchive(quiz.id)}
                            className="h-8 text-xs gap-1"
                          >
                            <Archive className="h-3 w-3" />
                            下架
                          </Button>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
