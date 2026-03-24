import { Link } from 'react-router-dom';
import { MapPin, Phone, Mail } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-brand-dark text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
          {/* About */}
          <div>
            <h3 className="text-xl font-bold text-white mb-4">
              Starter<span className="text-brand-gold">Hotel</span>
            </h3>
            <p className="text-sm leading-relaxed text-gray-400">
              Experience luxury and comfort at our premium hotel. We provide the best rooms and services for an unforgettable stay.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              {[
                { to: '/', label: 'Home' },
                { to: '/about', label: 'About' },
                { to: '/rooms', label: 'Rooms' },
                { to: '/gallery', label: 'Gallery' },
                { to: '/contact', label: 'Contact' },
              ].map((link) => (
                <li key={link.to}>
                  <Link to={link.to} className="hover:text-brand-gold transition-colors">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">Contact Info</h4>
            <ul className="space-y-3 text-sm">
              <li className="flex items-start gap-2">
                <MapPin size={16} className="text-brand-gold mt-0.5 flex-shrink-0" />
                <span>Location of Hotel, City, Country</span>
              </li>
              <li className="flex items-center gap-2">
                <Phone size={16} className="text-brand-gold flex-shrink-0" />
                <span>+12 1234567890</span>
              </li>
              <li className="flex items-center gap-2">
                <Mail size={16} className="text-brand-gold flex-shrink-0" />
                <span>demo@gmail.com</span>
              </li>
            </ul>
          </div>

          {/* Newsletter */}
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">Newsletter</h4>
            <p className="text-sm text-gray-400 mb-4">
              Subscribe to get updates on our latest offers.
            </p>
            <form
              onSubmit={(e) => e.preventDefault()}
              className="flex"
            >
              <input
                type="email"
                placeholder="Your Email"
                className="flex-1 px-3 py-2 bg-brand-dark-light border border-gray-600 rounded-l-md text-sm text-white placeholder-gray-500 focus:outline-none focus:border-brand-gold"
              />
              <button
                type="submit"
                className="px-4 py-2 bg-brand-gold text-brand-dark text-sm font-semibold rounded-r-md hover:bg-brand-gold/90 transition-colors"
              >
                Subscribe
              </button>
            </form>
          </div>
        </div>
      </div>

      {/* Bottom bar */}
      <div className="border-t border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 text-center text-sm text-gray-500">
          &copy; {new Date().getFullYear()} StarterHotel. All Rights Reserved.
        </div>
      </div>
    </footer>
  );
}
