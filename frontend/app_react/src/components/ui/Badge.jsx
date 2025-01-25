// src/components/ui/Badge.jsx
import classNames from 'classnames';

export function Badge({ 
  children, 
  variant = 'default', 
  className, 
  ...props 
}) {
  const baseClasses = 'inline-block px-2 py-1 rounded-full text-xs font-medium';
  
  const variantClasses = {
    default: 'bg-gray-100 text-gray-800',
    critical: 'bg-red-500 text-white',
    high: 'bg-orange-500 text-white',
    medium: 'bg-yellow-500 text-white',
    low: 'bg-green-500 text-white'
  };

  return (
    <span
      className={classNames(
        baseClasses,
        variantClasses[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}