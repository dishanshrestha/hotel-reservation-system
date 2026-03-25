import client from './client';
import type { BookingsResponse } from '../types';

export const createBooking = async (payload: {
  room_id: number;
  start_date: string;
  end_date: string;
  name?: string;
  email?: string;
  phone?: string;
  total_price?: number;
}) => {
  const { data } = await client.post('/api/bookings', payload);
  return data;
};

export const fetchMyBookings = async (): Promise<BookingsResponse> => {
  const { data } = await client.get<BookingsResponse>('/api/bookings/me');
  return data;
};

export const cancelBooking = async (bookingId: number) => {
  const { data } = await client.patch(`/api/bookings/${bookingId}/cancel`);
  return data;
};

export const checkout = async (payload: {
  room_id: number;
  start_date: string;
  end_date: string;
  name: string;
  email: string;
  phone: string;
  total_price: number;
}) => {
  const { data } = await client.post('/api/checkout', payload);
  return data;
};
