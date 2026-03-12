'use client';

import { createContext, useContext, useState, ReactNode } from 'react';

type Language = 'en' | 'hi';

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
}

const translations = {
  en: {
    // Navigation
    'nav.home': 'Home',
    'nav.dashboard': 'Dashboard',
    'nav.analysis': 'Credit Analysis',
    'nav.simulator': 'Simulator',
    'nav.portfolio': 'Portfolio',
    'nav.help': 'Help',
    
    // General
    'app.title': 'FinTrust AI',
    'app.subtitle': 'Intelligent Credit Scoring & Fraud Detection',
    'app.description': 'Advanced AI-powered fintech platform for credit analysis and fraud detection',
    
    // Dashboard
    'dashboard.title': 'Dashboard',
    'dashboard.welcome': 'Welcome to FinTrust AI',
    'dashboard.overview': 'Portfolio Overview',
    'dashboard.stats': 'Statistics',
    
    // Analysis
    'analysis.title': 'Credit Analysis',
    'analysis.inputForm': 'Borrower Information',
    'analysis.results': 'Analysis Results',
    'analysis.creditScore': 'Credit Score',
    'analysis.riskLevel': 'Risk Level',
    'analysis.recommendation': 'Recommendation',
    
    // Simulator
    'simulator.title': 'What-if Simulator',
    'simulator.creditSimulator': 'Credit Score Simulator',
    'simulator.fraudDetector': 'Fraud Detector',
    'simulator.loanEligibility': 'Loan Eligibility Checker',
  },
  hi: {
    // Navigation
    'nav.home': 'होम',
    'nav.dashboard': 'डैशबोर्ड',
    'nav.analysis': 'क्रेडिट विश्लेषण',
    'nav.simulator': 'सिम्युलेटर',
    'nav.portfolio': 'पोर्टफोलियो',
    'nav.help': 'मदद',
    
    // General
    'app.title': 'FinTrust AI',
    'app.subtitle': 'बुद्धिमान क्रेडिट स्कोरिंग और धोखाधड़ी का पता लगाना',
    'app.description': 'क्रेडिट विश्लेषण और धोखाधड़ी का पता लगाने के लिए उन्नत AI-संचालित फिनटेक प्लेटफॉर्म',
    
    // Dashboard
    'dashboard.title': 'डैशबोर्ड',
    'dashboard.welcome': 'FinTrust AI में आपका स्वागत है',
    'dashboard.overview': 'पोर्टफोलियो अवलोकन',
    'dashboard.stats': 'आंकड़े',
    
    // Analysis
    'analysis.title': 'क्रेडिट विश्लेषण',
    'analysis.inputForm': 'उधारकर्ता की जानकारी',
    'analysis.results': 'विश्लेषण परिणाम',
    'analysis.creditScore': 'क्रेडिट स्कोर',
    'analysis.riskLevel': 'जोखिम स्तर',
    'analysis.recommendation': 'सिफारिश',
    
    // Simulator
    'simulator.title': 'क्या-अगर सिम्युलेटर',
    'simulator.creditSimulator': 'क्रेडिट स्कोर सिम्युलेटर',
    'simulator.fraudDetector': 'धोखाधड़ी का पता लगाने वाला',
    'simulator.loanEligibility': 'ऋण पात्रता जांचक',
  }
};

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLanguage] = useState<Language>('en');

  const t = (key: string): string => {
    return translations[language][key as keyof typeof translations['en']] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within LanguageProvider');
  }
  return context;
}
