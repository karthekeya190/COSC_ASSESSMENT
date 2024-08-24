import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/navbar';
import HomePage from './pages/homepage';
import RecipeListPage from './pages/reciepelist';
import RecipeDetailsPage from './pages/reciepedetails';
import CreateEditRecipePage from './pages/createeditreciepe';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/recipes" element={<RecipeListPage />} />
          <Route path="/recipes/new" element={<CreateEditRecipePage />} />
          <Route path="/recipes/:id" element={<RecipeDetailsPage />} />
          <Route path="/recipes/:id/edit" element={<CreateEditRecipePage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;