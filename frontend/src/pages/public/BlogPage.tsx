import { Calendar, ArrowRight } from 'lucide-react';

const blogPosts = [
  {
    id: 1,
    title: 'Discover the Best Travel Destinations for 2024',
    excerpt:
      'Explore the top travel destinations that promise unforgettable experiences. From exotic beaches to cultural hotspots, find your perfect getaway.',
    image: '/images/blog/blog1.jpg',
    date: 'January 15, 2024',
    category: 'Travel',
  },
  {
    id: 2,
    title: 'Tips for a Perfect Hotel Stay Experience',
    excerpt:
      'Make the most of your hotel stay with these insider tips. Learn how to get room upgrades, access exclusive amenities, and more.',
    image: '/images/blog/blog2.jpg',
    date: 'February 20, 2024',
    category: 'Tips',
  },
  {
    id: 3,
    title: 'The Ultimate Guide to Luxury Hospitality',
    excerpt:
      'What defines luxury in the modern hospitality industry? We explore the trends, innovations, and standards that set premium hotels apart.',
    image: '/images/blog/blog3.jpg',
    date: 'March 10, 2024',
    category: 'Luxury',
  },
];

export default function BlogPage() {
  return (
    <div>
      {/* Header */}
      <section className="bg-brand-dark py-16 text-center">
        <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">Our Blog</h1>
        <p className="text-gray-300">Latest news, tips, and stories</p>
      </section>

      {/* Blog Grid */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {blogPosts.map((post) => (
              <article
                key={post.id}
                className="bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition-shadow group"
              >
                <div className="relative h-52 overflow-hidden">
                  <img
                    src={post.image}
                    alt={post.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    onError={(e) => { (e.target as HTMLImageElement).src = '/images/room/room1.jpg'; }}
                  />
                  <span className="absolute top-3 left-3 bg-brand-primary text-white text-xs font-semibold px-3 py-1 rounded-full">
                    {post.category}
                  </span>
                </div>
                <div className="p-6">
                  <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
                    <Calendar size={14} />
                    <span>{post.date}</span>
                  </div>
                  <h3 className="text-lg font-semibold text-brand-ink mb-2 line-clamp-2">
                    {post.title}
                  </h3>
                  <p className="text-sm text-gray-600 mb-4 line-clamp-3">{post.excerpt}</p>
                  <button className="flex items-center gap-1 text-sm font-medium text-brand-primary hover:text-brand-primary-dark transition-colors">
                    Read More <ArrowRight size={14} />
                  </button>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
