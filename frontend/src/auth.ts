import { createContext, useContext, useMemo, useState } from 'react';

import { postEnveloped, setAccessToken } from './api';
import type { Role } from './types';

type AuthState = {
  access: string | null;
  refresh: string | null;
  role: Role | null;
};

type LoginResponse = {
  access: string;
  refresh: string;
};

interface AuthContextType {
  auth: AuthState;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [auth, setAuth] = useState<AuthState>({ access: null, refresh: null, role: null });

  const login = async (username: string, password: string) => {
    const data = await postEnveloped<LoginResponse, { username: string; password: string }>(
      '/accounts/login/',
      { username, password },
    );
    setAccessToken(data.access);

    const parsed = JSON.parse(atob(data.access.split('.')[1])) as { role?: Role };
    setAuth({ access: data.access, refresh: data.refresh, role: parsed.role || null });
  };

  const logout = () => {
    setAccessToken(null);
    setAuth({ access: null, refresh: null, role: null });
  };

  const value = useMemo(() => ({ auth, login, logout }), [auth]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
};
