import client from './client';
import type { TokenResponse, User } from '../types';

export const loginUser = async (email: string, password: string): Promise<TokenResponse> => {
  const { data } = await client.post<TokenResponse>('/api/auth/login', { email, password });
  return data;
};

export const registerUser = async (payload: {
  name: string;
  email: string;
  password: string;
  phone?: string;
}): Promise<User> => {
  const { data } = await client.post<User>('/api/auth/register', payload);
  return data;
};

export const getProfile = async (): Promise<User> => {
  const { data } = await client.get<User>('/api/profile');
  return data;
};
