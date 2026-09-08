import { createContext } from 'react';
import type { User } from '../types/api';
import type { LoginPayload } from '../types/auth';

export interface AuthContextValue {
  user: User | null;
  isLoading: boolean;
  login: (payload: LoginPayload) => Promise<void>;
  logout: () => void;
  setUser: (user: User) => void;
}

export const AuthContext = createContext<AuthContextValue | undefined>(undefined);