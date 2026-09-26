const MEAL_ICONS = { breakfast: '🍳', lunch: '🥗', snack: '🍎', dinner: '🍛' }

export default function PlanCard({ plan, onExport, onDelete }) {
  const target = plan.nutrition_summary?.target || {}
  const totals = plan.nutrition_summary?.totals || {}

  return (
    <div className="card p-5">
      <div className="text-xs text-muted mb-2">
        {new Date(plan.created_at).toLocaleString()} · Goal: {plan.goal} · {plan.dietary_preference}
      </div>
      <div className="grid sm:grid-cols-2 gap-x-6">
        {['breakfast', 'lunch', 'snack', 'dinner'].map((slot) => (
          <div key={slot} className="flex justify-between py-2 border-b border-border">
            <span>{MEAL_ICONS[slot]} {plan[slot]?.name}</span>
            <span className="text-muted">{plan[slot]?.kcal} kcal</span>
          </div>
        ))}
      </div>
      <div className="mt-3 text-sm">
        Total: <b>{totals.cal} kcal</b> · P {totals.p}g · C {totals.c}g · F {totals.f}g
      </div>
      <div className="text-[11px] text-muted mt-1">
        Target: {target.cal} kcal (BMR {target.bmr}, TDEE {target.tdee}) — educational estimate, not medical advice.
      </div>
      {(onExport || onDelete) && (
        <div className="flex gap-2 mt-4">
          {onExport && <button onClick={() => onExport(plan)} className="btn-ghost">Export to cloud files</button>}
          {onDelete && <button onClick={() => onDelete(plan.plan_id)} className="btn-ghost">Delete</button>}
        </div>
      )}
    </div>
  )
}
