import type React from "react"
import type { Metadata } from "next"
import "./globals.css"
import { AuthProvider } from "@/hooks/use-auth"
import { CartProvider } from "@/hooks/use-cart"
import { ThemeProvider } from "@/components/theme-provider"
import { Toaster } from "@/components/ui/toaster"
import { fontSans } from "@/lib/fonts"
import { cn } from "@/lib/utils"
import { Navigation } from "@/components/navigation"
import AppInitializer from "@/components/app-initializer";
import { Inter } from "next/font/google";

export const metadata: Metadata = {
  title: "Rig Magic",
  description: "Find, customize, and service your perfect yacht rigging",
  generator: "v0.dev",
}


const inter = Inter({ subsets: ["latin"] });

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={cn("min-h-screen bg-background font-sans antialiased", fontSans.variable)}>
        <AuthProvider>
          <CartProvider>
            <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
              <Navigation />
                <AppInitializer>
                  {children}
                </AppInitializer>
              <Toaster />
            </ThemeProvider>
          </CartProvider>
        </AuthProvider>
      </body>
    </html>
  )
}
