export default function Footer() {
  return (
    <footer className="border-t bg-background py-8 mt-auto">
      <div className="mx-auto max-w-2xl px-4 text-center space-y-3">
        <p className="text-xs text-muted-foreground leading-relaxed">
          本平台內容僅供自我探索與生活反思，不構成任何醫療或心理診斷建議。
        </p>
        <p className="text-xs text-muted-foreground">
          © {new Date().getFullYear()} MindMirror. All rights reserved.
        </p>
      </div>
    </footer>
  );
}
