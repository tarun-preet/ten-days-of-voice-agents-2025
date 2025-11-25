import React from 'react';
import { cn } from '@/lib/utils';

const BentoGrid = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn('grid w-full auto-rows-[22rem] grid-cols-3 gap-4', className)}
      {...props}
    />
  )
);
BentoGrid.displayName = 'BentoGrid';

const BentoCard = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & {
    className?: string;
    isLarge?: boolean;
  }
>(({ className, isLarge = false, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      'col-span-3 flex flex-col justify-between overflow-hidden rounded-xl',
      'bg-card transform-gpu [box-shadow:0_-20px_80px_-20px_rgba(79,179,200,0.06)_inset] [border:1px_solid_var(--border)]',
      {
        'md:col-span-2': isLarge,
        'md:col-span-1': !isLarge,
      },
      className
    )}
    {...props}
  />
));
BentoCard.displayName = 'BentoCard';

export { BentoCard, BentoGrid };
