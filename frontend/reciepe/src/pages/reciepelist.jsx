import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import SearchBar from '../components/SearchBar';
import styles from './reciepelist.module.css';

function RecipeListPage() {
  const [recipes, setRecipes] = useState([]);

  useEffect(() => {
    fetchRecipes();
  }, []);

  const fetchRecipes = async () => {
    try {
      const response = await axios.get('http://localhost:8000/recipes/');
      setRecipes(response.data);
    } catch (error) {
      console.error('Error fetching recipes:', error);
    }
  };

  const handleSearch = async (keyword, cuisine, dietaryPreference) => {
    try {
      const response = await axios.get(`http://localhost:8000/recipes/search/`, {
        params: { keyword, cuisine, dietary_preference: dietaryPreference }
      });
      setRecipes(response.data);
    } catch (error) {
      console.error('Error searching recipes:', error);
    }
  };

  return (
    <div className="container">
      <h1>Recipes</h1>
      <SearchBar onSearch={handleSearch} />
      <div className={styles.recipeGrid}>
        {recipes.map((recipe) => (
          <div key={recipe.id} className={styles.recipeCard}>
            <h3 className={styles.recipeTitle}>{recipe.title}</h3>
            <p className={styles.recipeInfo}>Cuisine: {recipe.cuisine}</p>
            <p className={styles.recipeInfo}>Dietary Preferences: {recipe.dietary_preferences}</p>
            <p className={styles.recipeInfo}>Average Rating: {recipe.average_rating.toFixed(1)}</p>
            <Link to={`/recipes/${recipe.id}`} className={styles.recipeLink}>View Details</Link>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecipeListPage;
