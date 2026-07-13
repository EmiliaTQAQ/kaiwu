function resolveApiBaseUrl(rawBaseUrl: string | undefined) {
  const configuredBaseUrl = (rawBaseUrl || '').trim().replace(/\/$/, '');
  const isHttpsPage = typeof window !== 'undefined' && window.location.protocol === 'https:';

  if (isHttpsPage && configuredBaseUrl.toLowerCase().startsWith('http://')) {
    console.warn(
      'VITE_API_BASE_URL uses HTTP on an HTTPS page. Falling back to same-origin API paths to avoid mixed content.',
    );
    return '';
  }

  return configuredBaseUrl;
}

export const API_BASE_URL = resolveApiBaseUrl(import.meta.env.VITE_API_BASE_URL);

export async function apiJson<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    let message = `HTTP ${response.status}`;
    try {
      const body = await response.clone().json();
      if (typeof body?.error === 'string' && body.error.trim()) {
        message = body.error.trim();
      }
    } catch {
      // Keep the HTTP status fallback when the server did not return JSON.
    }
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}
