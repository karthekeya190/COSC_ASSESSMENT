import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './reciepedetails.module.css';

function RecipeDetailsPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [recipe, setRecipe] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const [newRating, setNewRating] = useState(0);

  useEffect(() => {
    fetchRecipe();
    fetchComments();
  }, [id]);

  const fetchRecipe = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/recipes/${id}`);
      setRecipe(response.data);
    } catch (error) {
      console.error('Error fetching recipe:', error);
    }
  };

  const fetchComments = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/recipes/${id}/comments`);
      setComments(response.data);
    } catch (error) {
      console.error('Error fetching comments:', error);
    }
  };

  const handleAddComment = async () => {
    try {
      const response = await axios.post(`http://localhost:8000/recipes/${id}/comment`, { content: newComment });
      setNewComment('');
      // Update the recipe state with the new data
      setRecipe(response.data);
      // Add the new comment to the comments state
      setComments(prevComments => [...prevComments, response.data.comments[response.data.comments.length - 1]]);
    } catch (error) {
      console.error('Error adding comment:', error);
    }
  };

  const handleAddRating = async () => {
    try {
      const response = await axios.post(`http://localhost:8000/recipes/${id}/rate`, { rating: newRating });
      setNewRating(0);
      setRecipe(response.data);
    } catch (error) {
      console.error('Error adding rating:', error);
    }
  };

  const handleShare = async (method) => {
    try {
      await axios.post(`http://localhost:8000/recipes/${id}/share`, { share_method: method });
      alert(`Recipe shared via ${method}`);
    } catch (error) {
      console.error('Error sharing recipe:', error);
    }
  };

  const handleDelete = async () => {
    try {
      await axios.delete(`http://localhost:8000/recipes/${id}`);
      navigate('/recipes');
    } catch (error) {
      console.error('Error deleting recipe:', error);
    }
  };

  if (!recipe) return <div className="container">Loading...</div>;

  return (
    <div className="container">
      <div className={styles.recipeDetails}>
        <h1 className={styles.recipeTitle}>{recipe.title}</h1>
        <div className={styles.recipeInfo}>
          <p>Cuisine: {recipe.cuisine}</p>
          <p>Dietary Preferences: {recipe.dietary_preferences}</p>
          <p>Average Rating: {recipe.average_rating.toFixed(1)}</p>
        </div>
        <div className={styles.recipeSection}>
          <h2 className={styles.sectionTitle}>Ingredients</h2>
          <p>{recipe.ingredients}</p>
        </div>
        <div className={styles.recipeSection}>
          <h2 className={styles.sectionTitle}>Instructions</h2>
          <p>{recipe.instructions}</p>
        </div>
        
        {/* Rating Section */}
        <div className={styles.ratingSection}>
          <h2 className={styles.sectionTitle}>Rate this Recipe</h2>
          <input
            type="number"
            min="0"
            max="5"
            value={newRating}
            onChange={(e) => setNewRating(Number(e.target.value))}
          />
          <button onClick={handleAddRating} className={styles.button}>Submit Rating</button>
        </div>

        {/* Comments Section */}
        <div className={styles.commentsSection}>
          <h2 className={styles.sectionTitle}>Comments</h2>
          {comments.map((comment, index) => (
            <div key={index} className={styles.comment}>
              <p>{comment.content}</p>
              <small>{new Date(comment.created_at).toLocaleString()}</small>
            </div>
          ))}
          <div className={styles.addComment}>
            <textarea
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              placeholder="Add a comment..."
            />
            <button onClick={handleAddComment} className={styles.button}>Add Comment</button>
          </div>
        </div>

        {/* Sharing Section */}
        <div className={styles.sharingSection}>
          <h2 className={styles.sectionTitle}>Share this Recipe</h2>
          <button onClick={() => handleShare('Facebook')} className={styles.button}>Share on Facebook</button>
          <button onClick={() => handleShare('Twitter')} className={styles.button}>Share on Twitter</button>
        </div>

        <button onClick={() => navigate(`/recipes/${id}/edit`)} className={styles.button}>Edit Recipe</button>
        <button onClick={handleDelete} className={`${styles.button} ${styles.deleteButton}`}>Delete Recipe</button>
      </div>
    </div>
  );
}

export default RecipeDetailsPage;