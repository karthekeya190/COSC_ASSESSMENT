// src/components/Navbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import styles from './navbar.module.css';

function Navbar() {
  return (
    <nav className={styles.navbar}>
      <div className={`container ${styles.navContainer}`}>
        <h1>Recipe Organizer</h1>
        <ul className={styles.navList}>
          <li className={styles.navItem}><Link to="/" className={styles.navLink}>Home</Link></li>
          <li className={styles.navItem}><Link to="/recipes" className={styles.navLink}>Recipes</Link></li>
          <li className={styles.navItem}><Link to="/recipes/new" className={styles.navLink}>Add New Recipe</Link></li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;
