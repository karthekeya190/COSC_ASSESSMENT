import React from 'react';
import { Link } from 'react-router-dom';
import styles from './homepage.module.css';

function HomePage() {
  return (
    <div className={styles.hero}>
      <div className="container">
        <h1 className={styles.heroTitle}>Welcome to COSC Recipe Organizer</h1>
        <p className={styles.heroText}>Share and manage your favorite recipes with the CBIT Open Source Community!</p>
        <Link to="/recipes" className={styles.ctaButton}>View Recipes</Link>
      </div>
    </div>
  );
}

export default HomePage;