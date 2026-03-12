'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';
import { useLanguage } from '@/contexts/LanguageContext';

export default function Home() {
  const { t } = useLanguage();

  return (
    <main className="min-h-screen bg-gradient-to-br from-fintrust-50 via-blue-50 to-cyan-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/95 backdrop-blur-md z-50 shadow-sm">
        <div className="container flex items-center justify-between py-4">
          <div className="text-2xl font-bold gradient-text">FinTrust AI</div>
          <div className="flex gap-8">
            <Link href="/dashboard" className="text-fintrust-600 hover:text-fintrust-700 font-medium">Dashboard</Link>
            <Link href="/analysis" className="text-fintrust-600 hover:text-fintrust-700 font-medium">Analysis</Link>
            <Link href="/simulator" className="text-fintrust-600 hover:text-fintrust-700 font-medium">Simulator</Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container pt-32 pb-20 px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl md:text-6xl font-bold gradient-text mb-6">
            FinTrust AI
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 mb-8">
            Intelligent Credit Scoring & Fraud Detection
          </p>
          <p className="text-lg text-gray-500 mb-12 max-w-2xl mx-auto">
            Advanced AI-powered platform for accurate credit analysis, fraud detection, and intelligent loan recommendations
          </p>

          <div className="flex gap-4 justify-center">
            <Link href="/analysis" className="btn-primary">
              Get Started
            </Link>
            <Link href="/simulator" className="btn-secondary">
              Try Simulator
            </Link>
          </div>
        </motion.div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-3 gap-8 mt-20">
          {[
            {
              title: 'Credit Scoring',
              description: 'AI-powered credit score prediction (300-900) using XGBoost models',
              icon: '📊'
            },
            {
              title: 'Fraud Detection',
              description: 'Real-time fraud detection using Isolation Forest and anomaly detection',
              icon: '🛡️'
            },
            {
              title: 'SHAP Explainability',
              description: 'Transparent AI with SHAP values explaining every credit decision',
              icon: '🔍'
            },
            {
              title: 'Risk Analysis',
              description: 'Comprehensive default risk prediction and portfolio analytics',
              icon: '⚠️'
            },
            {
              title: 'Loan Recommendations',
              description: 'Intelligent loan amount and interest rate recommendations',
              icon: '💰'
            },
            {
              title: 'What-if Simulator',
              description: 'Test financial scenarios and see impact on credit eligibility',
              icon: '🔄'
            },
          ].map((feature, idx) => (
            <motion.div
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1, duration: 0.5 }}
              className="card hover:shadow-xl"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <h3 className="text-xl font-bold text-fintrust-900 mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-fintrust-900 text-white py-16 mt-20">
        <div className="container text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Get Started?</h2>
          <p className="text-fintrust-100 mb-8 text-lg">
            Analyze credit profiles and detect fraud in seconds with FinTrust AI
          </p>
          <Link href="/analysis" className="btn-primary bg-white text-fintrust-900 hover:bg-fintrust-100">
            Start Analysis
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-8">
        <div className="container text-center">
          <p>&copy; 2024 FinTrust AI. All rights reserved. | Intelligent Fintech Platform</p>
        </div>
      </footer>
    </main>
  )
}
