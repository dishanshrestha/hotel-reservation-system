import client from './client';

export const submitRating = async (
  roomId: number,
  payload: { name: string; email: string; comment: string; rating: number }
) => {
  const { data } = await client.post(`/api/ratings/${roomId}`, payload);
  return data;
};
