'use client';

import React, { useEffect } from 'react';
import { useAnalytics } from '../hooks/useAnalytics';

interface AnalyticsProviderProps {
  children: React.ReactNode;
}

export const AnalyticsProvider: React.FC<AnalyticsProviderProps> = ({ children }) => {
  const { trackScrolling } = useAnalytics();

  useEffect(() => {
    // Set up global scroll tracking
    const cleanupScrollTracking = trackScrolling();
    
    return cleanupScrollTracking;
  }, [trackScrolling]);

  // Track page views
  useEffect(() => {
    // Log initial page view
    const sessionId = localStorage.getItem('analytics_session_id');
    if (sessionId) {
      console.log(`Page view tracked for session: ${sessionId} on ${window.location.href}`);
    }
  }, []);

  return <>{children}</>;
}; 