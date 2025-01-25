// src/components/ui/Card.jsx
import classNames from 'classnames';

export function Card({ 
  children, 
  className, 
  variant = 'default', 
  ...props 
}) {
  const baseClasses = 'rounded-lg shadow-md p-4';
  
  const variantClasses = {
    default: 'bg-gray-800 text-white',
    outlined: 'bg-transparent border border-gray-700',
    elevated: 'bg-gray-800 shadow-xl'
  };

  return (
    <div
      className={classNames(
        baseClasses,
        variantClasses[variant],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}