export interface User {
  id: number;
  name: string;
  email: string;
  phone: string | null;
  usertype: string;
  profile_photo_path: string | null;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Room {
  id: number;
  room_title: string | null;
  image: string | null;
  image_raw: string | null;
  description: string | null;
  price: string | null;
  wifi: string;
  room_type: string | null;
  created_at: string;
  updated_at: string;
  average_rating: number;
  rating_count: number;
  ratings?: RoomRating[];
  recommendation_score?: number;
  recommendation_reasons?: string[];
}

export interface RoomRating {
  id: number;
  username: string;
  email: string;
  comment: string;
  rating: number;
  created_at: string;
}

export interface Booking {
  id: number;
  room_id: string;
  room_title: string | null;
  room_image: string | null;
  name: string | null;
  email: string | null;
  phone: string | null;
  status: string;
  start_date: string | null;
  end_date: string | null;
  total_price: number | null;
  created_at: string;
  updated_at: string;
}

export interface GalleryItem {
  id: number;
  image: string | null;
  image_raw: string | null;
  created_at: string;
  updated_at: string;
}

export interface Contact {
  id: number;
  name: string;
  email: string;
  phone: string;
  message: string;
  created_at: string;
  updated_at: string;
}

export interface AdminStats {
  total_users: number;
  total_bookings: number;
  total_rooms: number;
  total_income: number;
  status_counts: {
    rejected: number;
    canceled: number;
    approved: number;
    waiting: number;
  };
  bookings_by_month: {
    labels: string[];
    data: number[];
  };
}

export interface AlternativeSlot {
  start_date: string;
  end_date: string;
  nights: number;
}

export interface BookingConflictDetail {
  message: string;
  alternative_slots: AlternativeSlot[];
}

export interface RoomsResponse {
  count: number;
  rooms: Room[];
}

export interface BookingsResponse {
  count: number;
  bookings: Booking[];
}

export interface GalleryResponse {
  count: number;
  gallery: GalleryItem[];
}

export interface RecommendationsResponse {
  count: number;
  algorithm: string;
  recommendations: Room[];
}
