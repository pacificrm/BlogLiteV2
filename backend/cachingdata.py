from models import Blogs,Users
from cache import cache


@cache.memoize(timeout=10)
def get_blogs_by_blogId(blog_id):
    return Blogs.query.filter_by(id=blog_id).first()

@cache.memoize(timeout=10)
def get_user_by_username(username):
    return Users.query.filter_by(username=username).first()