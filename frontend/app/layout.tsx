import type { Metadata } from 'next'
import { LanguageProvider } from '@/contexts/LanguageContext'
import { ThemeProvider } from '@/contexts/ThemeContext'
import '../globals.css'

export const metadata: Metadata = {
  title: 'FinTrust AI - Intelligent Credit Scoring & Fraud Detection',
  description: 'Advanced AI-powered fintech platform for credit analysis and fraud detection. Get instant credit scores, fraud alerts, and loan recommendations.',
  keywords: 'credit scoring, fraud detection, fintech, AI, lending, credit analysis',
  authors: [{ name: 'FinTrust AI Team' }],
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          <LanguageProvider>
            {children}
          </LanguageProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}
