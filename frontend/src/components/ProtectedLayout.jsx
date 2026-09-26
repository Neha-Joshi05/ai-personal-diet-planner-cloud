import { Navigate, NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'

const tabs = [
  { to: '/app', label: 'Dashboard', end: true },
  { to: '/app/profile', label: 'Profile' },
  { to: '/app/generate', label: 'Generate plan' },
  { to: '/app/history', label: 'History' },
  { to: '/app/files', label: 'Cloud files' },
]

export default function ProtectedLayout() {
  const { isAuthenticated, logout } = useAuth()

  if (!isAuthenticated) return <Navigate to="/login" replace />

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-10 backdrop-blur border-b border-border" style={{ background: 'rgba(7,11,18,.88)' }}>
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between gap-4">
          <div className="brand text-lg font-bold grad-text">NutriCloud</div>
          <nav className="hidden sm:flex gap-5 text-sm">
            {tabs.map((t) => (
              <NavLink
                key={t.to}
                to={t.to}
                end={t.end}
                className={({ isActive }) =>
                  `py-1 border-b-2 ${isActive ? 'border-cyan text-white' : 'border-transparent text-muted'}`
                }
              >
                {t.label}
              </NavLink>
            ))}
          </nav>
          <button onClick={logout} className="btn-ghost">Logout</button>
        </div>
        <nav className="flex sm:hidden gap-4 text-xs px-4 pb-2 overflow-x-auto">
          {tabs.map((t) => (
            <NavLink
              key={t.to}
              to={t.to}
              end={t.end}
              className={({ isActive }) =>
                `py-1 whitespace-nowrap border-b-2 ${isActive ? 'border-cyan text-white' : 'border-transparent text-muted'}`
              }
            >
              {t.label}
            </NavLink>
          ))}
        </nav>
      </header>
      <main className="max-w-6xl mx-auto px-4 py-6">
        <Outlet />
      </main>
    </div>
  )
}
