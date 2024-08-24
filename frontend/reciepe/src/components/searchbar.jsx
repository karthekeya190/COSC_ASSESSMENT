import React, { useState } from 'react';
import styles from './searchBar.module.css';

function SearchBar({ onSearch }) {
  const [keyword, setKeyword] = useState('');
  const [cuisine, setCuisine] = useState('');
  const [dietaryPreference, setDietaryPreference] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(keyword, cuisine, dietaryPreference);
  };

  return (
    <div className={styles.searchContainer}>
      <form onSubmit={handleSubmit} className={styles.searchForm}>
        <div className={styles.inputGroup}>
          <input
            type="text"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            placeholder="Search recipes..."
            className={styles.input}
          />
        </div>
        <div className={styles.inputGroup}>
          <input
            type="text"
            value={cuisine}
            onChange={(e) => setCuisine(e.target.value)}
            placeholder="Cuisine"
            className={styles.input}
          />
        </div>
        <div className={styles.inputGroup}>
          <input
            type="text"
            value={dietaryPreference}
            onChange={(e) => setDietaryPreference(e.target.value)}
            placeholder="Dietary Preference"
            className={styles.input}
          />
        </div>
        <button type="submit" className={styles.searchButton}>
          <span className={styles.searchIcon}>🔍</span>
          Search
        </button>
      </form>
    </div>
  );
}

export default SearchBar;