import client from './client';

export const submitContact = async (payload: {
  name: string;
  email: string;
  phone: string;
  message: string;
}) => {
  const { data } = await client.post('/api/contact', payload);
  return data;
};
