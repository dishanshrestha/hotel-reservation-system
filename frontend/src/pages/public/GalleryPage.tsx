import { useState, useEffect } from 'react';
import { X } from 'lucide-react';
import { fetchGallery } from '../../api/gallery';
import { getImageUrl } from '../../api/client';
import type { GalleryItem } from '../../types';

export default function GalleryPage() {
  const [items, setItems] = useState<GalleryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [lightbox, setLightbox] = useState<string | null>(null);

  useEffect(() => {
    fetchGallery()
      .then((res) => setItems(res.gallery))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  // Fallback static images if no API gallery items
  const staticImages = Array.from({ length: 8 }, (_, i) => `/gallary/gallery${i + 1}.jpg`);

  const displayImages = items.length > 0
    ? items.map((item) => getImageUrl(item.image))
    : staticImages;

  return (
    <div>
      {/* Header */}
      <section className="bg-brand-dark py-16 text-center">
        <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">Our Gallery</h1>
        <p className="text-gray-300">Explore our beautiful hotel and facilities</p>
      </section>

      {/* Gallery Grid */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {loading ? (
            <div className="flex justify-center py-20">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-primary" />
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {displayImages.map((src, index) => (
                <button
                  key={index}
                  onClick={() => setLightbox(src)}
                  className="relative overflow-hidden rounded-lg group aspect-square focus:outline-none focus:ring-2 focus:ring-brand-primary"
                >
                  <img
                    src={src}
                    alt={`Gallery ${index + 1}`}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                    onError={(e) => { (e.target as HTMLImageElement).src = '/images/room/room1.jpg'; }}
                  />
                  <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors flex items-center justify-center">
                    <span className="text-white opacity-0 group-hover:opacity-100 transition-opacity text-sm font-medium">
                      View
                    </span>
                  </div>
                </button>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Lightbox */}
      {lightbox && (
        <div
          className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4"
          onClick={() => setLightbox(null)}
        >
          <button
            onClick={() => setLightbox(null)}
            className="absolute top-4 right-4 text-white hover:text-gray-300 transition-colors"
          >
            <X size={32} />
          </button>
          <img
            src={lightbox}
            alt="Gallery preview"
            className="max-w-full max-h-[85vh] object-contain rounded-lg"
            onClick={(e) => e.stopPropagation()}
          />
        </div>
      )}
    </div>
  );
}
