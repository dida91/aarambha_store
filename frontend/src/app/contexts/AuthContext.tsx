import { createContext, useCallback, useEffect, useMemo, useState, type ReactNode } from 'react'

import { clearStoredTokens, getStoredTokens, setStoredTokens } from '../../lib/api'
import type { ApiErrorShape } from '../../types/api'
import type { LoginPayload, RegisterPayload, User } from '../../types/auth'
import { fetchCurrentUser, login, register } from '../../features/auth/service'

interface AuthContextValue {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  loginUser: (payload: LoginPayload) => Promise<void>
  registerUser: (payload: RegisterPayload) => Promise<void>
  logoutUser: () => void
  refreshUser: () => Promise<void>
}

export const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  const refreshUser = useCallback(async () => {
    const tokens = getStoredTokens()
    if (!tokens) {
      setUser(null)
      return
    }

    const data = await fetchCurrentUser()
    setUser(data)
  }, [])

  useEffect(() => {
    const init = async () => {
      try {
        await refreshUser()
      } catch {
        clearStoredTokens()
        setUser(null)
      } finally {
        setIsLoading(false)
      }
    }

    void init()
  }, [refreshUser])

  const loginUser = useCallback(async (payload: LoginPayload) => {
    const tokens = await login(payload)
    setStoredTokens(tokens)
    await refreshUser()
  }, [refreshUser])

  const registerUser = useCallback(async (payload: RegisterPayload) => {
    await register(payload)
    await loginUser({ username: payload.username, password: payload.password })
  }, [loginUser])

  const logoutUser = useCallback(() => {
    clearStoredTokens()
    setUser(null)
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      isAuthenticated: Boolean(user),
      isLoading,
      loginUser,
      registerUser,
      logoutUser,
      refreshUser,
    }),
    [user, isLoading, loginUser, registerUser, logoutUser, refreshUser],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export type { ApiErrorShape }
