'use client';

import { useEffect, useCallback } from 'react';
import { ActionType, logClick, logKeyPress, logScroll, logNavigation, getSessionId } from '../services/analyticsLogger';

export const useAnalytics = () => {
  const sessionId = getSessionId();

  // Enhanced click handler that logs automatically
  const handleClick = useCallback((elementId: string, text: string, event?: React.MouseEvent) => {
    let coordinates = { x: 0, y: 0 };
    if (event) {
      coordinates = { x: event.clientX, y: event.clientY };
    }
    logClick(elementId, text, coordinates);
  }, []);

  // Enhanced input handler that logs key presses
  const handleKeyPress = useCallback((elementId: string, text: string, value: string) => {
    logKeyPress(elementId, text, value);
  }, []);

  // Scroll tracking hook
  const trackScrolling = useCallback(() => {
    let scrollTimeout: NodeJS.Timeout;
    
    const handleScroll = () => {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(() => {
        const scrollX = window.scrollX;
        const scrollY = window.scrollY;
        const text = `User scrolled to position (${scrollX}, ${scrollY})`;
        logScroll(text, scrollX, scrollY);
      }, 150); // Debounce scroll events
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => {
      window.removeEventListener('scroll', handleScroll);
      clearTimeout(scrollTimeout);
    };
  }, []);

  // Navigation tracking
  const trackNavigation = useCallback((url: string, text: string) => {
    logNavigation(ActionType.GO_TO_URL, text, url);
  }, []);

  // Track browser back/forward
  useEffect(() => {
    const handlePopState = () => {
      logNavigation(ActionType.GO_BACK, 'User navigated back/forward using browser controls');
    };

    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, []);

  return {
    sessionId,
    handleClick,
    handleKeyPress,
    trackScrolling,
    trackNavigation
  };
}; 