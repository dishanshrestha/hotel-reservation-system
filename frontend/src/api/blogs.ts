import client from './client';
import type { Blog, BlogsResponse } from '../types';

export const fetchBlogs = async (): Promise<BlogsResponse> => {
  const { data } = await client.get<BlogsResponse>('/api/blogs');
  return data;
};

export const fetchBlog = async (blogId: number): Promise<Blog> => {
  const { data } = await client.get<Blog>(`/api/blogs/${blogId}`);
  return data;
};

// Admin
export const fetchAdminBlogs = async (): Promise<BlogsResponse> => {
  const { data } = await client.get<BlogsResponse>('/api/admin/blogs');
  return data;
};

export const createAdminBlog = async (payload: {
  title: string;
  excerpt?: string;
  content?: string;
  image?: string;
  category?: string;
  author?: string;
}): Promise<Blog> => {
  const { data } = await client.post<Blog>('/api/admin/blogs', payload);
  return data;
};

export const updateAdminBlog = async (
  blogId: number,
  payload: Partial<{
    title: string;
    excerpt: string;
    content: string;
    image: string;
    category: string;
    author: string;
  }>
): Promise<Blog> => {
  const { data } = await client.put<Blog>(`/api/admin/blogs/${blogId}`, payload);
  return data;
};

export const deleteAdminBlog = async (blogId: number) => {
  const { data } = await client.delete(`/api/admin/blogs/${blogId}`);
  return data;
};
