import React, { HTMLAttributes } from 'react';

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export function Card({ children, className = '', ...props }: CardProps) {
  return (
    <div className={`glass-panel ${className}`} style={{ padding: '20px' }} {...props}>
      {children}
    </div>
  );
}
