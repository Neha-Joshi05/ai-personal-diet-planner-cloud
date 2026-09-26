import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../services/api.js'
import PlanCard from '../components/PlanCard.jsx'

function todayKey() {
  return 'nutricloud_water_' + new Date().toISOString().slice(0, 10)
}

export default function Dashboard() {
  const [profile, setProfile] = useState(null)
  const [plans, setPlans] = useState([])
  const [loading, setLoading] = useState(true)
  const [water, setWater] = useState(() => Number(localStorage.getItem(todayKey())) || 0)

  useEffect(() => {
    Promise.all([api.getProfile(), api.listPlans()])
      .then(([p, pl]) => { setProfile(p); setPlans(pl) })
      .finally(() => setLoading(false))
  }, [])

  function addWater() {
    const next = Math.min(8, water + 1)
    setWater(next)
    localStorage.setItem(todayKey(), String(next))
  }

  const latest = plans[0]
  const totals = latest?.nutrition_summary?.totals
  const target = latest?.nutrition_summary?.target

  let p1 = 0, p2 = 0
  if (totals) {
    const pk = totals.p * 4, ck = totals.c * 4, fk = totals.f * 9
    const tk = pk + ck + fk || 1
    p1 = Math.round((pk / tk) * 100)
    p2 = p1 + Math.round((ck / tk) * 100)
  }

  if (loading) return <p className="text-muted">Loading dashboard…</p>

  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-bold">Welcome, {profile?.name}</h1>
        <p className="text-sm text-muted mt-1">
          {profile?.goal ? `Goal: ${profile.goal} · ${profile.dietary_preference}` : (
            <>Complete your <Link to="/app/profile" className="text-cyan">profile</Link> to get started.</>
          )}
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-4">
        <div className="bg-panel2 rounded-r-2xl rounded-l pl-4 py-4 pr-5 border-l-[3px] border-mint">
          <div className="text-xs text-muted">Plans generated</div>
          <div className="text-2xl font-bold mt-1">{plans.length}</div>
        </div>
        <div className="bg-panel2 rounded-r-2xl rounded-l pl-4 py-4 pr-5 border-l-[3px] border-cyan">
          <div className="text-xs text-muted">Daily target</div>
          <div className="text-2xl font-bold mt-1">{target ? `${target.cal} kcal` : '—'}</div>
        </div>
        <div className="bg-panel2 rounded-r-2xl rounded-l pl-4 py-4 pr-5 border-l-[3px] border-amber">
          <div className="text-xs text-muted">Goal</div>
          <div className="text-2xl font-bold mt-1">{profile?.goal || '—'}</div>
        </div>
      </div>

      <div className="grid md:grid-cols-3 gap-4">
        <div className="md:col-span-2">
          <div className="text-sm font-semibold mb-3">Latest plan</div>
          {latest ? <PlanCard plan={latest} /> : (
            <div className="card p-5 text-sm text-muted">
              No plan yet — <Link to="/app/generate" className="text-cyan">generate one</Link> to see it here.
            </div>
          )}
        </div>
        <div className="card p-5 flex flex-col items-center justify-center">
          <div className="text-sm font-semibold mb-3 self-start">Macro split</div>
          {totals ? (
            <>
              <div
                className="w-28 h-28 rounded-full flex items-center justify-center"
                style={{ background: `conic-gradient(#6ee7a8 0 ${p1}%, #3ac6e0 ${p1}% ${p2}%, #f5b76e ${p2}% 100%)` }}
              >
                <div className="w-[72px] h-[72px] rounded-full bg-panel flex flex-col items-center justify-center">
                  <div className="text-xs font-bold">{totals.cal}</div>
                  <div className="text-[9px] text-muted">kcal</div>
                </div>
              </div>
              <div className="text-[11px] text-muted mt-3 space-y-1">
                <div>🟢 Protein {totals.p}g</div>
                <div>🔵 Carbs {totals.c}g</div>
                <div>🟠 Fat {totals.f}g</div>
              </div>
            </>
          ) : <p className="text-xs text-muted">Generate a plan to see your macro split.</p>}
        </div>
      </div>

      <div className="card p-5">
        <div className="flex items-center justify-between mb-3">
          <div className="text-sm font-semibold">💧 Hydration tracker</div>
          <span className="text-xs text-muted">{water}/8 glasses</span>
        </div>
        <div className="w-full rounded-full h-2 mb-3 bg-panel2">
          <div className="h-2 rounded-full" style={{ width: `${(water / 8) * 100}%`, background: 'linear-gradient(90deg,#6ee7a8,#3ac6e0)' }} />
        </div>
        <button onClick={addWater} className="btn-ghost">+ Add glass</button>
      </div>
    </div>
  )
}
