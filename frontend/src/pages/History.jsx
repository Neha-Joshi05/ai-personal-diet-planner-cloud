import { useEffect, useState } from 'react'
import { api } from '../services/api.js'
import PlanCard from '../components/PlanCard.jsx'

export default function History() {
  const [plans, setPlans] = useState([])
  const [loading, setLoading] = useState(true)
  const [openId, setOpenId] = useState(null)

  useEffect(() => {
    api.listPlans().then(setPlans).finally(() => setLoading(false))
  }, [])

  async function handleDelete(planId) {
    await api.deletePlan(planId)
    setPlans(plans.filter((p) => p.plan_id !== planId))
  }

  const max = Math.max(1, ...plans.map((p) => p.nutrition_summary?.totals?.cal || 0))

  return (
    <div className="card p-6">
      <h2 className="text-lg font-semibold mb-2">Plan history</h2>
      <p className="text-xs text-muted mb-4">
        Every plan you generate is saved here, mirroring how it would live in a cloud database's plans collection.
      </p>

      {loading ? (
        <p className="text-muted text-sm">Loading…</p>
      ) : plans.length === 0 ? (
        <p className="text-sm text-muted">No history yet — generate your first plan.</p>
      ) : (
        <>
          <div className="mb-5">
            <div className="text-xs text-muted mb-2">Calorie trend (oldest to newest, right = most recent)</div>
            <div className="flex items-end gap-1 h-20">
              {plans.slice(0, 14).reverse().map((p) => (
                <div
                  key={p.plan_id}
                  title={`${p.nutrition_summary.totals.cal} kcal`}
                  className="rounded w-[10px]"
                  style={{
                    height: Math.max(6, Math.round((p.nutrition_summary.totals.cal / max) * 80)),
                    background: 'linear-gradient(90deg,#6ee7a8,#3ac6e0)',
                  }}
                />
              ))}
            </div>
          </div>

          <div className="space-y-3">
            {plans.map((p) => (
              <div key={p.plan_id} className="card">
                <button
                  onClick={() => setOpenId(openId === p.plan_id ? null : p.plan_id)}
                  className="w-full text-left px-4 py-3 text-sm"
                >
                  {new Date(p.created_at).toLocaleString()} — {p.nutrition_summary.totals.cal} kcal · {p.goal}
                </button>
                {openId === p.plan_id && (
                  <div className="px-4 pb-4">
                    <PlanCard plan={p} onDelete={handleDelete} />
                  </div>
                )}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
