from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # This matches your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)








# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./recipes.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Recipe model
class RecipeModel(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    ingredients = Column(String)
    instructions = Column(String)
    cuisine = Column(String)
    dietary_preferences = Column(String)
    average_rating = Column(Float, default=0.0)
    ratings = relationship("RatingModel", back_populates="recipe")
    comments = relationship("CommentModel", back_populates="recipe")

# Rating model
class RatingModel(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("RecipeModel", back_populates="ratings")

# Comment model
class CommentModel(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(String, default=datetime.utcnow)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("RecipeModel", back_populates="comments")

Base.metadata.create_all(bind=engine)

# Pydantic models for request/response
class Recipe(BaseModel):
    id: Optional[int]
    title: str
    ingredients: str
    instructions: str
    cuisine: str
    dietary_preferences: str
    average_rating: Optional[float]

class Rating(BaseModel):
    rating: float

class Comment(BaseModel):
    content: str

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations (same as before)
# ...
@app.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: Recipe, db: Session = Depends(get_db)):
    db_recipe = RecipeModel(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.get("/recipes/", response_model=List[Recipe])
def read_recipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recipes = db.query(RecipeModel).offset(skip).limit(limit).all()
    return recipes

@app.get("/recipes/{recipe_id}", response_model=Recipe)
def read_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

@app.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, recipe: Recipe, db: Session = Depends(get_db)):
    db_recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    for key, value in recipe.dict().items():
        setattr(db_recipe, key, value)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(db_recipe)
    db.commit()
    return {"message": "Recipe deleted successfully"}

# Search and filter endpoint
@app.get("/recipes/search/", response_model=List[Recipe])
def search_recipes(
    keyword: Optional[str] = None,
    cuisine: Optional[str] = None,
    dietary_preference: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(RecipeModel)
    if keyword:
        query = query.filter(RecipeModel.title.contains(keyword) | RecipeModel.ingredients.contains(keyword))
    if cuisine:
        query = query.filter(RecipeModel.cuisine == cuisine)
    if dietary_preference:
        query = query.filter(RecipeModel.dietary_preferences.contains(dietary_preference))
    return query.all()

# Extra credit: User ratings
@app.post("/recipes/{recipe_id}/rate")
def rate_recipe(recipe_id: int, rating: Rating, db: Session = Depends(get_db)):
    db_recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    new_rating = RatingModel(rating=rating.rating, recipe_id=recipe_id)
    db.add(new_rating)
    db.commit()

    # Update average rating
    all_ratings = db.query(RatingModel).filter(RatingModel.recipe_id == recipe_id).all()
    db_recipe.average_rating = sum(r.rating for r in all_ratings) / len(all_ratings)
    db.commit()

    return {"message": "Rating submitted successfully"}

# Extra credit: User comments
@app.post("/recipes/{recipe_id}/comment")
def comment_recipe(recipe_id: int, comment: Comment, db: Session = Depends(get_db)):
    db_recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    new_comment = CommentModel(content=comment.content, recipe_id=recipe_id)
    db.add(new_comment)
    db.commit()

    return {"message": "Comment added successfully"}

@app.get("/recipes/{recipe_id}/comments")
def get_recipe_comments(recipe_id: int, db: Session = Depends(get_db)):
    comments = db.query(CommentModel).filter(CommentModel.recipe_id == recipe_id).all()
    return comments

# Extra credit: Sharing options
@app.post("/recipes/{recipe_id}/share")
def share_recipe(recipe_id: int, share_method: str):
    # In a real application, you'd implement actual sharing logic here
    # For this example, we'll just return a success message
    return {"message": f"Recipe shared via {share_method}"}