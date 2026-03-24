import { useState, useEffect } from 'react';
import {
  Users, BedDouble, CalendarCheck, DollarSign,
  Plus, Pencil, Trash2, Image, X, Save, RefreshCw,
} from 'lucide-react';
import {
  fetchAdminStats, fetchAdminRooms, createAdminRoom, updateAdminRoom, deleteAdminRoom,
  fetchAdminBookings, updateBookingStatus, deleteAdminBooking,
  fetchAdminContacts, fetchAdminUsers, deleteAdminUser,
  fetchAdminGallery, createAdminGallery, deleteAdminGallery,
} from '../../api/admin';
import { getImageUrl } from '../../api/client';
import type { AdminStats, Room, Booking, GalleryItem, User, Contact } from '../../types';
import toast from 'react-hot-toast';
import {
  Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

type Tab = 'rooms' | 'bookings' | 'gallery' | 'users' | 'contacts';

export default function DashboardPage() {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>('rooms');
  const [rooms, setRooms] = useState<Room[]>([]);
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [gallery, setGallery] = useState<GalleryItem[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [loading, setLoading] = useState(true);

  // Room form
  const [showRoomForm, setShowRoomForm] = useState(false);
  const [editingRoom, setEditingRoom] = useState<Room | null>(null);
  const [roomForm, setRoomForm] = useState({
    room_title: '', description: '', price: '', wifi: 'yes', room_type: '', image_url: '',
  });
  const [roomImageFile, setRoomImageFile] = useState<File | null>(null);

  // Gallery form
  const [galleryUrl, setGalleryUrl] = useState('');
  const [galleryFile, setGalleryFile] = useState<File | null>(null);

  useEffect(() => {
    loadStats();
    loadTabData('rooms');
  }, []);

  const loadStats = async () => {
    try {
      const data = await fetchAdminStats();
      setStats(data);
    } catch {
      toast.error('Failed to load stats');
    } finally {
      setLoading(false);
    }
  };

  const loadTabData = async (tab: Tab) => {
    try {
      switch (tab) {
        case 'rooms': {
          const res = await fetchAdminRooms();
          setRooms(res.rooms);
          break;
        }
        case 'bookings': {
          const res = await fetchAdminBookings();
          setBookings(res.bookings);
          break;
        }
        case 'gallery': {
          const res = await fetchAdminGallery();
          setGallery(res.gallery);
          break;
        }
        case 'users': {
          const res = await fetchAdminUsers();
          setUsers(res.users);
          break;
        }
        case 'contacts': {
          const res = await fetchAdminContacts();
          setContacts(res.contacts);
          break;
        }
      }
    } catch {
      toast.error(`Failed to load ${tab}`);
    }
  };

  const switchTab = (tab: Tab) => {
    setActiveTab(tab);
    loadTabData(tab);
  };

  // Room CRUD
  const openRoomForm = (room?: Room) => {
    if (room) {
      setEditingRoom(room);
      setRoomForm({
        room_title: room.room_title || '',
        description: room.description || '',
        price: room.price || '',
        wifi: room.wifi || 'yes',
        room_type: room.room_type || '',
        image_url: room.image_raw || '',
      });
    } else {
      setEditingRoom(null);
      setRoomForm({ room_title: '', description: '', price: '', wifi: 'yes', room_type: '', image_url: '' });
    }
    setRoomImageFile(null);
    setShowRoomForm(true);
  };

  const handleRoomSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('room_title', roomForm.room_title);
    formData.append('description', roomForm.description);
    formData.append('price', roomForm.price);
    formData.append('wifi', roomForm.wifi);
    formData.append('room_type', roomForm.room_type);
    if (roomImageFile) {
      formData.append('image_file', roomImageFile);
    } else if (roomForm.image_url) {
      formData.append('image_url', roomForm.image_url);
    }

    try {
      if (editingRoom) {
        await updateAdminRoom(editingRoom.id, formData);
        toast.success('Room updated');
      } else {
        await createAdminRoom(formData);
        toast.success('Room created');
      }
      setShowRoomForm(false);
      loadTabData('rooms');
      loadStats();
    } catch {
      toast.error('Failed to save room');
    }
  };

  const handleDeleteRoom = async (id: number) => {
    if (!confirm('Delete this room?')) return;
    try {
      await deleteAdminRoom(id);
      toast.success('Room deleted');
      loadTabData('rooms');
      loadStats();
    } catch {
      toast.error('Failed to delete room');
    }
  };

  // Booking status
  const handleStatusChange = async (bookingId: number, newStatus: string) => {
    try {
      await updateBookingStatus(bookingId, newStatus);
      toast.success('Status updated');
      loadTabData('bookings');
      loadStats();
    } catch {
      toast.error('Failed to update status');
    }
  };

  const handleDeleteBooking = async (id: number) => {
    if (!confirm('Delete this booking?')) return;
    try {
      await deleteAdminBooking(id);
      toast.success('Booking deleted');
      loadTabData('bookings');
      loadStats();
    } catch {
      toast.error('Failed to delete booking');
    }
  };

  // Gallery
  const handleGallerySubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData();
    if (galleryFile) {
      formData.append('image_file', galleryFile);
    } else if (galleryUrl) {
      formData.append('image_url', galleryUrl);
    } else {
      toast.error('Provide an image URL or file');
      return;
    }
    try {
      await createAdminGallery(formData);
      toast.success('Image added');
      setGalleryUrl('');
      setGalleryFile(null);
      loadTabData('gallery');
    } catch {
      toast.error('Failed to add image');
    }
  };

  const handleDeleteGallery = async (id: number) => {
    if (!confirm('Delete this image?')) return;
    try {
      await deleteAdminGallery(id);
      toast.success('Image deleted');
      loadTabData('gallery');
    } catch {
      toast.error('Failed to delete image');
    }
  };

  // Users
  const handleDeleteUser = async (id: number) => {
    if (!confirm('Delete this user?')) return;
    try {
      await deleteAdminUser(id);
      toast.success('User deleted');
      loadTabData('users');
      loadStats();
    } catch {
      toast.error('Failed to delete user');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-brand-primary" />
      </div>
    );
  }

  const statCards = stats
    ? [
        { label: 'Total Users', value: stats.total_users, icon: Users, color: 'bg-blue-500' },
        { label: 'Total Rooms', value: stats.total_rooms, icon: BedDouble, color: 'bg-green-500' },
        { label: 'Total Bookings', value: stats.total_bookings, icon: CalendarCheck, color: 'bg-amber-500' },
        { label: 'Total Income', value: `$${stats.total_income.toLocaleString()}`, icon: DollarSign, color: 'bg-purple-500' },
      ]
    : [];

  const tabs: { key: Tab; label: string }[] = [
    { key: 'rooms', label: 'Rooms' },
    { key: 'bookings', label: 'Bookings' },
    { key: 'gallery', label: 'Gallery' },
    { key: 'users', label: 'Users' },
    { key: 'contacts', label: 'Messages' },
  ];

  return (
    <div className="space-y-8">
      {/* Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {statCards.map((card) => (
          <div key={card.label} className="bg-white rounded-lg shadow-sm p-5 flex items-center gap-4">
            <div className={`p-3 rounded-lg ${card.color}`}>
              <card.icon size={22} className="text-white" />
            </div>
            <div>
              <p className="text-2xl font-bold text-brand-ink">{card.value}</p>
              <p className="text-sm text-gray-500">{card.label}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Chart */}
      {stats && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h3 className="text-lg font-semibold text-brand-ink mb-4">Bookings by Month</h3>
          <div className="h-64">
            <Bar
              data={{
                labels: stats.bookings_by_month.labels,
                datasets: [
                  {
                    label: 'Bookings',
                    data: stats.bookings_by_month.data,
                    backgroundColor: 'rgba(15, 118, 110, 0.7)',
                    borderRadius: 4,
                  },
                ],
              }}
              options={{
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true, ticks: { precision: 0 } } },
              }}
            />
          </div>
        </div>
      )}

      {/* Status Summary */}
      {stats && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {Object.entries(stats.status_counts).map(([key, value]) => (
            <div key={key} className="bg-white rounded-lg shadow-sm p-4 text-center">
              <p className="text-lg font-bold text-brand-ink">{value}</p>
              <p className="text-sm text-gray-500 capitalize">{key}</p>
            </div>
          ))}
        </div>
      )}

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm">
        <div className="border-b border-gray-200 flex overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.key}
              onClick={() => switchTab(tab.key)}
              className={`px-6 py-3 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${
                activeTab === tab.key
                  ? 'border-brand-primary text-brand-primary'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              {tab.label}
            </button>
          ))}
          <button
            onClick={() => loadTabData(activeTab)}
            className="ml-auto px-4 py-3 text-gray-400 hover:text-gray-600"
            title="Refresh"
          >
            <RefreshCw size={16} />
          </button>
        </div>

        <div className="p-6">
          {/* ROOMS TAB */}
          {activeTab === 'rooms' && (
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold">Room Management</h3>
                <button
                  onClick={() => openRoomForm()}
                  className="flex items-center gap-1 px-4 py-2 bg-brand-primary text-white text-sm font-medium rounded-md hover:bg-brand-primary-dark"
                >
                  <Plus size={16} /> Add Room
                </button>
              </div>

              {/* Room Form Modal */}
              {showRoomForm && (
                <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
                  <div className="bg-white rounded-lg shadow-xl max-w-lg w-full p-6 max-h-[90vh] overflow-y-auto">
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="text-lg font-semibold">
                        {editingRoom ? 'Edit Room' : 'Add New Room'}
                      </h4>
                      <button onClick={() => setShowRoomForm(false)}>
                        <X size={20} className="text-gray-400 hover:text-gray-600" />
                      </button>
                    </div>
                    <form onSubmit={handleRoomSubmit} className="space-y-4">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Title</label>
                        <input
                          type="text"
                          value={roomForm.room_title}
                          onChange={(e) => setRoomForm({ ...roomForm, room_title: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                        <textarea
                          rows={3}
                          value={roomForm.description}
                          onChange={(e) => setRoomForm({ ...roomForm, description: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                        />
                      </div>
                      <div className="grid grid-cols-2 gap-3">
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Price ($/night)</label>
                          <input
                            type="text"
                            value={roomForm.price}
                            onChange={(e) => setRoomForm({ ...roomForm, price: e.target.value })}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium text-gray-700 mb-1">Room Type</label>
                          <input
                            type="text"
                            value={roomForm.room_type}
                            onChange={(e) => setRoomForm({ ...roomForm, room_type: e.target.value })}
                            placeholder="e.g. Deluxe, Standard"
                            className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                          />
                        </div>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">WiFi</label>
                        <select
                          value={roomForm.wifi}
                          onChange={(e) => setRoomForm({ ...roomForm, wifi: e.target.value })}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                        >
                          <option value="yes">Yes</option>
                          <option value="no">No</option>
                        </select>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Image URL</label>
                        <input
                          type="text"
                          value={roomForm.image_url}
                          onChange={(e) => setRoomForm({ ...roomForm, image_url: e.target.value })}
                          placeholder="https://..."
                          className="w-full px-3 py-2 border border-gray-300 rounded-md text-sm"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Or Upload Image</label>
                        <input
                          type="file"
                          accept="image/*"
                          onChange={(e) => setRoomImageFile(e.target.files?.[0] || null)}
                          className="w-full text-sm"
                        />
                      </div>
                      <button
                        type="submit"
                        className="w-full py-2 bg-brand-primary text-white font-medium rounded-md hover:bg-brand-primary-dark flex items-center justify-center gap-2"
                      >
                        <Save size={16} />
                        {editingRoom ? 'Update Room' : 'Create Room'}
                      </button>
                    </form>
                  </div>
                </div>
              )}

              {/* Room Table */}
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Room</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Type</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Price</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">WiFi</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Rating</th>
                      <th className="text-right px-4 py-3 font-medium text-gray-600">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {rooms.map((room) => (
                      <tr key={room.id} className="hover:bg-gray-50">
                        <td className="px-4 py-3">
                          <div className="flex items-center gap-3">
                            <img
                              src={getImageUrl(room.image)}
                              alt={room.room_title || ''}
                              className="w-12 h-12 rounded object-cover"
                              onError={(e) => { (e.target as HTMLImageElement).src = '/images/room/room1.jpg'; }}
                            />
                            <span className="font-medium">{room.room_title || `#${room.id}`}</span>
                          </div>
                        </td>
                        <td className="px-4 py-3 text-gray-600">{room.room_type || '-'}</td>
                        <td className="px-4 py-3 font-medium">${room.price}</td>
                        <td className="px-4 py-3 text-gray-600">{room.wifi}</td>
                        <td className="px-4 py-3 text-gray-600">{room.average_rating.toFixed(1)}</td>
                        <td className="px-4 py-3">
                          <div className="flex items-center justify-end gap-2">
                            <button
                              onClick={() => openRoomForm(room)}
                              className="p-1.5 text-blue-600 hover:bg-blue-50 rounded"
                            >
                              <Pencil size={14} />
                            </button>
                            <button
                              onClick={() => handleDeleteRoom(room.id)}
                              className="p-1.5 text-red-600 hover:bg-red-50 rounded"
                            >
                              <Trash2 size={14} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {rooms.length === 0 && (
                  <p className="text-center py-8 text-gray-500">No rooms found</p>
                )}
              </div>
            </div>
          )}

          {/* BOOKINGS TAB */}
          {activeTab === 'bookings' && (
            <div>
              <h3 className="text-lg font-semibold mb-4">Booking Management</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">ID</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Room</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Guest</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Dates</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Total</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Status</th>
                      <th className="text-right px-4 py-3 font-medium text-gray-600">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {bookings.map((booking) => (
                      <tr key={booking.id} className="hover:bg-gray-50">
                        <td className="px-4 py-3 font-medium">#{booking.id}</td>
                        <td className="px-4 py-3 text-gray-600">{booking.room_title || `#${booking.room_id}`}</td>
                        <td className="px-4 py-3">
                          <div>
                            <p className="font-medium">{booking.name}</p>
                            <p className="text-xs text-gray-500">{booking.email}</p>
                          </div>
                        </td>
                        <td className="px-4 py-3 text-gray-600 text-xs">
                          {booking.start_date} → {booking.end_date}
                        </td>
                        <td className="px-4 py-3 font-medium">
                          {booking.total_price != null ? `$${booking.total_price}` : '-'}
                        </td>
                        <td className="px-4 py-3">
                          <select
                            value={booking.status}
                            onChange={(e) => handleStatusChange(booking.id, e.target.value)}
                            className={`text-xs px-2 py-1 rounded-full border-0 font-medium ${
                              booking.status === 'approved' || booking.status === 'paid'
                                ? 'bg-green-100 text-green-700'
                                : booking.status === 'rejected' || booking.status === 'canceled'
                                ? 'bg-red-100 text-red-700'
                                : 'bg-yellow-100 text-yellow-700'
                            }`}
                          >
                            {['waiting', 'approved', 'rejected', 'canceled', 'paid'].map((s) => (
                              <option key={s} value={s}>{s}</option>
                            ))}
                          </select>
                        </td>
                        <td className="px-4 py-3">
                          <div className="flex justify-end">
                            <button
                              onClick={() => handleDeleteBooking(booking.id)}
                              className="p-1.5 text-red-600 hover:bg-red-50 rounded"
                            >
                              <Trash2 size={14} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {bookings.length === 0 && (
                  <p className="text-center py-8 text-gray-500">No bookings found</p>
                )}
              </div>
            </div>
          )}

          {/* GALLERY TAB */}
          {activeTab === 'gallery' && (
            <div>
              <h3 className="text-lg font-semibold mb-4">Gallery Management</h3>
              <form onSubmit={handleGallerySubmit} className="flex flex-col sm:flex-row gap-3 mb-6">
                <input
                  type="text"
                  value={galleryUrl}
                  onChange={(e) => setGalleryUrl(e.target.value)}
                  placeholder="Image URL"
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm"
                />
                <span className="text-sm text-gray-500 self-center">or</span>
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => setGalleryFile(e.target.files?.[0] || null)}
                  className="text-sm"
                />
                <button
                  type="submit"
                  className="flex items-center gap-1 px-4 py-2 bg-brand-primary text-white text-sm font-medium rounded-md hover:bg-brand-primary-dark"
                >
                  <Image size={16} /> Add
                </button>
              </form>
              <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
                {gallery.map((item) => (
                  <div key={item.id} className="relative group rounded-lg overflow-hidden">
                    <img
                      src={getImageUrl(item.image)}
                      alt={`Gallery ${item.id}`}
                      className="w-full aspect-square object-cover"
                      onError={(e) => { (e.target as HTMLImageElement).src = '/images/room/room1.jpg'; }}
                    />
                    <button
                      onClick={() => handleDeleteGallery(item.id)}
                      className="absolute top-2 right-2 p-1.5 bg-red-600 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <Trash2 size={14} />
                    </button>
                  </div>
                ))}
              </div>
              {gallery.length === 0 && (
                <p className="text-center py-8 text-gray-500">No gallery images</p>
              )}
            </div>
          )}

          {/* USERS TAB */}
          {activeTab === 'users' && (
            <div>
              <h3 className="text-lg font-semibold mb-4">User Management</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">ID</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Name</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Email</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Phone</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Role</th>
                      <th className="text-right px-4 py-3 font-medium text-gray-600">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {users.map((user) => (
                      <tr key={user.id} className="hover:bg-gray-50">
                        <td className="px-4 py-3 font-medium">#{user.id}</td>
                        <td className="px-4 py-3">{user.name}</td>
                        <td className="px-4 py-3 text-gray-600">{user.email}</td>
                        <td className="px-4 py-3 text-gray-600">{user.phone || '-'}</td>
                        <td className="px-4 py-3">
                          <span
                            className={`inline-block text-xs px-2 py-0.5 rounded-full font-medium ${
                              user.usertype === 'admin'
                                ? 'bg-purple-100 text-purple-700'
                                : 'bg-gray-100 text-gray-700'
                            }`}
                          >
                            {user.usertype}
                          </span>
                        </td>
                        <td className="px-4 py-3">
                          <div className="flex justify-end">
                            <button
                              onClick={() => handleDeleteUser(user.id)}
                              className="p-1.5 text-red-600 hover:bg-red-50 rounded"
                            >
                              <Trash2 size={14} />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {users.length === 0 && (
                  <p className="text-center py-8 text-gray-500">No users found</p>
                )}
              </div>
            </div>
          )}

          {/* CONTACTS TAB */}
          {activeTab === 'contacts' && (
            <div>
              <h3 className="text-lg font-semibold mb-4">Contact Messages</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Name</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Email</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Phone</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Message</th>
                      <th className="text-left px-4 py-3 font-medium text-gray-600">Date</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {contacts.map((contact) => (
                      <tr key={contact.id} className="hover:bg-gray-50">
                        <td className="px-4 py-3 font-medium">{contact.name}</td>
                        <td className="px-4 py-3 text-gray-600">{contact.email}</td>
                        <td className="px-4 py-3 text-gray-600">{contact.phone}</td>
                        <td className="px-4 py-3 text-gray-600 max-w-xs truncate">{contact.message}</td>
                        <td className="px-4 py-3 text-gray-600 text-xs">
                          {new Date(contact.created_at).toLocaleDateString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
                {contacts.length === 0 && (
                  <p className="text-center py-8 text-gray-500">No messages found</p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
