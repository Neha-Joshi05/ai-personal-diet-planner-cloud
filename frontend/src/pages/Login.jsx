import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function Login() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(form.email, form.password)
      navigate('/app')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="card w-full max-w-sm p-8">
        <div className="text-2xl font-bold grad-text mb-1">Log in</div>
        <p className="text-sm text-muted mb-6">Enter dashboard to pick up your saved plans.</p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-xs text-muted">Email</label>
            <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          </div>
          <div>
            <label className="text-xs text-muted">Password</label>
            <input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
          </div>
          {error && <p className="text-sm text-amber">{error}</p>}
          <button className="btn w-full" disabled={loading}>{loading ? 'Logging in…' : 'Enter dashboard'}</button>
        </form>
        <p className="text-xs text-muted mt-4">No account yet? <Link to="/register" className="text-cyan">Create one</Link></p>
      </div>
    </div>
  )
}
