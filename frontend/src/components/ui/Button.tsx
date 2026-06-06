import React, { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  isLoading?: boolean;
}

export function Button({ variant = 'primary', isLoading, children, className = '', disabled, ...props }: ButtonProps) {
  const baseClass = 'btn';
  const variantClass = `btn-${variant}`;
  const classes = `${baseClass} ${variantClass} ${className}`;

  return (
    <button className={classes} disabled={isLoading || disabled} {...props}>
      {isLoading ? (
        <span className="loader" style={{ width: '1em', height: '1em', border: '2px solid transparent', borderTopColor: 'currentColor', borderRadius: '50%', animation: 'spin 1s linear infinite' }}></span>
      ) : null}
      {children}
    </button>
  );
}
