import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { Providers } from '@/components/providers'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'AgenticAI Lab',
  description: 'AI-Powered Content Creation Platform',
  keywords: ['AI', 'Content Creation', 'Automation', 'YouTube', 'TikTok', 'Social Media'],
  authors: [{ name: 'AgenticAI Lab Team' }],
  viewport: 'width=device-width, initial-scale=1',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarnings>
      <body className={inter.className}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
