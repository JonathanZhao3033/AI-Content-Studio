import type { Metadata } from "next";
import "./globals.css";
import { ConfigProvider } from "@/context/ConfigContext";
import { Sidebar } from "@/components/Sidebar";

export const metadata: Metadata = {
  title: "AI Content Studio | Pro",
  description: "Commercial-grade automated AI video generation studio.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="flex h-screen overflow-hidden bg-[var(--bg-main)] text-zinc-100 font-sans">
        
        <Sidebar />

        <main className="flex-1 overflow-y-auto p-8 relative">
          <ConfigProvider>
            {children}
          </ConfigProvider>
        </main>
      </body>
    </html>
  );
}