import axios from 'axios';

const API_URL = 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Post APIs
export const createPost = async (title, content) => {
  try {
    const response = await api.post('/posts/', { title, content });
    return response.data;
  } catch (error) {
    console.error('Error creating post:', error);
    throw error;
  }
};

export const updatePost = async (postId, updates) => {
  try {
    const response = await api.patch(`/posts/${postId}`, updates);
    return response.data;
  } catch (error) {
    console.error('Error updating post:', error);
    throw error;
  }
};

export const submitPost = async (postId) => {
  try {
    const response = await api.post(`/posts/${postId}/submit/`);
    return response.data;
  } catch (error) {
    console.error('Error submitting post:', error);
    throw error;
  }
};

export const publishPost = async (postId) => {
  try {
    const response = await api.patch(`/posts/${postId}/publish/`);
    return response.data;
  } catch (error) {
    console.error('Error publishing post:', error);
    throw error;
  }
};

export const getPost = async (postId) => {
  try {
    const response = await api.get(`/posts/${postId}`);
    return response.data;
  } catch (error) {
    console.error('Error getting post:', error);
    throw error;
  }
};

export const listPosts = async (statusFilter = null) => {
  try {
    const params = statusFilter ? { status: statusFilter } : {};
    const response = await api.get('/posts/', { params });
    return response.data;
  } catch (error) {
    console.error('Error listing posts:', error);
    throw error;
  }
}; 