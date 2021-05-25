from fastapi import FastAPI  # import fastapi class and depends
import blog.database as database
import blog.models as models
from blog.routers import user, blog, authentication


app = FastAPI()

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)

models.Base.metadata.create_all(database.engine)

get_db = database.get_db
