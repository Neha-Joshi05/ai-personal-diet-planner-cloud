import { createContext, useContext, useState, useCallback } from 'react'
import { api } from '../services/api.js'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem('nutricloud_token'))

  const login = useCallback(async (email, password) => {
    const { access_token } = await api.login(email, password)
    localStorage.setItem('nutricloud_token', access_token)
    setToken(access_token)
  }, [])

  const register = useCallback(async (name, email, password) => {
    const { access_token } = await api.register(name, email, password)
    localStorage.setItem('nutricloud_token', access_token)
    setToken(access_token)
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('nutricloud_token')
    setToken(null)
  }, [])

  return (
    <AuthContext.Provider value={{ token, isAuthenticated: !!token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
