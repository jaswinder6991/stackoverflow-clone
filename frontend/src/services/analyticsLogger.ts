'use client';

// Action types enum matching backend types — minus HTTP_REQUEST and DB_UPDATE
export enum ActionType {
  CLICK = "click",
  SCROLL = "scroll",
  HOVER = "hover",
  KEY_PRESS = "key_press",
  GO_BACK = "go_back",
  GO_FORWARD = "go_forward",
  GO_TO_URL = "go_to_url",
  SET_STORAGE = "set_storage",
  CUSTOM = "custom"
}

export interface ClickPayload {
  text: string;
  page_url: string;
  element_identifier: string;
  coordinates: {
    x: number;
    y: number;
  };
}

export interface ScrollPayload {
  text: string;
  page_url: string;
  scroll_x: number;
  scroll_y: number;
}

export interface HoverPayload {
  text: string;
  page_url: string;
  element_identifier: string;
}

export interface KeyPressPayload {
  text: string;
  page_url: string;
  element_identifier: string;
  key: string;
}

export interface GoBackPayload {
  text: string;
  page_url: string;
}

export interface GoForwardPayload {
  text: string;
  page_url: string;
}

export interface GoToUrlPayload {
  text: string;
  page_url: string;
  target_url: string;
}

export interface SetStoragePayload {
  text: string;
  page_url: string;
  storage_type: "local" | "session";
  key: string;
  value: string;
}

export interface CustomPayload {
  text: string;
  custom_action: string;
  data: Record<string, unknown>;
}

// Union type for all possible payloads
export type LogPayload =
  | ClickPayload
  | ScrollPayload
  | HoverPayload
  | KeyPressPayload
  | GoBackPayload
  | GoForwardPayload
  | GoToUrlPayload
  | SetStoragePayload
  | CustomPayload;

// Log interface matching Python's Log model
export interface Log {
  id: number;
  timestamp: string; // ISO date string
  session_id: string;
  action_type: ActionType;
  payload: LogPayload;
}

// Utility function to get or create session ID
export const getSessionId = (): string => {
  if (typeof window === 'undefined') return '';
  
  // First, try to use auth token as session_id for logged-in users
  const authToken = localStorage.getItem('token');
  if (authToken) {
    return authToken;
  }
  
  // Fallback to anonymous session for non-logged users
  let sessionId = localStorage.getItem('analytics_session_id');
  if (!sessionId) {
    sessionId = `anonymous_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('analytics_session_id', sessionId);
  }
  return sessionId;
};

export const logEvent = async (sessionId: string, actionType: ActionType, payload: LogPayload) => {
  try {
    const response = await fetch(
      `http://localhost:8000/_synthetic/log_event?session_id=${sessionId}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          actionType: actionType, 
          payload: payload
        }),
      }
    );
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error("Failed to log event:", errorText);
      throw new Error(`Failed to log event: ${errorText}`);
    }
  } catch (error) {
    console.error("Error logging action:", error);
    // Don't throw - we don't want analytics errors to break the app
  }
};

// Helper functions for common logging patterns
export const logClick = (elementId: string, text: string, coordinates?: { x: number; y: number }) => {
  const sessionId = getSessionId();
  const payload: ClickPayload = {
    text,
    page_url: window.location.href,
    element_identifier: elementId,
    coordinates: coordinates || { x: 0, y: 0 }
  };
  logEvent(sessionId, ActionType.CLICK, payload);
};

export const logKeyPress = (elementId: string, text: string, key: string) => {
  const sessionId = getSessionId();
  const payload: KeyPressPayload = {
    text,
    page_url: window.location.href,
    element_identifier: elementId,
    key
  };
  logEvent(sessionId, ActionType.KEY_PRESS, payload);
};

export const logScroll = (text: string, scrollX: number, scrollY: number) => {
  const sessionId = getSessionId();
  const payload: ScrollPayload = {
    text,
    page_url: window.location.href,
    scroll_x: scrollX,
    scroll_y: scrollY
  };
  logEvent(sessionId, ActionType.SCROLL, payload);
};

export const logNavigation = (actionType: ActionType.GO_BACK | ActionType.GO_FORWARD | ActionType.GO_TO_URL, text: string, targetUrl?: string) => {
  const sessionId = getSessionId();
  let payload: GoBackPayload | GoForwardPayload | GoToUrlPayload;
  
  if (actionType === ActionType.GO_TO_URL && targetUrl) {
    payload = {
      text,
      page_url: window.location.href,
      target_url: targetUrl
    };
  } else {
    payload = {
      text,
      page_url: window.location.href
    };
  }
  
  logEvent(sessionId, actionType, payload);
}; 