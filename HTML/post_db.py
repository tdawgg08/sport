from database.database import engine, AsyncSessionLocal
from database.models import Category, SubCategory, Product

from HTML.BJU import parse_local_html

async def post_