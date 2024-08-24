from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
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
    title = Column(String(100), index=True)
    ingredients = Column(String(1000))
    instructions = Column(String(2000))
    cuisine = Column(String(50))
    dietary_preferences = Column(String(100))
    average_rating = Column(Float, default=0.0)
    ratings = relationship("RatingModel", back_populates="recipe", cascade="all, delete-orphan")
    comments = relationship("CommentModel", back_populates="recipe", cascade="all, delete-orphan")

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
    content = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    recipe = relationship("RecipeModel", back_populates="comments")

Base.metadata.create_all(bind=engine)

# Pydantic models
class RecipeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    ingredients: str = Field(..., min_length=1, max_length=1000)
    instructions: str = Field(..., min_length=1, max_length=2000)
    cuisine: str = Field(..., min_length=1, max_length=50)
    dietary_preferences: str = Field(..., min_length=1, max_length=100)

class RecipeCreate(RecipeBase):
    pass

class Rating(BaseModel):
    id: int
    rating: float

    class Config:
        orm_mode = True

class Comment(BaseModel):
    id: int
    content: str
    created_at: datetime

    class Config:
        orm_mode = True

class Recipe(RecipeBase):
    id: int
    average_rating: float = 0.0
    ratings: List[Rating] = []
    comments: List[Comment] = []

    class Config:
        orm_mode = True

class RatingCreate(BaseModel):
    rating: float = Field(..., ge=0, le=5)

class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations
@app.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
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
def update_recipe(recipe_id: int, recipe: RecipeCreate, db: Session = Depends(get_db)):
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

# User ratings
@app.post("/recipes/{recipe_id}/rate", response_model=Recipe)
def rate_recipe(recipe_id: int, rating: RatingCreate, db: Session = Depends(get_db)):
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
    db.refresh(db_recipe)

    return db_recipe

# User comments
@app.post("/recipes/{recipe_id}/comment", response_model=Recipe)
def comment_recipe(recipe_id: int, comment: CommentCreate, db: Session = Depends(get_db)):
    db_recipe = db.query(RecipeModel).filter(RecipeModel.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    new_comment = CommentModel(content=comment.content, recipe_id=recipe_id)
    db.add(new_comment)
    db.commit()
    db.refresh(db_recipe)

    return db_recipe

@app.get("/recipes/{recipe_id}/comments", response_model=List[Comment])
def get_recipe_comments(recipe_id: int, db: Session = Depends(get_db)):
    comments = db.query(CommentModel).filter(CommentModel.recipe_id == recipe_id).all()
    return comments

# Sharing options (placeholder)
@app.post("/recipes/{recipe_id}/share")
def share_recipe(recipe_id: int, share_method: str):
    return {"message": f"Recipe shared via {share_method}"}