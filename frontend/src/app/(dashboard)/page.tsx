'use client';

import { useEffect, useState } from 'react';
import { apiJson } from '@/lib/api';
import { Card } from '@/components/ui/Card';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip as RechartsTooltip, Legend } from 'recharts';
import { ArrowUpRight, ArrowDownRight, Activity } from 'lucide-react';

interface Balance {
  currency: string;
  total_deposits: string;
  total_withdrawals: string;
  balance: string;
}

interface CategoryDist {
  category_name: string;
  total_amount: string;
  percentage: string;
}

interface DashboardData {
  total_movements: number;
  balances: Balance[];
  category_distribution: CategoryDist[];
}

const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const res = await apiJson('/dashboard/metrics');
        setData(res);
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, []);

  if (isLoading) {
    return <div>Loading dashboard data...</div>;
  }

  if (!data) {
    return <div>Failed to load dashboard data.</div>;
  }

  // Use the primary balance (e.g. USD) for the main cards
  const primaryBalance = data.balances[0] || { total_deposits: '0', total_withdrawals: '0', balance: '0', currency: 'USD' };

  const pieData = data.category_distribution.map(c => ({
    name: c.category_name,
    value: parseFloat(c.total_amount)
  }));

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      
      {/* Metric Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '24px' }}>
        <Card style={{ borderTop: '4px solid var(--primary-color)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>Current Balance ({primaryBalance.currency})</h3>
            <Activity size={20} color="var(--primary-color)" />
          </div>
          <div style={{ fontSize: '32px', fontWeight: 700 }}>
            ${parseFloat(primaryBalance.balance).toLocaleString('en-US', { minimumFractionDigits: 2 })}
          </div>
        </Card>

        <Card style={{ borderTop: '4px solid var(--primary-color)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>Total Deposits</h3>
            <ArrowUpRight size={20} color="var(--primary-color)" />
          </div>
          <div style={{ fontSize: '28px', fontWeight: 600 }}>
            ${parseFloat(primaryBalance.total_deposits).toLocaleString('en-US', { minimumFractionDigits: 2 })}
          </div>
        </Card>

        <Card style={{ borderTop: '4px solid var(--danger-color)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h3 style={{ fontSize: '14px', color: 'var(--text-secondary)' }}>Total Withdrawals</h3>
            <ArrowDownRight size={20} color="var(--danger-color)" />
          </div>
          <div style={{ fontSize: '28px', fontWeight: 600 }}>
            ${parseFloat(primaryBalance.total_withdrawals).toLocaleString('en-US', { minimumFractionDigits: 2 })}
          </div>
        </Card>
      </div>

      {/* Charts Section */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '24px' }}>
        <Card>
          <h3 style={{ marginBottom: '20px' }}>Category Distribution</h3>
          {pieData.length > 0 ? (
            <div style={{ height: '300px' }}>
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                    stroke="none"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <RechartsTooltip 
                    formatter={(value: any) => `$${Number(value).toLocaleString('en-US', { minimumFractionDigits: 2 })}`}
                    contentStyle={{ backgroundColor: 'var(--surface-color)', borderColor: 'var(--border-color)', borderRadius: 'var(--radius-sm)' }}
                  />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <div style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
              No category data available
            </div>
          )}
        </Card>
      </div>

    </div>
  );
}
