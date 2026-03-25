import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Wifi, Star, Calendar, User, Mail, Phone, AlertCircle } from 'lucide-react';
import { fetchRooms, fetchRecommendations } from '../../api/rooms';
import { createBooking } from '../../api/bookings';
import { submitRating } from '../../api/ratings';
import { getImageUrl } from '../../api/client';
import type { Room, AlternativeSlot } from '../../types';
import toast from 'react-hot-toast';
import axios from 'axios';

export default function RoomsPage() {
  const [searchParams] = useSearchParams();
  const [rooms, setRooms] = useState<Room[]>([]);
  const [recommendations, setRecommendations] = useState<Room[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedRoom, setSelectedRoom] = useState<Room | null>(null);
  const [alternatives, setAlternatives] = useState<AlternativeSlot[]>([]);

  // Booking form
  const [bookingForm, setBookingForm] = useState({
    name: '',
    email: '',
    phone: '',
    arrival: searchParams.get('arrival') || '',
    departure: searchParams.get('departure') || '',
  });

  // Rating form
  const [showRatingForm, setShowRatingForm] = useState<number | null>(null);
  const [ratingForm, setRatingForm] = useState({
    name: '',
    email: '',
    comment: '',
    rating: 5,
  });

  useEffect(() => {
    loadRooms();
  }, []);

  useEffect(() => {
    if (bookingForm.arrival && bookingForm.departure) {
      loadRecommendations();
    }
  }, [bookingForm.arrival, bookingForm.departure]);

  // Pre-select room from URL
  useEffect(() => {
    const selectedId = searchParams.get('selected');
    if (selectedId && rooms.length > 0) {
      const room = rooms.find((r) => r.id === Number(selectedId));
      if (room) setSelectedRoom(room);
    }
  }, [rooms, searchParams]);

  const loadRooms = async () => {
    try {
      const res = await fetchRooms();
      setRooms(res.rooms);
    } catch {
      toast.error('Failed to load rooms');
    } finally {
      setLoading(false);
    }
  };

  const loadRecommendations = async () => {
    try {
      const res = await fetchRecommendations({
        start_date: bookingForm.arrival,
        end_date: bookingForm.departure,
      });
      setRecommendations(res.recommendations);
    } catch {
      setRecommendations([]);
    }
  };

  const calculateTotal = () => {
    if (!selectedRoom?.price || !bookingForm.arrival || !bookingForm.departure) return null;
    const start = new Date(bookingForm.arrival);
    const end = new Date(bookingForm.departure);
    const nights = Math.max(1, Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24)));
    return { nights, total: nights * parseFloat(selectedRoom.price) };
  };

  const handleBooking = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedRoom) return;

    const calc = calculateTotal();
    if (!calc) {
      toast.error('Please select dates');
      return;
    }

    try {
      const result = await createBooking({
        room_id: selectedRoom.id,
        start_date: bookingForm.arrival,
        end_date: bookingForm.departure,
        name: bookingForm.name,
        email: bookingForm.email,
        phone: bookingForm.phone,
        total_price: calc.total,
      });
      if (result.email_confirmation_sent) {
        toast.success('Room booked! Confirmation email sent to ' + bookingForm.email, { duration: 5000 });
      } else {
        toast.success('Room booked successfully!');
      }
      setSelectedRoom(null);
      setAlternatives([]);
      setBookingForm((prev) => ({ ...prev, name: '', email: '', phone: '' }));
    } catch (err) {
      if (axios.isAxiosError(err) && err.response?.status === 409) {
        const detail = err.response.data?.detail;
        if (detail?.alternative_slots) {
          setAlternatives(detail.alternative_slots);
          toast.error('Room is booked for those dates. See alternatives below.');
        } else {
          toast.error(typeof detail === 'string' ? detail : 'Room unavailable for selected dates');
        }
      } else {
        toast.error('Failed to book room');
      }
    }
  };

  const handleRating = async (e: React.FormEvent, roomId: number) => {
    e.preventDefault();
    try {
      const res = await submitRating(roomId, ratingForm);
      if (res.status === 'duplicate') {
        toast.error('You already rated this room');
      } else {
        toast.success('Thanks for your rating!');
        setShowRatingForm(null);
        setRatingForm({ name: '', email: '', comment: '', rating: 5 });
        loadRooms();
      }
    } catch {
      toast.error('Failed to submit rating');
    }
  };

  const applySlot = (slot: AlternativeSlot) => {
    setBookingForm((prev) => ({
      ...prev,
      arrival: slot.start_date,
      departure: slot.end_date,
    }));
    setAlternatives([]);
  };

  const priceInfo = calculateTotal();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-primary" />
      </div>
    );
  }

  return (
    <div className="bg-gray-50 min-h-screen">
      {/* Header */}
      <section className="bg-brand-dark py-16 text-center">
        <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">Our Rooms</h1>
        <p className="text-gray-300">Find and book your perfect room</p>
      </section>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Room List */}
          <div className="lg:col-span-2 space-y-6">
            {/* Recommendations */}
            {recommendations.length > 0 && (
              <div className="bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 rounded-lg p-5">
                <div className="flex items-center justify-between mb-1">
                  <h3 className="text-lg font-semibold text-amber-800 flex items-center gap-2">
                    <Star size={18} className="fill-amber-400 text-amber-400" />
                    AI Recommended for Your Dates
                  </h3>
                  <span className="text-xs bg-amber-200/60 text-amber-700 px-2 py-0.5 rounded-full font-medium">
                    Weighted Multi-Factor Algorithm
                  </span>
                </div>
                <p className="text-xs text-amber-600 mb-4">
                  Rooms ranked by rating (42%), price fit (28%), type match (20%), and amenities (10%)
                </p>
                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {recommendations.map((room, idx) => (
                    <button
                      key={room.id}
                      onClick={() => { setSelectedRoom(room); setAlternatives([]); }}
                      className={`text-left p-4 rounded-lg border-2 transition-all ${
                        selectedRoom?.id === room.id
                          ? 'border-brand-primary bg-brand-primary/5 shadow-md'
                          : 'border-gray-200 hover:border-brand-primary/50 bg-white hover:shadow-sm'
                      }`}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-xs font-bold text-amber-600">#{idx + 1} Pick</span>
                        {room.recommendation_score != null && (
                          <span className="text-xs font-bold text-brand-primary">
                            {(room.recommendation_score * 100).toFixed(0)}% match
                          </span>
                        )}
                      </div>
                      <p className="text-sm font-semibold truncate">{room.room_title}</p>
                      <div className="flex items-center justify-between mt-1">
                        <p className="text-xs text-gray-500">${room.price}/night</p>
                        <div className="flex items-center gap-0.5">
                          {Array.from({ length: 5 }, (_, i) => (
                            <Star key={i} size={10} className={i < Math.round(room.average_rating) ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'} />
                          ))}
                        </div>
                      </div>
                      {room.recommendation_score != null && (
                        <div className="mt-2 h-1.5 bg-gray-200 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-gradient-to-r from-brand-gold to-amber-400 rounded-full transition-all"
                            style={{ width: `${room.recommendation_score * 100}%` }}
                          />
                        </div>
                      )}
                      {room.recommendation_reasons && (
                        <div className="mt-2 flex flex-wrap gap-1">
                          {room.recommendation_reasons.map((reason, i) => (
                            <span key={i} className="text-[10px] bg-gray-100 text-gray-500 px-1.5 py-0.5 rounded">
                              {reason}
                            </span>
                          ))}
                        </div>
                      )}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* All Rooms */}
            <div className="space-y-4">
              {rooms.map((room) => (
                <div
                  key={room.id}
                  className={`bg-white rounded-lg shadow-sm overflow-hidden border-2 transition-colors ${
                    selectedRoom?.id === room.id
                      ? 'border-brand-primary'
                      : 'border-transparent hover:border-gray-200'
                  }`}
                >
                  <div className="flex flex-col sm:flex-row">
                    <div className="sm:w-64 h-48 sm:h-auto flex-shrink-0">
                      <img
                        src={getImageUrl(room.image)}
                        alt={room.room_title || 'Room'}
                        className="w-full h-full object-cover"
                        onError={(e) => { (e.target as HTMLImageElement).src = '/images/room1.jpg'; }}
                      />
                    </div>
                    <div className="flex-1 p-5">
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="text-lg font-semibold text-brand-ink">
                            {room.room_title || `Room #${room.id}`}
                          </h3>
                          {room.room_type && (
                            <span className="inline-block mt-1 text-xs bg-brand-primary/10 text-brand-primary px-2 py-0.5 rounded-full">
                              {room.room_type}
                            </span>
                          )}
                        </div>
                        <span className="text-xl font-bold text-brand-primary">
                          ${room.price}
                          <span className="text-xs font-normal text-gray-500">/night</span>
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mt-2 line-clamp-2">
                        {room.description || 'A comfortable room with all amenities.'}
                      </p>
                      <div className="flex items-center gap-4 mt-3">
                        <div className="flex items-center gap-1">
                          {Array.from({ length: 5 }, (_, i) => (
                            <Star
                              key={i}
                              size={12}
                              className={i < Math.round(room.average_rating) ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'}
                            />
                          ))}
                          <span className="text-xs text-gray-500 ml-1">
                            {room.average_rating.toFixed(1)} ({room.rating_count})
                          </span>
                        </div>
                        <div className="flex items-center gap-1 text-xs text-gray-500">
                          <Wifi size={12} />
                          WiFi: {room.wifi}
                        </div>
                      </div>
                      <div className="flex gap-2 mt-4">
                        <button
                          onClick={() => { setSelectedRoom(room); setAlternatives([]); }}
                          className="px-4 py-2 bg-brand-primary text-white text-sm font-medium rounded-md hover:bg-brand-primary-dark transition-colors"
                        >
                          {selectedRoom?.id === room.id ? 'Selected' : 'Select Room'}
                        </button>
                        <button
                          onClick={() => setShowRatingForm(showRatingForm === room.id ? null : room.id)}
                          className="px-4 py-2 border border-gray-300 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-50 transition-colors"
                        >
                          Rate
                        </button>
                      </div>

                      {/* Rating Form */}
                      {showRatingForm === room.id && (
                        <form
                          onSubmit={(e) => handleRating(e, room.id)}
                          className="mt-4 p-4 bg-gray-50 rounded-lg space-y-3"
                        >
                          <div className="grid grid-cols-2 gap-3">
                            <input
                              type="text"
                              placeholder="Name"
                              required
                              value={ratingForm.name}
                              onChange={(e) => setRatingForm({ ...ratingForm, name: e.target.value })}
                              className="px-3 py-2 text-sm border border-gray-300 rounded-md"
                            />
                            <input
                              type="email"
                              placeholder="Email"
                              required
                              value={ratingForm.email}
                              onChange={(e) => setRatingForm({ ...ratingForm, email: e.target.value })}
                              className="px-3 py-2 text-sm border border-gray-300 rounded-md"
                            />
                          </div>
                          <textarea
                            placeholder="Your review"
                            required
                            rows={2}
                            value={ratingForm.comment}
                            onChange={(e) => setRatingForm({ ...ratingForm, comment: e.target.value })}
                            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md"
                          />
                          <div className="flex items-center gap-2">
                            <span className="text-sm text-gray-600">Rating:</span>
                            <div className="flex gap-1">
                              {[1, 2, 3, 4, 5].map((val) => (
                                <button
                                  key={val}
                                  type="button"
                                  onClick={() => setRatingForm({ ...ratingForm, rating: val })}
                                >
                                  <Star
                                    size={18}
                                    className={val <= ratingForm.rating ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'}
                                  />
                                </button>
                              ))}
                            </div>
                          </div>
                          <button
                            type="submit"
                            className="px-4 py-2 bg-brand-gold text-brand-dark text-sm font-medium rounded-md hover:bg-brand-gold/90"
                          >
                            Submit Rating
                          </button>
                        </form>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Booking Sidebar */}
          <div className="lg:col-span-1">
            <div className="sticky top-24 bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-bold text-brand-ink mb-5">Book a Room</h2>
              <form onSubmit={handleBooking} className="space-y-4">
                {selectedRoom && (
                  <div className="p-3 bg-brand-primary/5 rounded-lg border border-brand-primary/20">
                    <p className="text-sm font-semibold text-brand-primary">
                      {selectedRoom.room_title || `Room #${selectedRoom.id}`}
                    </p>
                    <p className="text-xs text-gray-500">${selectedRoom.price}/night</p>
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    <User size={14} className="inline mr-1" /> Full Name
                  </label>
                  <input
                    type="text"
                    required
                    value={bookingForm.name}
                    onChange={(e) => setBookingForm({ ...bookingForm, name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-brand-primary focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    <Mail size={14} className="inline mr-1" /> Email
                  </label>
                  <input
                    type="email"
                    required
                    value={bookingForm.email}
                    onChange={(e) => setBookingForm({ ...bookingForm, email: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-brand-primary focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    <Phone size={14} className="inline mr-1" /> Phone
                  </label>
                  <input
                    type="tel"
                    required
                    value={bookingForm.phone}
                    onChange={(e) => setBookingForm({ ...bookingForm, phone: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-brand-primary focus:border-transparent"
                  />
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      <Calendar size={14} className="inline mr-1" /> Arrival
                    </label>
                    <input
                      type="date"
                      required
                      min={new Date().toISOString().split('T')[0]}
                      value={bookingForm.arrival}
                      onChange={(e) => setBookingForm({ ...bookingForm, arrival: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-brand-primary focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      <Calendar size={14} className="inline mr-1" /> Departure
                    </label>
                    <input
                      type="date"
                      required
                      min={bookingForm.arrival || new Date().toISOString().split('T')[0]}
                      value={bookingForm.departure}
                      onChange={(e) => setBookingForm({ ...bookingForm, departure: e.target.value })}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-brand-primary focus:border-transparent"
                    />
                  </div>
                </div>

                {/* Price Summary */}
                {priceInfo && (
                  <div className="p-3 bg-gray-50 rounded-lg">
                    <div className="flex justify-between text-sm text-gray-600">
                      <span>{priceInfo.nights} night(s)</span>
                      <span>${selectedRoom?.price} x {priceInfo.nights}</span>
                    </div>
                    <div className="flex justify-between text-lg font-bold text-brand-ink mt-1">
                      <span>Total</span>
                      <span>${priceInfo.total.toFixed(2)}</span>
                    </div>
                  </div>
                )}

                {/* Alternative Slots — Merged-Interval Gap-Scan Algorithm */}
                {alternatives.length > 0 && (
                  <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                    <p className="text-sm font-semibold text-red-700 mb-1 flex items-center gap-1">
                      <AlertCircle size={14} />
                      Room unavailable for selected dates
                    </p>
                    <p className="text-xs text-red-500 mb-3">
                      Our gap-scan algorithm found these nearest available windows:
                    </p>
                    <div className="space-y-2">
                      {alternatives.map((slot, i) => (
                        <button
                          key={i}
                          type="button"
                          onClick={() => applySlot(slot)}
                          className="w-full text-left p-3 bg-white rounded-lg border border-red-200 hover:border-brand-primary hover:shadow-sm text-sm transition-all group"
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <Calendar size={14} className="text-brand-primary" />
                              <span className="font-semibold text-brand-ink">{slot.start_date}</span>
                              <span className="text-gray-400">→</span>
                              <span className="font-semibold text-brand-ink">{slot.end_date}</span>
                            </div>
                            <span className="text-xs bg-brand-primary/10 text-brand-primary px-2 py-0.5 rounded-full font-medium group-hover:bg-brand-primary group-hover:text-white transition-colors">
                              {slot.nights} night{slot.nights !== 1 ? 's' : ''} — Click to book
                            </span>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                <button
                  type="submit"
                  disabled={!selectedRoom}
                  className="w-full py-3 bg-brand-primary text-white font-semibold rounded-md hover:bg-brand-primary-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {selectedRoom ? 'Book Now' : 'Select a Room First'}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
