'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { apiClient } from '@/services/api';
import { useLanguage } from '@/contexts/LanguageContext';

export default function Simulator() {
  const { t } = useLanguage();
  const [activeTab, setActiveTab] = useState('credit');
  
  const [formData, setFormData] = useState({
    full_name: 'Test User',
    employment_type: 'salaried',
    annual_income: 1200000,
    monthly_expenses: 50000,
    upi_transactions_per_month: 30,
    payment_history_score: 75,
    savings_behavior_score: 5,
  });

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleInputChange = (e: any) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: isNaN(value) ? value : parseFloat(value) || value
    }));
  };

  const handleRunSimulator = async () => {
    setLoading(true);
    try {
      let response;
      if (activeTab === 'credit') {
        response = await apiClient.creditSimulator(formData);
      } else if (activeTab === 'fraud') {
        response = await apiClient.fraudDetector(formData);
      } else {
        response = await apiClient.loanEligibility(formData);
      }
      setResult(response.data);
    } catch (error) {
      console.error('Error running simulator:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-fintrust-50 to-blue-50 p-4 pt-20">
      <div className="container">
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-bold gradient-text mb-8"
        >
          {t('simulator.title')}
        </motion.h1>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Input Panel */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="card"
          >
            <h2 className="text-2xl font-bold mb-6">Scenario Parameters</h2>

            <div className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-medium mb-1">Annual Income (₹)</label>
                <input
                  type="number"
                  name="annual_income"
                  value={formData.annual_income}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fintrust-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Monthly Expenses (₹)</label>
                <input
                  type="number"
                  name="monthly_expenses"
                  value={formData.monthly_expenses}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fintrust-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Payment History Score</label>
                <input
                  type="range"
                  name="payment_history_score"
                  value={formData.payment_history_score}
                  onChange={handleInputChange}
                  min="0"
                  max="100"
                  className="w-full"
                />
                <div className="text-sm text-gray-600 mt-1">{formData.payment_history_score}/100</div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Savings Behavior</label>
                <input
                  type="range"
                  name="savings_behavior_score"
                  value={formData.savings_behavior_score}
                  onChange={handleInputChange}
                  min="1"
                  max="10"
                  className="w-full"
                />
                <div className="text-sm text-gray-600 mt-1">{formData.savings_behavior_score}/10</div>
              </div>
            </div>

            {/* Tab Selection */}
            <div className="flex gap-2 mb-6">
              {[
                { id: 'credit', label: 'Credit Simulator' },
                { id: 'fraud', label: 'Fraud Detector' },
                { id: 'loan', label: 'Loan Eligibility' },
              ].map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    activeTab === tab.id
                      ? 'bg-fintrust-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            <button
              onClick={handleRunSimulator}
              disabled={loading}
              className="btn-primary w-full"
            >
              {loading ? 'Running...' : 'Run Simulation'}
            </button>
          </motion.div>

          {/* Results Panel */}
          {result && (
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="card space-y-6"
            >
              <h2 className="text-2xl font-bold">Simulation Results</h2>

              {activeTab === 'credit' && (
                <div className="space-y-4">
                  <div className="text-center">
                    <p className="text-gray-600">Predicted Credit Score</p>
                    <p className="text-5xl font-bold gradient-text">{result.credit_score}</p>
                    <p className="text-gray-600">/900</p>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-gray-50 p-4 rounded">
                      <p className="text-sm text-gray-600">Risk Level</p>
                      <p className={`text-lg font-bold mt-2 ${
                        result.risk_level === 'Low' ? 'text-green-600' :
                        result.risk_level === 'Medium' ? 'text-yellow-600' :
                        'text-red-600'
                      }`}>
                        {result.risk_level}
                      </p>
                    </div>
                    <div className="bg-gray-50 p-4 rounded">
                      <p className="text-sm text-gray-600">Default Risk</p>
                      <p className="text-lg font-bold mt-2">{(result.default_probability * 100).toFixed(1)}%</p>
                    </div>
                  </div>

                  <div className="bg-blue-50 p-4 rounded">
                    <p className="text-sm font-medium mb-2">Explanation</p>
                    <p className="text-gray-700">{result.explanation}</p>
                  </div>
                </div>
              )}

              {activeTab === 'fraud' && (
                <div className="space-y-4">
                  <div className={`text-center p-6 rounded-lg ${
                    result.is_flagged ? 'bg-red-50' : 'bg-green-50'
                  }`}>
                    <p className="text-3xl mb-2">{result.is_flagged ? '🚨' : '✅'}</p>
                    <p className={`text-xl font-bold ${
                      result.is_flagged ? 'text-red-600' : 'text-green-600'
                    }`}>
                      {result.risk_level}
                    </p>
                  </div>

                  <div className="bg-gray-50 p-4 rounded">
                    <p className="text-sm font-medium mb-2">Fraud Score</p>
                    <div className="text-3xl font-bold text-fintrust-600">{result.fraud_score.toFixed(2)}</div>
                    <p className="text-xs text-gray-600 mt-1">/100</p>
                  </div>

                  <div className="bg-blue-50 p-4 rounded">
                    <p className="text-sm font-medium mb-2">Next Step</p>
                    <p className="text-gray-700">{result.recommendation}</p>
                  </div>
                </div>
              )}

              {activeTab === 'loan' && (
                <div className="space-y-4">
                  <div className={`text-center p-6 rounded-lg ${
                    result.eligible_for_loan ? 'bg-green-50' : 'bg-red-50'
                  }`}>
                    <p className="text-3xl mb-2">{result.eligible_for_loan ? '✅' : '❌'}</p>
                    <p className={`text-xl font-bold ${
                      result.eligible_for_loan ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {result.eligible_for_loan ? 'ELIGIBLE' : 'NOT ELIGIBLE'}
                    </p>
                  </div>

                  {result.eligible_for_loan && (
                    <div className="space-y-3 bg-gray-50 p-4 rounded">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Credit Score</span>
                        <span className="font-bold">{result.credit_score}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Max Loan Amount</span>
                        <span className="font-bold">₹{result.max_loan_amount.toLocaleString('en-IN')}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Interest Rate</span>
                        <span className="font-bold">{result.annual_interest_rate}% p.a.</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Category</span>
                        <span className="font-bold">{result.loan_category}</span>
                      </div>
                    </div>
                  )}

                  <div className="bg-blue-50 p-4 rounded text-sm">
                    <p className="text-gray-700">{result.notes}</p>
                  </div>
                </div>
              )}
            </motion.div>
          )}
        </div>
      </div>
    </main>
  );
}
