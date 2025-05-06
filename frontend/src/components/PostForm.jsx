import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createPost } from '../api';

const PostForm = () => {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!title.trim() || !content.trim()) {
      setError('Title and content are required');
      return;
    }
    
    setIsSubmitting(true);
    setError('');
    
    try {
      const newPost = await createPost(title, content);
      navigate(`/posts/${newPost.id}`);
    } catch (err) {
      setError('Failed to create post. Please try again.');
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="post-form">
      <h2>Create New Post</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="title">Title</label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            disabled={isSubmitting}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="content">Content</label>
          <textarea
            id="content"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows="10"
            disabled={isSubmitting}
            required
          />
          <small className="hint">Minimum 50 characters, maximum 2000 characters.</small>
        </div>
        
        <button type="submit" disabled={isSubmitting}>
          {isSubmitting ? 'Creating...' : 'Create Draft'}
        </button>
      </form>
    </div>
  );
};

export default PostForm; 