'use client';

type EventType = 
  | 'DB_UPDATE'
  | 'CLICK'
  | 'SCROLL'
  | 'HOVER'
  | 'KEY_PRESS'
  | 'GO_BACK'
  | 'GO_FORWARD'
  | 'GO_TO_URL'
  | 'SET_STORAGE'
  | 'CUSTOM';

interface BaseEvent {
  actionType: EventType;
  payload: {
    text: string;
    page_url: string;
    [key: string]: any;
  };
}

interface ClickEvent extends BaseEvent {
  actionType: 'CLICK';
  payload: {
    text: string;
    page_url: string;
    element_identifier: string;
    coordinates?: { x: number; y: number };
  };
}

interface ScrollEvent extends BaseEvent {
  actionType: 'SCROLL';
  payload: {
    text: string;
    page_url: string;
    scroll_x: number;
    scroll_y: number;
  };
}

interface HoverEvent extends BaseEvent {
  actionType: 'HOVER';
  payload: {
    text: string;
    page_url: string;
    element_identifier: string;
  };
}

interface KeyPressEvent extends BaseEvent {
  actionType: 'KEY_PRESS';
  payload: {
    text: string;
    page_url: string;
    element_identifier: string;
    key: string;
  };
}

interface NavigationEvent extends BaseEvent {
  actionType: 'GO_BACK' | 'GO_FORWARD' | 'GO_TO_URL';
  payload: {
    text: string;
    page_url: string;
    target_url?: string;
  };
}

interface StorageEvent extends BaseEvent {
  actionType: 'SET_STORAGE';
  payload: {
    text: string;
    page_url: string;
    storage_type: 'local' | 'session';
    key: string;
    value: any;
  };
}

interface CustomEvent extends BaseEvent {
  actionType: 'CUSTOM';
  payload: {
    text: string;
    page_url: string;
    [key: string]: any;
  };
}

type Event = 
  | ClickEvent
  | ScrollEvent
  | HoverEvent
  | KeyPressEvent
  | NavigationEvent
  | StorageEvent
  | CustomEvent;

class AnalyticsLogger {
  private static instance: AnalyticsLogger;
  private apiUrl: string;

  private constructor() {
    this.apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  }

  public static getInstance(): AnalyticsLogger {
    if (!AnalyticsLogger.instance) {
      AnalyticsLogger.instance = new AnalyticsLogger();
    }
    return AnalyticsLogger.instance;
  }

  private async logEvent(event: Event): Promise<void> {
    try {
      const response = await fetch(`${this.apiUrl}/_synthetic/log_event`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(event),
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error(`Failed to log event: ${response.statusText}`);
      }
    } catch (error) {
      console.error('Error logging event:', error);
    }
  }

  public logClick(elementId: string, text: string, coordinates?: { x: number; y: number }): void {
    this.logEvent({
      actionType: 'CLICK',
      payload: {
        text,
        page_url: window.location.href,
        element_identifier: elementId,
        coordinates,
      },
    });
  }

  public logScroll(scrollX: number, scrollY: number): void {
    this.logEvent({
      actionType: 'SCROLL',
      payload: {
        text: `User scrolled to position (${scrollX}, ${scrollY})`,
        page_url: window.location.href,
        scroll_x: scrollX,
        scroll_y: scrollY,
      },
    });
  }

  public logHover(elementId: string, text: string): void {
    this.logEvent({
      actionType: 'HOVER',
      payload: {
        text,
        page_url: window.location.href,
        element_identifier: elementId,
      },
    });
  }

  public logKeyPress(elementId: string, key: string): void {
    this.logEvent({
      actionType: 'KEY_PRESS',
      payload: {
        text: `User pressed key '${key}'`,
        page_url: window.location.href,
        element_identifier: elementId,
        key,
      },
    });
  }

  public logNavigation(action: 'GO_BACK' | 'GO_FORWARD' | 'GO_TO_URL', targetUrl?: string): void {
    this.logEvent({
      actionType: action,
      payload: {
        text: `User navigated ${action.toLowerCase()}`,
        page_url: window.location.href,
        target_url: targetUrl,
      },
    });
  }

  public logStorage(type: 'local' | 'session', key: string, value: any): void {
    this.logEvent({
      actionType: 'SET_STORAGE',
      payload: {
        text: `User set ${type} storage for key '${key}'`,
        page_url: window.location.href,
        storage_type: type,
        key,
        value,
      },
    });
  }

  async logCustomAction(action: string, data: Record<string, any> = {}) {
    const event: CustomEvent = {
      actionType: 'CUSTOM',
      payload: {
        text: action,
        page_url: window.location.href,
        ...data
      }
    };
    await this.logEvent(event);
  }
}

export const analyticsLogger = AnalyticsLogger.getInstance(); 