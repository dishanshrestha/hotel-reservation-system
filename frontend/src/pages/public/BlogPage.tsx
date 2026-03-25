import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Calendar, ArrowRight, User } from 'lucide-react';
import { fetchBlogs } from '../../api/blogs';
import { getImageUrl } from '../../api/client';
import type { Blog } from '../../types';

export default function BlogPage() {
  const [blogs, setBlogs] = useState<Blog[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedBlog, setSelectedBlog] = useState<Blog | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchBlogs()
      .then((res) => setBlogs(res.blogs))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (selectedBlog) {
    return (
      <div>
        <section className="bg-brand-dark py-16 text-center">
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-2 max-w-3xl mx-auto px-4">
            {selectedBlog.title}
          </h1>
          <div className="flex items-center justify-center gap-4 mt-3 text-gray-300 text-sm">
            {selectedBlog.author && (
              <span className="flex items-center gap-1">
                <User size={14} /> {selectedBlog.author}
              </span>
            )}
            <span className="flex items-center gap-1">
              <Calendar size={14} />
              {new Date(selectedBlog.created_at).toLocaleDateString('en-US', {
                year: 'numeric', month: 'long', day: 'numeric',
              })}
            </span>
            {selectedBlog.category && (
              <span className="bg-brand-primary/80 text-white text-xs px-2 py-0.5 rounded-full">
                {selectedBlog.category}
              </span>
            )}
          </div>
        </section>

        <article className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {selectedBlog.image && (
            <img
              src={getImageUrl(selectedBlog.image)}
              alt={selectedBlog.title}
              className="w-full h-72 md:h-96 object-cover rounded-lg mb-8"
            />
          )}
          <div className="prose prose-lg max-w-none text-gray-700 whitespace-pre-line leading-relaxed">
            {selectedBlog.content || selectedBlog.excerpt}
          </div>
          <button
            onClick={() => setSelectedBlog(null)}
            className="mt-8 px-6 py-2 border-2 border-brand-primary text-brand-primary font-medium rounded-md hover:bg-brand-primary hover:text-white transition-colors"
          >
            Back to Blog
          </button>
        </article>
      </div>
    );
  }

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
          {loading ? (
            <div className="flex justify-center py-20">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-primary" />
            </div>
          ) : blogs.length === 0 ? (
            <p className="text-center text-gray-500 py-20">No blog posts yet.</p>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {blogs.map((post) => (
                <article
                  key={post.id}
                  className="bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-md transition-shadow group cursor-pointer"
                  onClick={() => setSelectedBlog(post)}
                >
                  <div className="relative h-52 overflow-hidden">
                    <img
                      src={getImageUrl(post.image)}
                      alt={post.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                      onError={(e) => { (e.target as HTMLImageElement).src = '/images/room1.jpg'; }}
                    />
                    {post.category && (
                      <span className="absolute top-3 left-3 bg-brand-primary text-white text-xs font-semibold px-3 py-1 rounded-full">
                        {post.category}
                      </span>
                    )}
                  </div>
                  <div className="p-6">
                    <div className="flex items-center gap-3 text-sm text-gray-500 mb-3">
                      <span className="flex items-center gap-1">
                        <Calendar size={14} />
                        {new Date(post.created_at).toLocaleDateString('en-US', {
                          year: 'numeric', month: 'long', day: 'numeric',
                        })}
                      </span>
                      {post.author && (
                        <span className="flex items-center gap-1">
                          <User size={14} /> {post.author}
                        </span>
                      )}
                    </div>
                    <h3 className="text-lg font-semibold text-brand-ink mb-2 line-clamp-2">
                      {post.title}
                    </h3>
                    <p className="text-sm text-gray-600 mb-4 line-clamp-3">{post.excerpt}</p>
                    <span className="flex items-center gap-1 text-sm font-medium text-brand-primary hover:text-brand-primary-dark transition-colors">
                      Read More <ArrowRight size={14} />
                    </span>
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
