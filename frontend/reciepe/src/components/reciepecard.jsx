import React from 'react';
import { Link } from 'react-router-dom';
import styles from './RecipeCard.module.css';

function RecipeCard({ recipe }) {
  return (
    <div className={styles.recipeCard}>
      <img src={recipe.imageUrl || 'default-recipe-image.jpg'} alt={recipe.title} className={styles.recipeImage} />
      <h3 className={styles.recipeTitle}>{recipe.title}</h3>
      <p className={styles.recipeInfo}>Cuisine: {recipe.cuisine}</p>
      <p className={styles.recipeInfo}>Dietary Preferences: {recipe.dietary_preferences}</p>
      <p className={styles.recipeInfo}>Average Rating: {recipe.average_rating.toFixed(1)}</p>
      <Link to={`/recipes/${recipe.id}`} className={styles.recipeLink}>View Details</Link>
    </div>
  );
}

export default RecipeCard;