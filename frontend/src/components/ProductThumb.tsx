import { useState } from 'react';

export function ProductThumb({ src, alt, className }: { src: string | null; alt: string; className: string }) {
  const [failed, setFailed] = useState(false);

  if (!src || failed) {
    return <div className={className} />;
  }

  return <img src={src} alt={alt} className={className} onError={() => setFailed(true)} />;
}