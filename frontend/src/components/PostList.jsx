import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { listPosts } from '../api';

const StatusBadge = ({ status }) => {
  const getStatusClass = () => {
    switch (status) {
      case 'draft': return 'status-draft';
      case 'flagged': return 'status-flagged';
      case 'approved': return 'status-approved';
      case 'published': return 'status-published';
      default: return '';
    }
  };
  
  return <span className={`status-badge ${getStatusClass()}`}>{status}</span>;
};

const PostList = () => {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('');
  
  useEffect(() => {
    fetchPosts();
  }, [filter]);
  
  const fetchPosts = async () => {
    setLoading(true);
    try {
      const data = await listPosts(filter || null);
      setPosts(data);
      setError('');
    } catch (err) {
      setError('Failed to load posts. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) return <div className="loading">Loading posts...</div>;
  
  return (
    <div className="post-list">
      <h2>Blog Posts</h2>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="filter-buttons">
        <button 
          className={filter === '' ? 'active' : ''} 
          onClick={() => setFilter('')}
        >
          All
        </button>
        <button 
          className={filter === 'draft' ? 'active' : ''} 
          onClick={() => setFilter('draft')}
        >
          Drafts
        </button>
        <button 
          className={filter === 'flagged' ? 'active' : ''} 
          onClick={() => setFilter('flagged')}
        >
          Flagged
        </button>
        <button 
          className={filter === 'approved' ? 'active' : ''} 
          onClick={() => setFilter('approved')}
        >
          Approved
        </button>
        <button 
          className={filter === 'published' ? 'active' : ''} 
          onClick={() => setFilter('published')}
        >
          Published
        </button>
      </div>
      
      {posts.length === 0 ? (
        <div className="no-posts">No posts found</div>
      ) : (
        <ul className="posts">
          {posts.map(post => (
            <li key={post.id} className="post-item">
              <Link to={`/posts/${post.id}`}>
                <h3>{post.title}</h3>
                <StatusBadge status={post.status} />
                <p className="post-excerpt">
                  {post.content.substring(0, 100)}
                  {post.content.length > 100 ? '...' : ''}
                </p>
              </Link>
            </li>
          ))}
        </ul>
      )}
      
      <div className="actions">
        <Link to="/new" className="button">Create New Post</Link>
      </div>
    </div>
  );
};

export default PostList; 