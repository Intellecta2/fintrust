'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { apiClient } from '@/services/api';
import { useLanguage } from '@/contexts/LanguageContext';

export default function Dashboard() {
  const { t } = useLanguage();
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await apiClient.getPortfolioStats();
        setStats(response.data);
      } catch (error) {
        console.error('Error fetching stats:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  return (
    <main className="min-h-screen bg-gradient-to-br from-fintrust-50 to-blue-50 p-4">
      <div className="container">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="my-8"
        >
          <h1 className="text-4xl font-bold gradient-text mb-2">{t('dashboard.title')}</h1>
          <p className="text-gray-600">{t('dashboard.welcome')}</p>
        </motion.div>

        {/* Stats Grid */}
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-fintrust-600"></div>
          </div>
        ) : (
          <div className="grid md:grid-cols-4 gap-6 mb-8">
            {[
              { label: 'Total Borrowers', value: stats?.total_borrowers || 0, icon: '👥' },
              { label: 'Avg Credit Score', value: Math.round(stats?.avg_credit_score || 0), icon: '📊' },
              { label: 'Approval Rate', value: `${Math.round(stats?.approval_rate || 0)}%`, icon: '✅' },
              { label: 'Fraud Alerts', value: stats?.fraud_alerts_count || 0, icon: '🚨' },
            ].map((stat, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: idx * 0.1 }}
                className="card text-center"
              >
                <div className="text-4xl mb-2">{stat.icon}</div>
                <div className="text-3xl font-bold text-fintrust-600">{stat.value}</div>
                <p className="text-gray-600 text-sm">{stat.label}</p>
              </motion.div>
            ))}
          </div>
        )}

        {/* Risk Distribution */}
        {stats && (
          <div className="grid md:grid-cols-2 gap-6">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="card"
            >
              <h3 className="text-xl font-bold mb-4">Portfolio Risk Distribution</h3>
              <div className="space-y-4">
                {Object.entries(stats.portfolio_risk_distribution).map(([level, count]: [string, any]) => (
                  <div key={level}>
                    <div className="flex justify-between mb-2">
                      <span className="font-medium">{level} Risk</span>
                      <span>{count} borrowers</span>
                    </div>
                    <div className="bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all ${
                          level === 'Low' ? 'bg-green-500' :
                          level === 'Medium' ? 'bg-yellow-500' :
                          'bg-red-500'
                        }`}
                        style={{ width: `${(count / stats.total_borrowers) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.1 }}
              className="card"
            >
              <h3 className="text-xl font-bold mb-4">Fraud Analytics</h3>
              <div className="space-y-4">
                <div>
                  <p className="text-gray-600">Average Fraud Score</p>
                  <p className="text-3xl font-bold text-fintrust-600">{(stats?.avg_fraud_score || 0).toFixed(2)}</p>
                </div>
                <div>
                  <p className="text-gray-600">Active Alerts</p>
                  <p className="text-3xl font-bold text-red-600">{stats?.fraud_alerts_count || 0}</p>
                </div>
              </div>
            </motion.div>
          </div>
        )}
      </div>
    </main>
  );
}
