import { useState } from 'react';
import { MapPin, Phone, Mail, Clock } from 'lucide-react';
import { submitContact } from '../../api/contacts';
import toast from 'react-hot-toast';

export default function ContactPage() {
  const [form, setForm] = useState({ name: '', email: '', phone: '', message: '' });
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await submitContact(form);
      toast.success('Message sent successfully!');
      setForm({ name: '', email: '', phone: '', message: '' });
    } catch {
      toast.error('Failed to send message. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div>
      {/* Header */}
      <section className="bg-brand-dark py-16 text-center">
        <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">Contact Us</h1>
        <p className="text-gray-300">Get in touch with us for any inquiries</p>
      </section>

      {/* Contact Content */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12">
            {/* Form */}
            <div>
              <h2 className="text-2xl font-bold text-brand-ink mb-6">Send us a Message</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Name</label>
                  <input
                    type="text"
                    required
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-primary focus:border-transparent"
                    placeholder="Your name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    type="email"
                    required
                    value={form.email}
                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-primary focus:border-transparent"
                    placeholder="Your email"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                  <input
                    type="tel"
                    required
                    value={form.phone}
                    onChange={(e) => setForm({ ...form, phone: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-primary focus:border-transparent"
                    placeholder="Your phone number"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Message</label>
                  <textarea
                    required
                    rows={5}
                    value={form.message}
                    onChange={(e) => setForm({ ...form, message: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-brand-primary focus:border-transparent"
                    placeholder="Your message"
                  />
                </div>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-8 py-3 bg-brand-primary text-white font-semibold rounded-md hover:bg-brand-primary-dark transition-colors disabled:opacity-50"
                >
                  {submitting ? 'Sending...' : 'Send Message'}
                </button>
              </form>
            </div>

            {/* Info */}
            <div>
              <h2 className="text-2xl font-bold text-brand-ink mb-6">Contact Information</h2>
              <div className="space-y-6">
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-brand-primary/10 rounded-lg flex-shrink-0">
                    <MapPin className="text-brand-primary" size={22} />
                  </div>
                  <div>
                    <h4 className="font-semibold text-brand-ink">Address</h4>
                    <p className="text-gray-600 text-sm mt-1">
                      Location of Hotel, City, Country
                    </p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-brand-primary/10 rounded-lg flex-shrink-0">
                    <Phone className="text-brand-primary" size={22} />
                  </div>
                  <div>
                    <h4 className="font-semibold text-brand-ink">Phone</h4>
                    <p className="text-gray-600 text-sm mt-1">+12 1234567890</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-brand-primary/10 rounded-lg flex-shrink-0">
                    <Mail className="text-brand-primary" size={22} />
                  </div>
                  <div>
                    <h4 className="font-semibold text-brand-ink">Email</h4>
                    <p className="text-gray-600 text-sm mt-1">demo@gmail.com</p>
                  </div>
                </div>
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-brand-primary/10 rounded-lg flex-shrink-0">
                    <Clock className="text-brand-primary" size={22} />
                  </div>
                  <div>
                    <h4 className="font-semibold text-brand-ink">Working Hours</h4>
                    <p className="text-gray-600 text-sm mt-1">Mon - Fri: 9:00 AM - 6:00 PM</p>
                    <p className="text-gray-600 text-sm">Sat - Sun: 10:00 AM - 4:00 PM</p>
                  </div>
                </div>
              </div>

              {/* Map */}
              <div className="mt-8 rounded-lg overflow-hidden shadow-sm">
                <iframe
                  title="Location"
                  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d387190.2799140298!2d-74.25987584510595!3d40.697670063847!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c24fa5d33f083b%3A0xc80b8f06e177fe62!2sNew%20York%2C%20NY!5e0!3m2!1sen!2sus!4v1"
                  width="100%"
                  height="300"
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
