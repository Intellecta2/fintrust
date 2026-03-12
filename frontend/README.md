# FinTrust AI Frontend - Setup Instructions

## Quick Start

### Prerequisites
- Node.js 18+
- Backend Running (http://localhost:8000)

### Development

```bash
npm install
npm run dev
```

Visit http://localhost:3000

### Production Build

```bash
npm run build
npm start
```

## Docker

### Build & Run
```bash
docker build -t fintrust-frontend .
docker run -p 3000:3000 buntrust-frontend
```

### Environment Variables
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Features

✅ Credit Score Analysis
✅ Fraud Detection Dashboard
✅ What-if Simulator
✅ Portfolio Analytics
✅ Multilingual Support (EN/HI)
✅ Real-time Data Updates
✅ Responsive Design

## Pages

- `/` - Home Page
- `/dashboard` - Portfolio Analytics
- `/analysis` - Credit Analysis
- `/simulator` - What-if Scenarios

## Troubleshooting

API Connection Error:
- Set NEXT_PUBLIC_API_URL correctly
- Ensure backend is running
- Check CORS settings in backend

Build Issues:
```bash
rm -rf .next node_modules
npm install
npm run build
```
