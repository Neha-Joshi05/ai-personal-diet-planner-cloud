import { Routes, Route } from 'react-router-dom'
import Landing from './pages/Landing.jsx'
import Register from './pages/Register.jsx'
import Login from './pages/Login.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Profile from './pages/Profile.jsx'
import Generate from './pages/Generate.jsx'
import History from './pages/History.jsx'
import Files from './pages/Files.jsx'
import ProtectedLayout from './components/ProtectedLayout.jsx'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<Login />} />

      <Route path="/app" element={<ProtectedLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="profile" element={<Profile />} />
        <Route path="generate" element={<Generate />} />
        <Route path="history" element={<History />} />
        <Route path="files" element={<Files />} />
      </Route>
    </Routes>
  )
}
