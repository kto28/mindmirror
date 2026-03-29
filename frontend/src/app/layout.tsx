import type { Metadata, Viewport } from "next";
import "./globals.css";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export const metadata: Metadata = {
  title: {
    default: "MindMirror — 每日一測，更了解自己",
    template: "%s | MindMirror",
  },
  description: "每日正向心理測驗平台。透過輕鬆有趣的自我探索測驗，更了解自己，提升自我素質。",
  metadataBase: new URL("https://mindmirror.eddyto.com"),
  openGraph: {
    type: "website",
    locale: "zh_TW",
    siteName: "MindMirror",
    title: "MindMirror — 每日一測，更了解自己",
    description: "每日正向心理測驗平台。透過輕鬆有趣的自我探索測驗，更了解自己，提升自我素質。",
  },
  twitter: {
    card: "summary_large_image",
    title: "MindMirror — 每日一測，更了解自己",
    description: "每日正向心理測驗平台。",
  },
  robots: { index: true, follow: true },
  manifest: "/manifest.json",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  themeColor: "#7C8DB0",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-Hant">
      <body className="min-h-screen flex flex-col antialiased">
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
