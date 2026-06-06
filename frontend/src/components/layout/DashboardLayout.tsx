'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import { LayoutDashboard, ArrowRightLeft, Upload, FileBarChart, LogOut } from 'lucide-react';

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  const { user, logout, isLoading } = useAuth();
  const pathname = usePathname();

  if (isLoading) {
    return <div style={{ display: 'flex', height: '100vh', alignItems: 'center', justifyContent: 'center' }}>Loading...</div>;
  }

  // Basic protection
  if (!user) {
    return null; // Will redirect in AuthContext
  }

  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Movements', path: '/movements', icon: ArrowRightLeft },
    { name: 'Import CSV', path: '/import', icon: Upload },
    { name: 'Reports', path: '/reports', icon: FileBarChart },
  ];

  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
      {/* Sidebar */}
      <aside style={{
        width: 'var(--sidebar-width)',
        backgroundColor: 'var(--surface-color)',
        borderRight: '1px solid var(--border-color)',
        display: 'flex',
        flexDirection: 'column',
        padding: '20px 0',
      }}>
        <div style={{ padding: '0 20px', marginBottom: '40px' }}>
          <h1 style={{ color: 'var(--primary-color)', fontSize: '24px' }}>FinTrack</h1>
        </div>

        <nav style={{ flex: 1 }}>
          <ul style={{ listStyle: 'none', padding: 0 }}>
            {navItems.map((item) => {
              const isActive = pathname === item.path || (item.path !== '/' && pathname.startsWith(item.path));
              return (
                <li key={item.path} style={{ marginBottom: '4px', padding: '0 12px' }}>
                  <Link href={item.path} style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '12px',
                    padding: '10px 16px',
                    borderRadius: 'var(--radius-sm)',
                    backgroundColor: isActive ? 'var(--primary-glow)' : 'transparent',
                    color: isActive ? 'var(--primary-color)' : 'var(--text-secondary)',
                    fontWeight: isActive ? 600 : 500,
                  }}>
                    <item.icon size={20} />
                    {item.name}
                  </Link>
                </li>
              );
            })}
          </ul>
        </nav>

        <div style={{ padding: '20px', borderTop: '1px solid var(--border-color)' }}>
          <div style={{ marginBottom: '16px' }}>
            <p style={{ fontWeight: 600, fontSize: '14px', margin: 0 }}>{user.full_name}</p>
            <p className="text-muted" style={{ fontSize: '12px', margin: 0 }}>{user.email}</p>
          </div>
          <button 
            onClick={logout}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              background: 'none',
              border: 'none',
              color: 'var(--text-secondary)',
              cursor: 'pointer',
              padding: '8px 0',
              fontWeight: 500,
              fontSize: '14px',
              width: '100%',
            }}
          >
            <LogOut size={18} />
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        {/* Topbar */}
        <header style={{
          height: 'var(--header-height)',
          borderBottom: '1px solid var(--border-color)',
          display: 'flex',
          alignItems: 'center',
          padding: '0 30px',
          backgroundColor: 'rgba(11, 15, 25, 0.8)',
          backdropFilter: 'blur(8px)',
          zIndex: 10,
        }}>
          <h2 style={{ fontSize: '20px', fontWeight: 600 }}>
            {navItems.find(i => i.path === pathname || (i.path !== '/' && pathname.startsWith(i.path)))?.name || 'Dashboard'}
          </h2>
        </header>

        {/* Page Content */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '30px' }} className="animate-fade-in">
          {children}
        </div>
      </main>
    </div>
  );
}
