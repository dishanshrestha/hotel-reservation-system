import { useState, useEffect, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ChevronLeft, ChevronRight, Wifi, Star, MapPin, Phone, Mail } from 'lucide-react';
import { fetchRooms } from '../../api/rooms';
import { submitContact } from '../../api/contacts';
import { getImageUrl } from '../../api/client';
import type { Room } from '../../types';
import toast from 'react-hot-toast';

const bannerSlides = [
  {
    image: '/images/banner1.jpg',
    title: 'Welcome to StarterHotel',
    subtitle: 'Your home in the heart of Thamel, Kathmandu',
  },
  {
    image: '/images/banner2.jpg',
    title: 'Himalayan Views',
    subtitle: 'Wake up to the majestic mountains of Nepal',
  },
  {
    image: '/images/banner3.jpg',
    title: 'Book Your Stay',
    subtitle: 'Best rates in Thamel, guaranteed',
  },
];

export default function HomePage() {
  const navigate = useNavigate();
  const [currentSlide, setCurrentSlide] = useState(0);
  const [rooms, setRooms] = useState<Room[]>([]);
  const [arrival, setArrival] = useState('');
  const [departure, setDeparture] = useState('');

  useEffect(() => {
    fetchRooms().then((res) => setRooms(res.rooms.slice(0, 6))).catch(() => {});
  }, []);

  // Auto-advance carousel
  const nextSlide = useCallback(() => {
    setCurrentSlide((prev) => (prev + 1) % bannerSlides.length);
  }, []);

  useEffect(() => {
    const timer = setInterval(nextSlide, 5000);
    return () => clearInterval(timer);
  }, [nextSlide]);

  const prevSlide = () => setCurrentSlide((prev) => (prev - 1 + bannerSlides.length) % bannerSlides.length);

  const handleBookingSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams();
    if (arrival) params.set('arrival', arrival);
    if (departure) params.set('departure', departure);
    navigate(`/rooms?${params.toString()}`);
  };

  const [contactForm, setContactForm] = useState({ name: '', email: '', phone: '', message: '' });
  const handleContactSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const result = await submitContact(contactForm);
      if (result.email_confirmation_sent) {
        toast.success('Message sent! A confirmation has been emailed to you.', { duration: 5000 });
      } else {
        toast.success('Message sent successfully!');
      }
      setContactForm({ name: '', email: '', phone: '', message: '' });
    } catch {
      toast.error('Failed to send message');
    }
  };

  return (
    <div>
      {/* Hero Carousel */}
      <section className="relative h-[600px] md:h-[700px] overflow-hidden">
        {bannerSlides.map((slide, index) => (
          <div
            key={index}
            className={`absolute inset-0 transition-opacity duration-700 ${
              index === currentSlide ? 'opacity-100' : 'opacity-0'
            }`}
          >
            <div
              className="absolute inset-0 bg-cover bg-center"
              style={{ backgroundImage: `url(${slide.image})` }}
            />
            <div className="absolute inset-0 bg-black/50" />
            <div className="relative h-full flex items-center justify-center text-center px-4">
              <div>
                <h1 className="text-4xl md:text-6xl font-bold text-white mb-4">
                  {slide.title}
                </h1>
                <p className="text-lg md:text-xl text-gray-200 mb-8">{slide.subtitle}</p>
                <Link
                  to="/rooms"
                  className="inline-block px-8 py-3 bg-brand-gold text-brand-dark font-semibold rounded-md hover:bg-brand-gold/90 transition-colors"
                >
                  Book Now
                </Link>
              </div>
            </div>
          </div>
        ))}
        <button
          onClick={prevSlide}
          className="absolute left-4 top-1/2 -translate-y-1/2 p-2 bg-white/20 backdrop-blur-sm rounded-full text-white hover:bg-white/30 transition-colors"
        >
          <ChevronLeft size={24} />
        </button>
        <button
          onClick={nextSlide}
          className="absolute right-4 top-1/2 -translate-y-1/2 p-2 bg-white/20 backdrop-blur-sm rounded-full text-white hover:bg-white/30 transition-colors"
        >
          <ChevronRight size={24} />
        </button>
        <div className="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
          {bannerSlides.map((_, i) => (
            <button
              key={i}
              onClick={() => setCurrentSlide(i)}
              className={`w-3 h-3 rounded-full transition-colors ${
                i === currentSlide ? 'bg-brand-gold' : 'bg-white/50'
              }`}
            />
          ))}
        </div>
      </section>

      {/* Booking Search Bar */}
      <section className="bg-brand-primary py-6">
        <div className="max-w-4xl mx-auto px-4">
          <form onSubmit={handleBookingSearch} className="flex flex-col sm:flex-row gap-4 items-end">
            <div className="flex-1 w-full">
              <label className="block text-sm font-medium text-teal-100 mb-1">Arrival</label>
              <input
                type="date"
                value={arrival}
                onChange={(e) => setArrival(e.target.value)}
                min={new Date().toISOString().split('T')[0]}
                className="w-full px-3 py-2 rounded-md border-0 text-gray-900"
              />
            </div>
            <div className="flex-1 w-full">
              <label className="block text-sm font-medium text-teal-100 mb-1">Departure</label>
              <input
                type="date"
                value={departure}
                onChange={(e) => setDeparture(e.target.value)}
                min={arrival || new Date().toISOString().split('T')[0]}
                className="w-full px-3 py-2 rounded-md border-0 text-gray-900"
              />
            </div>
            <button
              type="submit"
              className="w-full sm:w-auto px-8 py-2 bg-brand-gold text-brand-dark font-semibold rounded-md hover:bg-brand-gold/90 transition-colors"
            >
              Check Availability
            </button>
          </form>
        </div>
      </section>

      {/* About Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-brand-ink mb-2">About Us</h2>
              <div className="w-16 h-1 bg-brand-gold mb-6" />
              <p className="text-gray-600 mb-4 leading-relaxed">
                Welcome to StarterHotel, nestled in the vibrant heart of Thamel, Kathmandu. Our hotel
                blends traditional Nepali warmth with modern luxury, offering an unforgettable gateway
                to the Himalayas and Kathmandu Valley&apos;s rich cultural heritage.
              </p>
              <p className="text-gray-600 leading-relaxed">
                From our rooftop terrace with panoramic mountain views to rooms adorned with Newari
                woodwork and local textiles, every detail celebrates Nepal&apos;s beauty. Whether
                you&apos;re trekking to Everest Base Camp or exploring ancient temples, we&apos;re your
                perfect home base.
              </p>
              <Link
                to="/about"
                className="inline-block mt-6 px-6 py-2 border-2 border-brand-gold text-brand-gold font-medium rounded-md hover:bg-brand-gold hover:text-brand-dark transition-colors"
              >
                Read More
              </Link>
            </div>
            <div className="relative">
              <img
                src="https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80"
                alt="About our hotel"
                className="rounded-lg shadow-lg w-full object-cover h-[400px]"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Rooms Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-brand-ink mb-2">Our Rooms</h2>
            <div className="w-16 h-1 bg-brand-gold mx-auto mb-4" />
            <p className="text-gray-600">Choose from our selection of premium rooms</p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {rooms.map((room) => (
              <div
                key={room.id}
                className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow group"
              >
                <div className="relative h-56 overflow-hidden">
                  <img
                    src={getImageUrl(room.image)}
                    alt={room.room_title || 'Room'}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    onError={(e) => { (e.target as HTMLImageElement).src = '/images/room1.jpg'; }}
                  />
                  {room.room_type && (
                    <span className="absolute top-3 left-3 bg-brand-primary text-white text-xs font-semibold px-3 py-1 rounded-full">
                      {room.room_type}
                    </span>
                  )}
                </div>
                <div className="p-5">
                  <h3 className="text-lg font-semibold text-brand-ink mb-1">
                    {room.room_title || `Room #${room.id}`}
                  </h3>
                  <div className="flex items-center gap-1 mb-2">
                    {Array.from({ length: 5 }, (_, i) => (
                      <Star
                        key={i}
                        size={14}
                        className={i < Math.round(room.average_rating) ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'}
                      />
                    ))}
                    <span className="text-xs text-gray-500 ml-1">({room.rating_count})</span>
                  </div>
                  <div className="flex items-center justify-between mt-3">
                    <span className="text-xl font-bold text-brand-primary">
                      ${room.price}<span className="text-sm font-normal text-gray-500">/night</span>
                    </span>
                    <div className="flex items-center gap-1 text-sm text-gray-500">
                      <Wifi size={14} />
                      <span>{room.wifi}</span>
                    </div>
                  </div>
                  <Link
                    to={`/rooms?selected=${room.id}`}
                    className="mt-4 block text-center py-2 bg-brand-primary text-white text-sm font-medium rounded-md hover:bg-brand-primary-dark transition-colors"
                  >
                    Book Now
                  </Link>
                </div>
              </div>
            ))}
          </div>
          <div className="text-center mt-10">
            <Link
              to="/rooms"
              className="inline-block px-8 py-3 border-2 border-brand-primary text-brand-primary font-medium rounded-md hover:bg-brand-primary hover:text-white transition-colors"
            >
              View All Rooms
            </Link>
          </div>
        </div>
      </section>

      {/* Gallery Preview */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-brand-ink mb-2">Our Gallery</h2>
            <div className="w-16 h-1 bg-brand-gold mx-auto mb-4" />
            <p className="text-gray-600">Explore our beautiful spaces</p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=400&q=80',
              'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=400&q=80',
              'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=400&q=80',
              'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=400&q=80',
              'https://images.unsplash.com/photo-1584132967334-10e028bd69f7?w=400&q=80',
              'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400&q=80',
              'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400&q=80',
              'https://images.unsplash.com/photo-1605346434674-a440ca4dc4c0?w=400&q=80',
            ].map((src, i) => (
              <div key={i} className="relative overflow-hidden rounded-lg group aspect-square">
                <img
                  src={src}
                  alt={`Gallery ${i + 1}`}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                />
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/30 transition-colors" />
              </div>
            ))}
          </div>
          <div className="text-center mt-10">
            <Link
              to="/gallery"
              className="inline-block px-8 py-3 border-2 border-brand-primary text-brand-primary font-medium rounded-md hover:bg-brand-primary hover:text-white transition-colors"
            >
              View Full Gallery
            </Link>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-brand-ink mb-2">Contact Us</h2>
            <div className="w-16 h-1 bg-brand-gold mx-auto mb-4" />
          </div>
          <div className="grid md:grid-cols-2 gap-12">
            <form onSubmit={handleContactSubmit} className="space-y-4">
              <input
                type="text"
                placeholder="Your Name"
                required
                value={contactForm.name}
                onChange={(e) => setContactForm({ ...contactForm, name: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-primary focus:border-transparent"
              />
              <input
                type="email"
                placeholder="Your Email"
                required
                value={contactForm.email}
                onChange={(e) => setContactForm({ ...contactForm, email: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-primary focus:border-transparent"
              />
              <input
                type="tel"
                placeholder="Phone Number"
                required
                value={contactForm.phone}
                onChange={(e) => setContactForm({ ...contactForm, phone: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-primary focus:border-transparent"
              />
              <textarea
                rows={4}
                placeholder="Your Message"
                required
                value={contactForm.message}
                onChange={(e) => setContactForm({ ...contactForm, message: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-primary focus:border-transparent"
              />
              <button
                type="submit"
                className="px-8 py-3 bg-brand-primary text-white font-semibold rounded-md hover:bg-brand-primary-dark transition-colors"
              >
                Send Message
              </button>
            </form>
            <div className="space-y-6">
              <div className="flex items-start gap-4">
                <div className="p-3 bg-brand-primary/10 rounded-lg">
                  <MapPin className="text-brand-primary" size={22} />
                </div>
                <div>
                  <h4 className="font-semibold text-brand-ink">Address</h4>
                  <p className="text-gray-600 text-sm">Thamel, Kathmandu 44600, Nepal</p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <div className="p-3 bg-brand-primary/10 rounded-lg">
                  <Phone className="text-brand-primary" size={22} />
                </div>
                <div>
                  <h4 className="font-semibold text-brand-ink">Phone</h4>
                  <p className="text-gray-600 text-sm">+977 1-4700123</p>
                </div>
              </div>
              <div className="flex items-start gap-4">
                <div className="p-3 bg-brand-primary/10 rounded-lg">
                  <Mail className="text-brand-primary" size={22} />
                </div>
                <div>
                  <h4 className="font-semibold text-brand-ink">Email</h4>
                  <p className="text-gray-600 text-sm">info@starterhotel.com.np</p>
                </div>
              </div>
              <div className="rounded-lg overflow-hidden h-48">
                <iframe
                  title="Location"
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3532.2!2d85.3103!3d27.7153!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39eb18fcb77fd4bd%3A0x58099b1deffed8d4!2sThamel%2C%20Kathmandu%2044600!5e0!3m2!1sen!2snp!4v1"
                  width="100%"
                  height="100%"
                  style={{ border: 0 }}
                  allowFullScreen
                  loading="lazy"
                />
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
