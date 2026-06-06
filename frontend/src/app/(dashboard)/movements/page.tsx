'use client';

import { useEffect, useState } from 'react';
import { apiJson, apiFetch } from '@/lib/api';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Download } from 'lucide-react';
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from '@tanstack/react-table';

interface Movement {
  id: string;
  type: string;
  amount: string;
  currency: string;
  status: string;
  movement_date: string;
  description: string | null;
  category: {
    id: string;
    name: string;
  } | null;
  investor: {
    id: string;
    name: string;
  };
}

const columnHelper = createColumnHelper<Movement>();

const columns = [
  columnHelper.accessor('movement_date', {
    header: 'Date',
    cell: info => new Date(info.getValue()).toLocaleDateString(),
  }),
  columnHelper.accessor('investor.name', {
    header: 'Investor',
    cell: info => info.getValue(),
  }),
  columnHelper.accessor('type', {
    header: 'Type',
    cell: info => {
      const type = info.getValue();
      const badgeClass = type === 'deposit' ? 'badge-success' : 'badge-danger';
      return <span className={`badge ${badgeClass}`}>{type}</span>;
    },
  }),
  columnHelper.accessor('amount', {
    header: 'Amount',
    cell: info => {
      const amount = parseFloat(info.getValue());
      const type = info.row.original.type;
      const formatted = amount.toLocaleString('en-US', { style: 'currency', currency: info.row.original.currency });
      return (
        <span style={{ fontWeight: 600, color: type === 'deposit' ? 'var(--primary-color)' : 'var(--text-primary)' }}>
          {type === 'withdrawal' ? '-' : '+'}{formatted}
        </span>
      );
    },
  }),
  columnHelper.accessor('category.name', {
    header: 'Category',
    cell: info => info.getValue() || '-',
  }),
  columnHelper.accessor('status', {
    header: 'Status',
    cell: info => {
      const status = info.getValue();
      let badgeClass = 'badge-secondary';
      if (status === 'completed') badgeClass = 'badge-success';
      if (status === 'pending') badgeClass = 'badge-warning';
      if (status === 'failed') badgeClass = 'badge-danger';
      
      return <span className={`badge ${badgeClass}`}>{status}</span>;
    },
  }),
  columnHelper.accessor('description', {
    header: 'Description',
    cell: info => <span className="text-muted">{info.getValue() || '-'}</span>,
  }),
];

export default function MovementsPage() {
  const [data, setData] = useState<Movement[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const res = await apiJson('/financial-movements');
        setData(res.items || res); // Assuming pagination or direct array
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    }
    loadData();
  }, []);

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  const handleExport = async () => {
    try {
      const res = await apiFetch('/exports/movements/csv');
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'movements_export.csv';
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (err) {
      console.error('Export failed', err);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '24px', marginBottom: '8px' }}>Financial Movements</h2>
          <p className="text-muted">Track all deposits and withdrawals in real-time.</p>
        </div>
        <Button onClick={handleExport} variant="secondary">
          <Download size={16} />
          Export CSV
        </Button>
      </div>

      <Card style={{ padding: 0, overflow: 'hidden' }}>
        {isLoading ? (
          <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>Loading...</div>
        ) : data.length === 0 ? (
           <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>No movements found.</div>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                {table.getHeaderGroups().map(headerGroup => (
                  <tr key={headerGroup.id}>
                    {headerGroup.headers.map(header => (
                      <th key={header.id}>
                        {header.isPlaceholder
                          ? null
                          : flexRender(
                              header.column.columnDef.header,
                              header.getContext()
                            )}
                      </th>
                    ))}
                  </tr>
                ))}
              </thead>
              <tbody>
                {table.getRowModel().rows.map(row => (
                  <tr key={row.id}>
                    {row.getVisibleCells().map(cell => (
                      <td key={cell.id}>
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
}
