'use client';

import { useState } from 'react';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { UploadCloud, FileType, CheckCircle2, XCircle, AlertCircle } from 'lucide-react';
import { getAuthToken, API_BASE_URL } from '@/lib/api';

interface ImportResponse {
  id: string;
  status: string;
  total_rows: number;
  successful_rows: number;
  failed_rows: number;
  error_details: any[];
}

export default function ImportPage() {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [result, setResult] = useState<ImportResponse | null>(null);
  const [error, setError] = useState('');

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setResult(null);
      setError('');
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = getAuthToken();
      const response = await fetch(`${API_BASE_URL}/imports/csv`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
      setFile(null); // clear after successful dispatch
    } catch (err: any) {
      setError(err.message || 'An error occurred during upload.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ marginBottom: '24px' }}>
        <h2 style={{ fontSize: '24px', marginBottom: '8px' }}>Import CSV</h2>
        <p className="text-muted">Upload your financial movements via CSV file.</p>
      </div>

      <Card style={{ marginBottom: '24px' }}>
        <div style={{ 
          border: '2px dashed var(--border-color)', 
          borderRadius: 'var(--radius-md)', 
          padding: '40px 20px', 
          textAlign: 'center',
          backgroundColor: 'rgba(255, 255, 255, 0.02)',
          transition: 'all 0.2s ease',
        }}>
          {!file ? (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '12px' }}>
              <UploadCloud size={48} color="var(--primary-color)" style={{ opacity: 0.8 }} />
              <h3 style={{ fontSize: '18px', fontWeight: 500 }}>Select a CSV File</h3>
              <p className="text-muted" style={{ fontSize: '14px', maxWidth: '300px' }}>
                Ensure your CSV has the required headers: investor_id, category_id, type, amount, currency, status, movement_date.
              </p>
              
              <label style={{ marginTop: '16px', display: 'inline-block' }}>
                <input 
                  type="file" 
                  accept=".csv" 
                  onChange={handleFileChange} 
                  style={{ display: 'none' }} 
                />
                <span className="btn btn-secondary">Browse Files</span>
              </label>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
              <FileType size={48} color="var(--secondary-color)" />
              <div>
                <h3 style={{ fontSize: '16px', fontWeight: 500 }}>{file.name}</h3>
                <p className="text-muted" style={{ fontSize: '14px' }}>{(file.size / 1024).toFixed(2)} KB</p>
              </div>
              <div style={{ display: 'flex', gap: '12px', marginTop: '8px' }}>
                <Button variant="secondary" onClick={() => setFile(null)}>Cancel</Button>
                <Button onClick={handleUpload} isLoading={isUploading}>Upload Data</Button>
              </div>
            </div>
          )}
        </div>
        
        {error && (
          <div style={{ marginTop: '20px', padding: '16px', backgroundColor: 'rgba(239, 68, 68, 0.1)', borderRadius: 'var(--radius-sm)', display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
            <AlertCircle size={20} color="var(--danger-color)" style={{ flexShrink: 0 }} />
            <p className="text-danger" style={{ margin: 0, fontSize: '14px' }}>{error}</p>
          </div>
        )}
      </Card>

      {result && (
        <Card className="animate-fade-in" style={{ borderTop: `4px solid ${result.failed_rows > 0 ? 'var(--warning-color)' : 'var(--primary-color)'}` }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
            {result.failed_rows > 0 ? (
              <AlertCircle size={24} color="var(--warning-color)" />
            ) : (
              <CheckCircle2 size={24} color="var(--primary-color)" />
            )}
            <h3 style={{ fontSize: '18px' }}>Import Completed</h3>
          </div>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', marginBottom: '24px' }}>
            <div style={{ padding: '16px', backgroundColor: 'var(--surface-color)', borderRadius: 'var(--radius-sm)' }}>
              <p className="text-muted" style={{ fontSize: '13px', marginBottom: '4px' }}>Total Rows</p>
              <p style={{ fontSize: '24px', fontWeight: 600 }}>{result.total_rows}</p>
            </div>
            <div style={{ padding: '16px', backgroundColor: 'var(--surface-color)', borderRadius: 'var(--radius-sm)' }}>
              <p className="text-success" style={{ fontSize: '13px', marginBottom: '4px' }}>Successful</p>
              <p style={{ fontSize: '24px', fontWeight: 600 }}>{result.successful_rows}</p>
            </div>
            <div style={{ padding: '16px', backgroundColor: 'var(--surface-color)', borderRadius: 'var(--radius-sm)' }}>
              <p className="text-danger" style={{ fontSize: '13px', marginBottom: '4px' }}>Failed</p>
              <p style={{ fontSize: '24px', fontWeight: 600 }}>{result.failed_rows}</p>
            </div>
          </div>

          {result.error_details && result.error_details.length > 0 && (
            <div>
              <h4 style={{ fontSize: '15px', marginBottom: '12px', color: 'var(--danger-color)' }}>Error Details</h4>
              <div style={{ maxHeight: '300px', overflowY: 'auto', backgroundColor: 'var(--bg-color)', border: '1px solid var(--border-color)', borderRadius: 'var(--radius-sm)' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '13px' }}>
                  <thead>
                    <tr>
                      <th style={{ padding: '10px 16px', borderBottom: '1px solid var(--border-color)', textAlign: 'left', color: 'var(--text-secondary)' }}>Row</th>
                      <th style={{ padding: '10px 16px', borderBottom: '1px solid var(--border-color)', textAlign: 'left', color: 'var(--text-secondary)' }}>Error</th>
                    </tr>
                  </thead>
                  <tbody>
                    {result.error_details.map((err, idx) => (
                      <tr key={idx}>
                        <td style={{ padding: '10px 16px', borderBottom: '1px solid var(--border-color)', width: '80px' }}>{err.row}</td>
                        <td style={{ padding: '10px 16px', borderBottom: '1px solid var(--border-color)' }}>{JSON.stringify(err.errors)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </Card>
      )}
    </div>
  );
}
