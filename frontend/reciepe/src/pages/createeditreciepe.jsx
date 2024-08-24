import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './createedit.module.css';

function CreateEditRecipePage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [recipe, setRecipe] = useState({
    title: '',
    ingredients: '',
    instructions: '',
    cuisine: '',
    dietary_preferences: '',
  });

  useEffect(() => {
    if (id) {
      fetchRecipe();
    }
  }, [id]);

  const fetchRecipe = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/recipes/${id}`);
      setRecipe(response.data);
    } catch (error) {
      console.error('Error fetching recipe:', error);
    }
  };

  const handleChange = (e) => {
    setRecipe({ ...recipe, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (id) {
        await axios.put(`http://localhost:8000/recipes/${id}`, recipe);
      } else {
        await axios.post('http://localhost:8000/recipes/', recipe);
      }
      navigate('/recipes');
    } catch (error) {
      console.error('Error saving recipe:', error);
    }
  };

  return (
    <div className="container">
      <form onSubmit={handleSubmit} className={styles.form}>
        <h1 className={styles.formTitle}>{id ? 'Edit Recipe' : 'Create New Recipe'}</h1>
        <div className={styles.formGroup}>
          <label htmlFor="title" className={styles.label}>Title</label>
          <input
            id="title"
            name="title"
            value={recipe.title}
            onChange={handleChange}
            placeholder="Recipe Title"
            required
            className={styles.input}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="ingredients" className={styles.label}>Ingredients</label>
          <textarea
            id="ingredients"
            name="ingredients"
            value={recipe.ingredients}
            onChange={handleChange}
            placeholder="Ingredients"
            required
            className={styles.textarea}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="instructions" className={styles.label}>Instructions</label>
          <textarea
            id="instructions"
            name="instructions"
            value={recipe.instructions}
            onChange={handleChange}
            placeholder="Instructions"
            required
            className={styles.textarea}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="cuisine" className={styles.label}>Cuisine</label>
          <input
            id="cuisine"
            name="cuisine"
            value={recipe.cuisine}
            onChange={handleChange}
            placeholder="Cuisine"
            className={styles.input}
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="dietary_preferences" className={styles.label}>Dietary Preferences</label>
          <input
            id="dietary_preferences"
            name="dietary_preferences"
            value={recipe.dietary_preferences}
            onChange={handleChange}
            placeholder="Dietary Preferences"
            className={styles.input}
          />
        </div>
        <button type="submit" className={styles.submitButton}>{id ? 'Update' : 'Create'} Recipe</button>
      </form>
    </div>
  );
}


export default CreateEditRecipePage;