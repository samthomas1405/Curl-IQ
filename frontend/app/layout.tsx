import type { Metadata } from "next";
import { Geist, Geist_Mono, Great_Vibes } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/lib/auth";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const greatVibes = Great_Vibes({
  variable: "--font-heading",
  weight: "400",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "CurlLabs - Curly Hair Routine Optimizer",
  description: "Track your curly hair routines, products, and results",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} ${greatVibes.variable} font-sans antialiased`}
      >
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}
