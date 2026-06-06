'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { getAuthToken, removeAuthToken, apiJson } from '@/lib/api';
import { useRouter, usePathname } from 'next/navigation';

interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  isLoading: true,
  logout: () => {},
  checkAuth: async () => {},
});

export const useAuth = () => useContext(AuthContext);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  const logout = () => {
    removeAuthToken();
    setUser(null);
    router.push('/login');
  };

  const checkAuth = async () => {
    try {
      const token = getAuthToken();
      if (!token) {
        setUser(null);
        if (pathname !== '/login') {
          router.push('/login');
        }
        return;
      }
      // Assuming a /users/me endpoint exists, if not we can decode JWT, but let's try calling users/me
      const userData = await apiJson('/users/me');
      setUser(userData);
      if (pathname === '/login') {
        router.push('/');
      }
    } catch (err) {
      setUser(null);
      if (pathname !== '/login') {
        router.push('/login');
      }
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    checkAuth();
  }, [pathname]);

  return (
    <AuthContext.Provider value={{ user, isLoading, logout, checkAuth }}>
      {children}
    </AuthContext.Provider>
  );
}
