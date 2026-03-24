export default function LoadingSpinner({ className = '' }: { className?: string }) {
  return (
    <div className={`flex items-center justify-center py-20 ${className}`}>
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-primary" />
    </div>
  );
}
