import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await register(form.name, form.email, form.password)
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
        <div className="text-2xl font-bold grad-text mb-1">Create your account</div>
        <p className="text-sm text-muted mb-6">Sample details only — this is a course demo, not a medical service.</p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-xs text-muted">Name</label>
            <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
          </div>
          <div>
            <label className="text-xs text-muted">Email</label>
            <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          </div>
          <div>
            <label className="text-xs text-muted">Password</label>
            <input type="password" minLength={6} value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
          </div>
          {error && <p className="text-sm text-amber">{error}</p>}
          <button className="btn w-full" disabled={loading}>{loading ? 'Creating account…' : 'Create account'}</button>
        </form>
        <p className="text-xs text-muted mt-4">Already have an account? <Link to="/login" className="text-cyan">Log in</Link></p>
      </div>
    </div>
  )
}
