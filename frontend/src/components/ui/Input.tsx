import React, { InputHTMLAttributes, forwardRef } from 'react';

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(({ label, error, className = '', id, ...props }, ref) => {
  const inputId = id || props.name;
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginBottom: '16px' }}>
      {label && <label htmlFor={inputId} style={{ fontSize: '14px', fontWeight: 500 }}>{label}</label>}
      <input
        id={inputId}
        ref={ref}
        className={className}
        style={{ borderColor: error ? 'var(--danger-color)' : undefined }}
        {...props}
      />
      {error && <span style={{ color: 'var(--danger-color)', fontSize: '12px' }}>{error}</span>}
    </div>
  );
});

Input.displayName = 'Input';
