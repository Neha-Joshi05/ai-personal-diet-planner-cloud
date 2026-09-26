const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function authHeaders() {
  const token = localStorage.getItem('nutricloud_token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function handle(res) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed (${res.status})`)
  }
  if (res.status === 204) return null
  return res.json()
}

export const api = {
  async register(name, email, password) {
    const res = await fetch(`${BASE_URL}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password }),
    })
    return handle(res)
  },

  async login(email, password) {
    const res = await fetch(`${BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    return handle(res)
  },

  async getProfile() {
    const res = await fetch(`${BASE_URL}/profile`, { headers: authHeaders() })
    return handle(res)
  },

  async updateProfile(profile) {
    const res = await fetch(`${BASE_URL}/profile`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', ...authHeaders() },
      body: JSON.stringify(profile),
    })
    return handle(res)
  },

  async generatePlan() {
    const res = await fetch(`${BASE_URL}/generate-plan`, { method: 'POST', headers: authHeaders() })
    return handle(res)
  },

  async listPlans() {
    const res = await fetch(`${BASE_URL}/plans`, { headers: authHeaders() })
    return handle(res)
  },

  async deletePlan(planId) {
    const res = await fetch(`${BASE_URL}/plans/${planId}`, { method: 'DELETE', headers: authHeaders() })
    return handle(res)
  },

  async uploadFile(planText, filename) {
    const form = new FormData()
    form.append('file', new Blob([planText], { type: 'text/plain' }), filename)
    const res = await fetch(`${BASE_URL}/upload`, { method: 'POST', headers: authHeaders(), body: form })
    return handle(res)
  },

  async listFiles() {
    const res = await fetch(`${BASE_URL}/files`, { headers: authHeaders() })
    return handle(res)
  },

  async deleteFile(fileId) {
    const res = await fetch(`${BASE_URL}/files/${fileId}`, { method: 'DELETE', headers: authHeaders() })
    return handle(res)
  },
}
