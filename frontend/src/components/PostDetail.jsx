import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { getPost, submitPost, publishPost, updatePost, deletePost } from '../api';

const PostDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [moderationResult, setModerationResult] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isPublishing, setIsPublishing] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState('');
  const [editedContent, setEditedContent] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  
  useEffect(() => {
    fetchPost();
  }, [id]);
  
  const fetchPost = async () => {
    setLoading(true);
    try {
      const data = await getPost(id);
      setPost(data);
      setEditedTitle(data.title);
      setEditedContent(data.content);
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

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await deletePost(id);
      navigate('/'); // Redirect to posts list after deletion
    } catch (err) {
      setError('Failed to delete post. Please try again.');
      console.error(err);
    } finally {
      setIsDeleting(false);
      setShowDeleteConfirm(false);
    }
  };

  const toggleDeleteConfirm = () => {
    setShowDeleteConfirm(!showDeleteConfirm);
  };

  const toggleEdit = () => {
    setIsEditing(!isEditing);
    if (!isEditing) {
      setEditedTitle(post.title);
      setEditedContent(post.content);
    }
  };

  const handleSaveEdit = async (e) => {
    e.preventDefault();
    
    if (!editedTitle.trim() || !editedContent.trim()) {
      setError('Title and content are required');
      return;
    }
    
    setIsSaving(true);
    try {
      await updatePost(id, {
        title: editedTitle,
        content: editedContent
      });
      
      await fetchPost(); // Refresh post data
      setIsEditing(false);
      setError('');
    } catch (err) {
      setError('Failed to update post. Please try again.');
      console.error(err);
    } finally {
      setIsSaving(false);
    }
  };
  
  if (loading) return <div className="loading">Loading post...</div>;
  if (!post) return <div className="not-found">Post not found</div>;
  
  const isReadOnly = post.status === 'published';
  const isDraft = post.status === 'draft';
  
  return (
    <div className="post-detail">
      <div className="header">
        {isEditing ? (
          <h2>Editing Post</h2>
        ) : (
          <h2>{post.title}</h2>
        )}
        <div className={`status status-${post.status}`}>{post.status}</div>
      </div>
      
      {error && <div className="error-message">{error}</div>}
      
      {isEditing ? (
        <form onSubmit={handleSaveEdit} className="edit-form">
          <div className="form-group">
            <label htmlFor="title">Title</label>
            <input
              type="text"
              id="title"
              value={editedTitle}
              onChange={(e) => setEditedTitle(e.target.value)}
              disabled={isSaving}
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="content">Content</label>
            <textarea
              id="content"
              value={editedContent}
              onChange={(e) => setEditedContent(e.target.value)}
              rows="10"
              disabled={isSaving}
              required
            />
            <small className="hint">Minimum 50 characters, maximum 2000 characters.</small>
          </div>
          
          <div className="actions">
            <button type="submit" disabled={isSaving} className="primary-button">
              {isSaving ? 'Saving...' : 'Save Changes'}
            </button>
            <button type="button" onClick={toggleEdit} disabled={isSaving} className="secondary-button">
              Cancel
            </button>
          </div>
        </form>
      ) : (
        <>
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
          
          {showDeleteConfirm ? (
            <div className="delete-confirmation">
              <p>Are you sure you want to delete this post? This action cannot be undone.</p>
              <div className="actions">
                <button 
                  onClick={handleDelete} 
                  disabled={isDeleting}
                  className="delete-button"
                >
                  {isDeleting ? 'Deleting...' : 'Confirm Delete'}
                </button>
                <button 
                  onClick={toggleDeleteConfirm} 
                  className="secondary-button"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div className="actions">
              {isDraft && (
                <>
                  <button 
                    onClick={handleSubmitForReview} 
                    disabled={isSubmitting}
                    className="primary-button"
                  >
                    {isSubmitting ? 'Submitting...' : 'Submit for Review'}
                  </button>
                  <button 
                    onClick={toggleEdit} 
                    className="secondary-button"
                  >
                    Edit Draft
                  </button>
                </>
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
              
              <button
                onClick={toggleDeleteConfirm}
                className="delete-button"
              >
                Delete Post
              </button>
              
              <Link to="/" className="button">Back to List</Link>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default PostDetail;