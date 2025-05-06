import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getPost, submitPost, publishPost } from '../api';

const PostDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [moderationResult, setModerationResult] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isPublishing, setIsPublishing] = useState(false);
  
  useEffect(() => {
    fetchPost();
  }, [id]);
  
  const fetchPost = async () => {
    setLoading(true);
    try {
      const data = await getPost(id);
      setPost(data);
      setError('');
      
      // Parse flagged reasons if any
      if (data.flagged_reasons) {
        try {
          const reasons = JSON.parse(data.flagged_reasons);
          setModerationResult({ status: 'flagged', reasons });
        } catch (e) {
          console.error('Error parsing flagged reasons:', e);
        }
      }
    } catch (err) {
      setError('Failed to load post. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  const handleSubmitForReview = async () => {
    setIsSubmitting(true);
    try {
      const result = await submitPost(id);
      setModerationResult(result);
      await fetchPost(); // Refresh post data
    } catch (err) {
      setError('Failed to submit post for review. Please try again.');
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };
  
  const handlePublish = async () => {
    setIsPublishing(true);
    try {
      await publishPost(id);
      await fetchPost(); // Refresh post data
    } catch (err) {
      setError('Failed to publish post. Please try again.');
      console.error(err);
    } finally {
      setIsPublishing(false);
    }
  };
  
  if (loading) return <div className="loading">Loading post...</div>;
  if (!post) return <div className="not-found">Post not found</div>;
  
  const isReadOnly = post.status === 'published';
  
  return (
    <div className="post-detail">
      <div className="header">
        <h2>{post.title}</h2>
        <div className={`status status-${post.status}`}>{post.status}</div>
      </div>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="content">
        {post.content}
      </div>
      
      {moderationResult && moderationResult.status === 'flagged' && (
        <div className="moderation-result flagged">
          <h3>Moderation Issues:</h3>
          <ul>
            {moderationResult.reasons.map((reason, index) => (
              <li key={index}>{reason}</li>
            ))}
          </ul>
        </div>
      )}
      
      {moderationResult && moderationResult.status === 'approved' && (
        <div className="moderation-result approved">
          <h3>Moderation Passed</h3>
          <p>Your post has been approved and can now be published.</p>
        </div>
      )}
      
      <div className="actions">
        {post.status === 'draft' && (
          <button 
            onClick={handleSubmitForReview} 
            disabled={isSubmitting}
            className="primary-button"
          >
            {isSubmitting ? 'Submitting...' : 'Submit for Review'}
          </button>
        )}
        
        {post.status === 'approved' && (
          <button 
            onClick={handlePublish} 
            disabled={isPublishing}
            className="primary-button"
          >
            {isPublishing ? 'Publishing...' : 'Publish Post'}
          </button>
        )}
        
        <Link to="/" className="button">Back to List</Link>
      </div>
    </div>
  );
};

export default PostDetail; 