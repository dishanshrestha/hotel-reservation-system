import { useState } from 'react';
import { getImageUrl } from '../../api/client';

interface ImageWithFallbackProps {
  src: string | null | undefined;
  alt: string;
  className?: string;
  fallback?: string;
}

export default function ImageWithFallback({
  src,
  alt,
  className = '',
  fallback = '/images/room1.jpg',
}: ImageWithFallbackProps) {
  const [error, setError] = useState(false);
  const resolvedSrc = error ? fallback : getImageUrl(src);

  return (
    <img
      src={resolvedSrc}
      alt={alt}
      className={className}
      onError={() => setError(true)}
      loading="lazy"
    />
  );
}
