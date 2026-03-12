import axios, { AxiosInstance, AxiosError } from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Borrower endpoints
  async createBorrower(data: any) {
    return this.client.post('/v1/borrowers', data);
  }

  async getBorrower(borrowerId: string) {
    return this.client.get(`/v1/borrowers/${borrowerId}`);
  }

  async listBorrowers(skip = 0, limit = 100) {
    return this.client.get('/v1/borrowers', { params: { skip, limit } });
  }

  async updateBorrower(borrowerId: string, data: any) {
    return this.client.put(`/v1/borrowers/${borrowerId}`, data);
  }

  async deleteBorrower(borrowerId: string) {
    return this.client.delete(`/v1/borrowers/${borrowerId}`);
  }

  // Analysis endpoints
  async instantAnalysis(data: any) {
    return this.client.post('/v1/analyze/instant', data);
  }

  async analyzeBorrower(borrowerId: string) {
    return this.client.post(`/v1/analyze/${borrowerId}`);
  }

  async getLatestAnalysis(borrowerId: string) {
    return this.client.get(`/v1/analyze/${borrowerId}`);
  }

  async getPortfolioStats() {
    return this.client.get('/v1/portfolio/statistics');
  }

  // Simulator endpoints
  async creditSimulator(data: any) {
    return this.client.post('/v1/simulator/credit-score-simulator', data);
  }

  async fraudDetector(data: any) {
    return this.client.post('/v1/simulator/fraud-detection-simulator', data);
  }

  async loanEligibility(data: any) {
    return this.client.post('/v1/simulator/loan-eligibility-simulator', data);
  }

  // Health check
  async healthCheck() {
    return this.client.get('/health');
  }

  async apiInfo() {
    return this.client.get('/api/v1/info');
  }
}

export const apiClient = new APIClient();
