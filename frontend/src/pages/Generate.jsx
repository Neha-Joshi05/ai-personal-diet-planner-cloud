import { useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../services/api.js'
import PlanCard from '../components/PlanCard.jsx'

export default function Generate() {
  const [plan, setPlan] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [exported, setExported] = useState('')

  async function handleGenerate() {
    setLoading(true)
    setError('')
    try {
      const result = await api.generatePlan()
      setPlan(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleExport(p) {
    const text = buildExportText(p)
    await api.uploadFile(text, `diet-plan-${p.plan_id}.txt`)
    setExported(`Saved diet-plan-${p.plan_id}.txt to Cloud files.`)
  }

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between flex-wrap gap-3 mb-4">
        <h2 className="text-lg font-semibold">Generate AI diet plan</h2>
        <button onClick={handleGenerate} className="btn" disabled={loading}>
          {loading ? 'Generating…' : 'Generate plan'}
        </button>
      </div>

      {error === 'Complete your profile before generating a plan.' && (
        <p className="text-sm text-amber mb-3">
          Complete your <Link to="/app/profile" className="text-cyan">profile</Link> first.
        </p>
      )}
      {error && error !== 'Complete your profile before generating a plan.' && (
        <p className="text-sm text-amber mb-3">{error}</p>
      )}

      {plan ? (
        <>
          <PlanCard plan={plan} onExport={handleExport} />
          {exported && <p className="text-xs text-mint mt-3">{exported}</p>}
        </>
      ) : (
        <p className="text-sm text-muted">Complete your profile, then generate a personalized plan.</p>
      )}
    </div>
  )
}

function buildExportText(plan) {
  const t = plan.nutrition_summary.target
  const tot = plan.nutrition_summary.totals
  return `NutriCloud diet plan, ${new Date(plan.created_at).toLocaleString()}
Goal: ${plan.goal} | Diet: ${plan.dietary_preference}
Target: ${t.cal} kcal (BMR ${t.bmr}, TDEE ${t.tdee})
Macro target — P:${t.macros.p}g C:${t.macros.c}g F:${t.macros.f}g

Breakfast: ${plan.breakfast.name} (${plan.breakfast.kcal} kcal)
Lunch: ${plan.lunch.name} (${plan.lunch.kcal} kcal)
Snack: ${plan.snack.name} (${plan.snack.kcal} kcal)
Dinner: ${plan.dinner.name} (${plan.dinner.kcal} kcal)

Totals: ${tot.cal} kcal, P${tot.p}g C${tot.c}g F${tot.f}g
Educational demo output, not medical advice.`
}
