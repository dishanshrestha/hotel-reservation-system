import client from './client';
import type { AdminStats, Room, RoomsResponse, BookingsResponse, GalleryResponse, GalleryItem, User } from '../types';

// Stats
export const fetchAdminStats = async (): Promise<AdminStats> => {
  const { data } = await client.get<AdminStats>('/api/admin/stats');
  return data;
};

// Rooms
export const fetchAdminRooms = async (): Promise<RoomsResponse> => {
  const { data } = await client.get<RoomsResponse>('/api/admin/rooms');
  return data;
};

export const createAdminRoom = async (formData: FormData): Promise<Room> => {
  const { data } = await client.post<Room>('/api/admin/rooms', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
};

export const updateAdminRoom = async (roomId: number, formData: FormData): Promise<Room> => {
  const { data } = await client.put<Room>(`/api/admin/rooms/${roomId}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
};

export const deleteAdminRoom = async (roomId: number) => {
  const { data } = await client.delete(`/api/admin/rooms/${roomId}`);
  return data;
};

// Bookings
export const fetchAdminBookings = async (): Promise<BookingsResponse> => {
  const { data } = await client.get<BookingsResponse>('/api/admin/bookings');
  return data;
};

export const updateBookingStatus = async (bookingId: number, status: string) => {
  const { data } = await client.patch(`/api/admin/bookings/${bookingId}/status`, { status });
  return data;
};

export const deleteAdminBooking = async (bookingId: number) => {
  const { data } = await client.delete(`/api/admin/bookings/${bookingId}`);
  return data;
};

// Contacts
export const fetchAdminContacts = async () => {
  const { data } = await client.get('/api/admin/contacts');
  return data;
};

// Users
export const fetchAdminUsers = async (): Promise<{ count: number; users: User[] }> => {
  const { data } = await client.get('/api/admin/users');
  return data;
};

export const updateAdminUser = async (userId: number, payload: Partial<User & { password?: string }>) => {
  const { data } = await client.put(`/api/admin/users/${userId}`, payload);
  return data;
};

export const deleteAdminUser = async (userId: number) => {
  const { data } = await client.delete(`/api/admin/users/${userId}`);
  return data;
};

// Gallery
export const fetchAdminGallery = async (): Promise<GalleryResponse> => {
  const { data } = await client.get<GalleryResponse>('/api/admin/gallery');
  return data;
};

export const createAdminGallery = async (formData: FormData): Promise<GalleryItem> => {
  const { data } = await client.post<GalleryItem>('/api/admin/gallery', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
};

export const deleteAdminGallery = async (galleryId: number) => {
  const { data } = await client.delete(`/api/admin/gallery/${galleryId}`);
  return data;
};

// SMTP Settings
export interface SmtpSettings {
  smtp_host: string | null;
  smtp_port: string | null;
  smtp_username: string | null;
  smtp_password: string | null;
  smtp_sender: string | null;
  smtp_use_tls: string | null;
}

export const fetchSmtpSettings = async (): Promise<SmtpSettings> => {
  const { data } = await client.get<SmtpSettings>('/api/admin/smtp-settings');
  return data;
};

export const updateSmtpSettings = async (settings: Partial<SmtpSettings>) => {
  const { data } = await client.put('/api/admin/smtp-settings', settings);
  return data;
};

export const testSmtpEmail = async (recipient: string) => {
  const { data } = await client.post<{ success: boolean; message: string }>('/api/admin/smtp-test', { recipient });
  return data;
};
