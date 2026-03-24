import client from './client';
import type { GalleryResponse } from '../types';

export const fetchGallery = async (): Promise<GalleryResponse> => {
  const { data } = await client.get<GalleryResponse>('/api/gallery');
  return data;
};
