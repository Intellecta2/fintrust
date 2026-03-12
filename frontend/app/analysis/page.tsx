'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { apiClient } from '@/services/api';
import { useLanguage } from '@/contexts/LanguageContext';

export default function Analysis() {
  const { t } = useLanguage();
  const [formData, setFormData] = useState({
    full_name: '',
    occupation: '',
    employment_type: 'salaried',
    annual_income: 1200000,
    monthly_expenses: 50000,
    upi_transactions_per_month: 30,
    payment_history_score: 75,
    savings_behavior_score: 5,
  });

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e: any) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: isNaN(value) ? value : parseFloat(value) || value
    }));
  };

  const handleAnalysis = async (e: any) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await apiClient.instantAnalysis(formData);
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error performing analysis');
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
          {t('analysis.title')}
        </motion.h1>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="card"
          >
            <h2 className="text-2xl font-bold mb-6">{t('analysis.inputForm')}</h2>

            <form onSubmit={handleAnalysis} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Full Name *</label>
                <input
                  type="text"
                  name="full_name"
                  value={formData.full_name}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fintrust-500 focus:border-transparent"
                  placeholder="John Doe"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Occupation</label>
                <input
                  type="text"
                  name="occupation"
                  value={formData.occupation}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fintrust-500 focus:border-transparent"
                  placeholder="Software Engineer"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Employment Type *</label>
                <select
                  name="employment_type"
                  value={formData.employment_type}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fintrust-500 focus:border-transparent"
                >
                  <option value="salaried">Salaried</option>
                  <option value="government">Government</option>
                  <option value="business">Business</option>
                  <option value="self_employed">Self Employed</option>
                  <option value="freelancer">Freelancer</option>
                  <option value="unemployed">Unemployed</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Annual Income (₹) *</label>
                <input
                  type="number"
                  name="annual_income"
                  value={formData.annual_income}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fintrust-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Monthly Expenses (₹)</label>
                <input
                  type="number"
                  name="monthly_expenses"
                  value={formData.monthly_expenses}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fintrust-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">UPI Transactions/Month</label>
                <input
                  type="number"
                  name="upi_transactions_per_month"
                  value={formData.upi_transactions_per_month}
                  onChange={handleInputChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fintrust-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Payment History Score (0-100)</label>
                <input
                  type="number"
                  name="payment_history_score"
                  value={formData.payment_history_score}
                  onChange={handleInputChange}
                  min="0"
                  max="100"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fintrust-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-1">Savings Behavior (1-10)</label>
                <input
                  type="number"
                  name="savings_behavior_score"
                  value={formData.savings_behavior_score}
                  onChange={handleInputChange}
                  min="1"
                  max="10"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-fintrust-500 focus:border-transparent"
                />
              </div>

              {error && <div className="text-red-600 text-sm bg-red-50 p-3 rounded">{error}</div>}

              <button
                type="submit"
                disabled={loading}
                className="btn-primary w-full disabled:opacity-50"
              >
                {loading ? 'Analyzing...' : 'Analyze Credit'}
              </button>
            </form>
          </motion.div>

          {/* Results */}
          {result && (
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="space-y-6"
            >
              {/* Credit Score Card */}
              <div className="card text-center">
                <h3 className="text-lg font-medium text-gray-600 mb-2">{t('analysis.creditScore')}</h3>
                <div className="text-5xl font-bold gradient-text mb-2">{result.credit_score}</div>
                <p className="text-gray-600">/900</p>
              </div>

              {/* Risk Level & Status */}
              <div className="grid grid-cols-2 gap-4">
                <div className="card text-center">
                  <p className="text-sm text-gray-600">{t('analysis.riskLevel')}</p>
                  <p className={`text-xl font-bold mt-2 ${
                    result.risk_level === 'Low' ? 'text-green-600' :
                    result.risk_level === 'Medium' ? 'text-yellow-600' :
                    'text-red-600'
                  }`}>
                    {result.risk_level}
                  </p>
                </div>

                <div className="card text-center">
                  <p className="text-sm text-gray-600">Fraud Status</p>
                  <p className={`text-xl font-bold mt-2 ${result.is_flagged ? 'text-red-600' : 'text-green-600'}`}>
                    {result.is_flagged ? '⚠️ Flagged' : '✅ Normal'}
                  </p>
                </div>
              </div>

              {/* Loan Recommendation */}
              <div className="card">
                <h3 className="text-lg font-bold mb-4">{t('analysis.recommendation')}</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Approval Status</span>
                    <span className={`font-bold ${result.loan_approved ? 'text-green-600' : 'text-red-600'}`}>
                      {result.loan_approved ? 'APPROVED' : 'DENIED'}
                    </span>
                  </div>
                  {result.loan_approved && (
                    <>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Max Loan Amount</span>
                        <span className="font-bold">₹{result.recommended_loan_amount.toLocaleString('en-IN')}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Interest Rate</span>
                        <span className="font-bold">{result.interest_rate}% p.a.</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Category</span>
                        <span className="font-bold">{result.loan_category}</span>
                      </div>
                    </>
                  )}
                </div>
              </div>

              {/* Explanation */}
              <div className="card">
                <h3 className="text-lg font-bold mb-2">AI Explanation</h3>
                <p className="text-gray-700">{result.explanation}</p>
              </div>

              {/* Improvement Tips */}
              {result.improvement_tips && result.improvement_tips.length > 0 && (
                <div className="card">
                  <h3 className="text-lg font-bold mb-4">Improvement Tips</h3>
                  <ul className="space-y-2">
                    {result.improvement_tips.map((tip: string, idx: number) => (
                      <li key={idx} className="flex items-start gap-2">
                        <span className="text-fintrust-600 font-bold">💡</span>
                        <span className="text-gray-700">{tip}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </motion.div>
          )}
        </div>
      </div>
    </main>
  );
}
