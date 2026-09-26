import { Link } from 'react-router-dom'

export default function Landing() {
  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="max-w-lg text-center">
        <div className="text-3xl font-bold grad-text mb-3">NutriCloud</div>
        <p className="text-muted mb-8">
          Personalized meal plans, calculated from your goals with a rule-based AI engine,
          and saved to a cloud-backed dashboard you can reach from any device.
        </p>
        <div className="flex gap-3 justify-center">
          <Link to="/register" className="btn">Create account</Link>
          <Link to="/login" className="btn-ghost">Log in</Link>
        </div>
        <p className="text-[11px] text-muted mt-8">
          A Cloud Computing course project. Use sample details, not real health information —
          generated plans are educational estimates, not medical advice.
        </p>
      </div>
    </div>
  )
}
