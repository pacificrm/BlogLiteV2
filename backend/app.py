from os import path
from flask import Flask , render_template,request,redirect,flash
from models import db,Users,Blogs,Follow,Comments,Likes,Dislikes,Role
from flask_security import Security
from flask_restful import Api
from flask_cors import CORS
from api import UsersAPI,user_datastore,BlogAPI,ProfileAPI,SearchAPI,FollowAPI,UnfollowAPI,LikeUnlikeAPI,CommentAPI,ExportblogAPI


from celery.schedules import crontab
import clery as clery
from cache import cache
from tasks import daily_reminder, monthly_reminder


app= Flask(__name__)

cd= path.abspath(path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+path.join(cd,"database.sqlite3")
app.config['SECURITY_USERNAME_ENABLE']=True
# app.config['SECURITY_TRACKABLE']=True
app.config['SECRET_KEY'] = "yudw890_ASHudb^T^%VSA%&*CASGVHSbsjdbjsd"
app.config['SECURITY_PASSWORD_SALT'] = 'Thi$_is@#super9secrets%$'
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = "Authentication-Token"
app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'


app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'
app.config['CELERY_ENABLE_UTC'] = False
app.config['CELERY_TIMEZONE']='Asia/Kolkata'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/3'
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 100



api=Api(app)
CORS(app)
db.init_app(app)
cache.init_app(app)


celery = clery.celery
app.app_context().push()

celery.conf.update(
     broker_url='redis://localhost:6379/1',
     result_backend='redis://localhost:6379/2'
 )

celery.Task = clery.ContextTask
app.app_context().push()

Security().init_app(app, user_datastore)


api.add_resource(UsersAPI, '/api/user')
api.add_resource(BlogAPI, '/api/blog','/api/blog/<int:id>')
api.add_resource(ProfileAPI,'/api/profile/<string:username>')
api.add_resource(SearchAPI, '/api/search')
api.add_resource(FollowAPI, '/api/follow')
api.add_resource(UnfollowAPI, '/api/unfollow')
api.add_resource(LikeUnlikeAPI,'/api/likeunlike')
api.add_resource(CommentAPI,'/api/comment/<int:id>')
api.add_resource(ExportblogAPI, "/api/exportblogs")


@app.before_first_request
def create():
    if not path.exists('sqlite:///database.sqlite3'):
        db.create_all()


@app.route('/')
def start():
    return "hello"


import datetime
import pytz
def timee(): 
    return datetime.datetime.now(pytz.timezone('Asia/Kolkata')) 


@celery.on_after_finalize.connect
def monthly_report(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=23, minute=14, day_of_month="22", nowfun=timee),
        monthly_reminder.s(),
    )
    # sender.add_periodic_task(
    #     crontab(hour=16, minute=47, day_of_week='*', nowfun=timee),
    #     daily_reminder.s(),
    # )


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # sender.add_periodic_task(
    #    10, generate_daily_report.s(), name='Daily ')
     sender.add_periodic_task(
        crontab(hour=23, minute=14, day_of_week='*', nowfun=timee),
        daily_reminder.s(),
    )

    # sender.add_periodic_task(
    #     crontab(hour=16, minute=52), daily_reminder.s(), name='Daily ')


celery.conf.timezone = 'Asia/Kolkata'



if __name__=="__main__":
    app.run(debug=True)


# ~/go/bin/MailHog
#redis-server in redis at desktop
#npm run serve in frntend
#python3 app.py in bkend
#mailhog
#celery -A app.celery beat --max-interval 1 -l info in bkend
#celery -A app.celery worker -l info in bkend
