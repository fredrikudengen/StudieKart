export const API_BASE = import.meta.env.VITE_API_URL ?? ''

export const getToken = () => localStorage.getItem('token')
export const setToken = (t) => localStorage.setItem('token', t)
export const clearToken = () => localStorage.removeItem('token')

export async function authFetch(url, options = {}) {
  const token = getToken()
  const res = await fetch(API_BASE + url, {
    ...options,
    headers: {
      ...(options.headers || {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    },
  })
  if (res.status === 401) {
    // Expired or invalid token: drop it and send the user back to login.
    clearToken()
    window.location.assign('/login')
  }
  return res
}
