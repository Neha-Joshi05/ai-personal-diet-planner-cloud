import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api.js'

const initial = { age: '', sex: 'female', height_cm: '', weight_kg: '', activity_level: 'moderate', dietary_preference: 'veg', goal: 'maintain' }

export default function Profile() {
  const [form, setForm] = useState(initial)
  const [status, setStatus] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    api.getProfile().then((p) => {
      if (p.age) setForm({
        age: p.age, sex: p.sex, height_cm: p.height_cm, weight_kg: p.weight_kg,
        activity_level: p.activity_level, dietary_preference: p.dietary_preference, goal: p.goal,
      })
    })
  }, [])

  async function handleSubmit(e) {
    e.preventDefault()
    setStatus('Saving…')
    try {
      await api.updateProfile({
        ...form,
        age: Number(form.age), height_cm: Number(form.height_cm), weight_kg: Number(form.weight_kg),
      })
      setStatus('Saved profile')
      navigate('/app/generate')
    } catch (err) {
      setStatus(err.message)
    }
  }

  function set(field) {
    return (e) => setForm({ ...form, [field]: e.target.value })
  }

  return (
    <div className="card p-6 max-w-2xl">
      <h2 className="text-lg font-semibold mb-4">Your profile</h2>
      <form onSubmit={handleSubmit} className="grid sm:grid-cols-2 gap-4">
        <div><label className="text-xs text-muted">Age</label><input type="number" min="10" max="100" value={form.age} onChange={set('age')} required /></div>
        <div>
          <label className="text-xs text-muted">Sex</label>
          <select value={form.sex} onChange={set('sex')}>
            <option value="female">Female</option>
            <option value="male">Male</option>
          </select>
        </div>
        <div><label className="text-xs text-muted">Height (cm)</label><input type="number" value={form.height_cm} onChange={set('height_cm')} required /></div>
        <div><label className="text-xs text-muted">Weight (kg)</label><input type="number" value={form.weight_kg} onChange={set('weight_kg')} required /></div>
        <div>
          <label className="text-xs text-muted">Activity level</label>
          <select value={form.activity_level} onChange={set('activity_level')}>
            <option value="sedentary">Sedentary</option>
            <option value="light">Light</option>
            <option value="moderate">Moderate</option>
            <option value="active">Active</option>
          </select>
        </div>
        <div>
          <label className="text-xs text-muted">Dietary preference</label>
          <select value={form.dietary_preference} onChange={set('dietary_preference')}>
            <option value="veg">Vegetarian</option>
            <option value="vegan">Vegan</option>
            <option value="nonveg">Non-vegetarian</option>
          </select>
        </div>
        <div>
          <label className="text-xs text-muted">Goal</label>
          <select value={form.goal} onChange={set('goal')}>
            <option value="maintain">Maintain</option>
            <option value="lose">Weight loss</option>
            <option value="gain">Weight gain</option>
          </select>
        </div>
        <div className="sm:col-span-2 flex items-center gap-3 pt-2">
          <button className="btn">Save profile</button>
          <span className="text-[11px] text-muted">{status || 'Used only to estimate calorie/macro targets. Not medical advice.'}</span>
        </div>
      </form>
    </div>
  )
}
