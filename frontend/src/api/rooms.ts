import client from './client';
import type { Room, RoomsResponse, RecommendationsResponse } from '../types';

export const fetchRooms = async (params?: {
  price_range?: string;
  room_type?: string;
}): Promise<RoomsResponse> => {
  const { data } = await client.get<RoomsResponse>('/api/rooms', { params });
  return data;
};

export const fetchRoomDetails = async (roomId: number): Promise<Room> => {
  const { data } = await client.get<Room>(`/api/rooms/${roomId}`);
  return data;
};

export const searchRooms = async (params?: {
  price_range?: string;
  room_type?: string;
}): Promise<RoomsResponse> => {
  const { data } = await client.get<RoomsResponse>('/api/search-rooms', { params });
  return data;
};

export const fetchRecommendations = async (params: {
  start_date?: string;
  end_date?: string;
  room_type?: string;
  max_budget?: number;
  wifi?: string;
  top_k?: number;
}): Promise<RecommendationsResponse> => {
  const { data } = await client.get<RecommendationsResponse>('/api/recommendations/rooms', { params });
  return data;
};

export const fetchAvailabilitySuggestions = async (
  roomId: number,
  startDate: string,
  endDate: string,
  maxSuggestions?: number
) => {
  const { data } = await client.get(`/api/rooms/${roomId}/availability-suggestions`, {
    params: { start_date: startDate, end_date: endDate, max_suggestions: maxSuggestions },
  });
  return data;
};
