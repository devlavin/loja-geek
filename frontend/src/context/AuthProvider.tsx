import { useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { User } from '../types/api';
import type { LoginPayload } from '../types/auth';
import { login as loginRequest, getMe } from '../api/auth';
import { AuthContext } from './auth-context';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');

    if (!token) {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- reset intencional ao deslogar
      setIsLoading(false);
      return;
    }

    let ignore = false;

    getMe()
      .then((data) => {
        if (!ignore) setUser(data);
      })
      .catch(() => {
        if (!ignore) localStorage.removeItem('token');
      })
      .finally(() => {
        if (!ignore) setIsLoading(false);
      });

    return () => { ignore = true; };
  }, []);

  async function login(payload: LoginPayload) {
    const { access_token } = await loginRequest(payload);
    localStorage.setItem('token', access_token);
    const me = await getMe();
    setUser(me);
  }

  function logout() {
    localStorage.removeItem('token');
    setUser(null);
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}