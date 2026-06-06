export const API_BASE_URL = 'http://localhost:8000/api/v1';

export function getAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('fintrack_token');
}

export function setAuthToken(token: string) {
  if (typeof window !== 'undefined') {
    localStorage.setItem('fintrack_token', token);
  }
}

export function removeAuthToken() {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('fintrack_token');
  }
}

interface FetchOptions extends RequestInit {
  requireAuth?: boolean;
}

export async function apiFetch(endpoint: string, options: FetchOptions = {}) {
  const { requireAuth = true, headers, ...customConfig } = options;
  const token = getAuthToken();

  if (requireAuth && !token) {
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
    throw new Error('No auth token found');
  }

  const config: RequestInit = {
    ...customConfig,
    headers: {
      ...headers,
      ...(requireAuth && token ? { Authorization: `Bearer ${token}` } : {}),
    },
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

  if (response.status === 401) {
    removeAuthToken();
    if (typeof window !== 'undefined') {
      window.location.href = '/login';
    }
    throw new Error('Unauthorized');
  }

  return response;
}

export async function apiJson(endpoint: string, options: FetchOptions = {}) {
  const customHeaders: Record<string, string> = { ...((options.headers as Record<string, string>) || {}) };
  
  if (!customHeaders['Content-Type']) {
    customHeaders['Content-Type'] = 'application/json';
  }

  const response = await apiFetch(endpoint, { ...options, headers: customHeaders });
  
  const text = await response.text();
  if (!text) return null;
  
  try {
    return JSON.parse(text);
  } catch (e) {
    return text;
  }
}
