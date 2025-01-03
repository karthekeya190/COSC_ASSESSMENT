# COSC's Recipe Manager

Welcome to the COSC's Recipe Manager! This application is designed for COSC members to share and explore recipes within the club. With features like sharing recipes, liking, commenting, and an advanced search filter, this platform fosters an engaging and interactive cooking community.

## Features

1. **Share Recipes**: Users can upload their favorite recipes, including ingredients, steps, and optional images.
2. **Like and Comment**: Interact with shared recipes by liking and leaving comments.
3. **Search and Filter**: Use the search bar to find recipes by keywords, ingredients, or other criteria.
4. **User-Friendly Interface**: Intuitive design for easy navigation and seamless user experience.

## Getting Started

### Prerequisites

To run this project locally, ensure you have the following installed:

- Node.js
- Python (for FastAPI backend)
- Uvicorn (ASGI server)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/recipe-manager.git
   cd recipe-manager
   ```

2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Set up the backend:
   ```bash
   cd ../backend
   pip install fastapi uvicorn
   ```

4. Run the backend:
   ```bash
   uvicorn main:app --reload
   ```

5. Run the frontend:
   ```bash
   cd ../frontend
   npm start
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

## Usage

1. **Share Recipes**: Use the "Add Recipe" button to share your recipes.
2. **Interact**: Browse recipes, like your favorites, and leave comments to share your thoughts.
3. **Search**: Use the search bar to find recipes based on keywords or ingredients.

## Technologies Used

- **Frontend**: React.js
- **Backend**: FastAPI
- **Server**: Uvicorn
- **Styling**: CSS/Bootstrap

## Contributing

We welcome contributions to improve this project! If you'd like to contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them:
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.



---

Happy Cooking! 🍳
