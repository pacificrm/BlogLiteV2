from models import db,Users,Blogs,Follow,Comments,Likes,Dislikes,Role
from flask_security import SQLAlchemyUserDatastore,auth_required,current_user,hash_password
from flask_restful import Resource, reqparse, fields, marshal_with
from flask import jsonify,request
from datetime import datetime
import werkzeug
import os
from os import path
import matplotlib.pyplot as plt
import tasks
from cache import cache
import cachingdata

cd = os.getcwd()

UPLOAD_BLOG = '../frontend/src/assets/blogs'
UPLOAD_PROFILE= '../frontend/src/assets/profile'

user_datastore=SQLAlchemyUserDatastore(db,Users,Role)

user_req = reqparse.RequestParser()
user_req.add_argument('email', required=True, help="email required")
user_req.add_argument('username', required=True, help="username required")
user_req.add_argument('password1', required=True, help="password required")


user_fields = {
    'username' : fields.String ,
    'email' : fields.String ,
}

class UsersAPI(Resource):
    @cache.memoize(timeout=10)
    @auth_required('token')
    def get(self):
        chk=Users.query.filter_by(id=current_user.id).first()
        following= Follow.query.filter_by(follower_id=current_user.id).all()
        follower= Follow.query.filter_by(followed_id=current_user.id).all()
        flr=[]
        flng=[]
        for fl in following:
            u=Users.query.filter_by(id=fl.followed_id).first()
            flng.append({'username':u.username,'uid':u.id})
        for fl in follower:
            u=Users.query.filter_by(id=fl.follower_id).first()
            flr.append({'username':u.username,'uid':u.id})
        print(following)
        blogs=[]
        if following:
            blgs=Blogs.query.filter(Blogs.user_id.in_([c.followed_id for c in following])).order_by(Blogs.blog_time.desc()).all()
            print(blgs)
            # if len(blgs)>5:
            #     blgs=blgs[:5]
            for blg in blgs:
                l=Likes.query.filter_by(blog_id=blg.id).count()
                dl=Dislikes.query.filter_by(blog_id=blg.id).count()
                cmnt=Comments.query.filter_by(blog_id=blg.id).count()
                blogs.append({'id':blg.id,'title':blg.blog_title,'preview':blg.blog_preview,'content':blg.blog_content,'date':blg.blog_time.strftime("%d %b"),'time':blg.blog_time.strftime( "%I:%M %p"),'user':blg.user.username,'image':blg.blog_img,'likes':l,'dislikes':dl,'comments':cmnt})
        print(blogs)
        return { 'blogs':blogs,'email':current_user.email,'fullname':current_user.fullname,'about':current_user.about,'follower':flr,'following':flng }

    @marshal_with(user_fields)
    def post(self):
        args = user_req.parse_args()
        email = args.get("email")
        user_name = args.get("username")
        passw = args.get("password1")
        check1=Users.query.filter_by(email=email).first()
        check2=Users.query.filter_by(username=user_name).first()
        if check1:
           print(check1)
           return jsonify('User already exist!! Try with another email.'),400
        elif check2:
           print(check2)
           return jsonify('User already exist!! Try with another username.'),401
        elif not check1 and not check2:    
            user_datastore.create_user(email=email,username=user_name,password=hash_password(passw))
            db.session.commit()
            data = Users.query.filter_by(email=email).first()
            return data,200
        else:
            return jsonify('Error happend !! Please enter the details again. '),500
    def put(self):
        try:
            fullname=request.form.get('fullname')
            about=request.form.get('about')
            profile_pic=request.files['profile_pic']
            imgname="no-profile-pic.jpeg"
            if profile_pic:
                imgname="{cu}{dt}.jpeg".format(cu=current_user.username,dt=datetime.now())
                profile_pic.save(path.join(UPLOAD_PROFILE, imgname))
                Users.query.filter_by(id=current_user.id).update({'fullname': fullname, 'about': about,
                                                'profile_img': imgname})
                db.session.commit()
        except:
            fullname=request.form.get('fullname')
            about=request.form.get('about')
            imgname="no-profile-pic.jpeg"
            Users.query.filter_by(id=current_user.id).update({'fullname': fullname, 'about': about,'profile_img': imgname
                                         })
            db.session.commit()  

    @auth_required('token')
    def delete(self):
        print(current_user.id)
        Likes.query.filter_by(user_id=current_user.id).delete()
        Dislikes.query.filter_by(user_id=current_user.id).delete()
        Comments.query.filter_by(user_id=current_user.id).delete()
        Blogs.query.filter_by(user_id=current_user.id).delete()
        # Profile.query.filter_by(user_id=current_user.id).delete()
        Users.query.filter_by(id=current_user.id).delete()
        Follow.query.filter_by(followed_id=current_user.id).delete()
        Follow.query.filter_by(follower_id=current_user.id).delete()
        db.session.commit()
        return {'del':'done'}


blog_req_args=reqparse.RequestParser()
blog_req_args.add_argument('blogTitle', required=True,type=werkzeug.datastructures.FileStorage, help="blog title is required",location='form')
blog_req_args.add_argument('blogContent',required=True,type=werkzeug.datastructures.FileStorage,help="blog content is required",location='form')
blog_req_args.add_argument('blogPrev',required=True,help="blog preview is required",location='form')
blog_req_args.add_argument('blogImage',required=True,help="blog preview is required",location='form')
blog_req_args.add_argument('formData',required=True,type=werkzeug.datastructures.FileStorage, help="blog preview is required",location='form')

Blog_fields = {
    'blogTitle' : fields.String ,
    'blogPrev' : fields.String ,
    'blogImage' : fields.String ,
    'blogContent' : fields.String ,
}


class BlogAPI(Resource):
    @auth_required('token')
    # @cache.memoize(timeout=10)
    def get(self,id):

        # blg=Blogs.query.filter_by(id=id).first()
        blg=cachingdata.get_blogs_by_blogId(blog_id=id)
        
        l=Likes.query.filter_by(blog_id=id).count()
        dl=Dislikes.query.filter_by(blog_id=id).count()
        cmnt=Comments.query.filter_by(blog_id=id).count()
        x=["Likes","Dislikes",'Comments']
        y=[l,dl,cmnt]
        plt.clf()
        plt.bar(x, y,color='green')
        # plt.plot(x,y,c='r',marker='o')
        plt.ylabel("Frequency", rotation="vertical",fontsize=15 ,c="r")
        plt.xlabel("Post-Engagement" ,c="b")
        plt.grid(axis='both', alpha=0.65)
        plt.title('Post-engagement graph',fontsize=15,c="r")
        plt.yticks([n for n in range(int(max(y))+4)])
        plt.legend('count')
        dic=os.getcwd()
        print(dic)
        plt.savefig("../frontend/src/assets/test.png")
        return{'title':blg.blog_title,'preview':blg.blog_preview,'content':blg.blog_content}


    # @marshal_with(user_fields)
    @auth_required('token')
    def post(self):
        try:
            blog_title=request.form.get('blogTitle')
            blog_prev=request.form.get('blogPrev')
            blog_content=request.form.get('blogContent')
            blog_img=request.files['blogImage']
            imgname="no-img.jpeg"
            if blog_img:
                imgname="{cu}{dt}.jpeg".format(cu=current_user.username,dt=datetime.now())
                blog_img.save(path.join(UPLOAD_BLOG, imgname))
                bg=Blogs(blog_title=blog_title,blog_preview=blog_prev,blog_content=blog_content,blog_img=imgname,user_id=current_user.id,blog_time=datetime.now())
                db.session.add(bg)
                db.session.commit()
                return{'blog':'posted'}
            
        except:
            blog_title=request.form.get('blogTitle')
            blog_prev=request.form.get('blogPrev')
            blog_content=request.form.get('blogContent')
            imgname="no-img.jpeg"
            bg=Blogs(blog_title=blog_title,blog_preview=blog_prev,blog_content=blog_content,blog_img=imgname,user_id=current_user.id,blog_time=datetime.now())
            db.session.add(bg)
            db.session.commit()
            cache.delete_memoized(cachingdata.get_blogs_by_blogId)
            return{'blog':'posted'}

    @auth_required('token')
    def put(self,id):
        try:
            title=request.form.get('blogTitle')
            prev=request.form.get('blogPrev')
            content=request.form.get('blogContent')
            blog_img=request.files['blogImage']
            imgname="no-img.jpeg"
            if blog_img:
                imgname="{cu}{dt}.jpeg".format(cu=current_user.username,dt=datetime.now())
                blog_img.save(path.join(UPLOAD_BLOG, imgname))
            Blogs.query.filter_by(id=id).update(dict(blog_title=title,blog_preview=prev,blog_content=content,
                blog_img=imgname,blog_time=datetime.now()))
            db.session.commit()
            cache.delete_memoized(cachingdata.get_blogs_by_blogId)
        except:
            title=request.form.get('blogTitle')
            prev=request.form.get('blogPrev')
            content=request.form.get('blogContent')
            # blog_img=request.files['blogImage']
            # imgname="no-img.jpeg"
            Blogs.query.filter_by(id=id).update(dict(blog_title=title,blog_preview=prev,blog_content=content,blog_time=datetime.now()))
            db.session.commit()

    def delete(self,id):
        Likes.query.filter_by(blog_id=id).delete()
        Dislikes.query.filter_by(blog_id=id).delete()
        Comments.query.filter_by(blog_id=id).delete()
        Blogs.query.filter_by(id=id).delete()
        db.session.commit()
        cache.delete_memoized(cachingdata.get_blogs_by_blogId)
        return {'del':'done'}


class ProfileAPI(Resource):
    def get (self,username):
        print(username)
        chk=cachingdata.get_user_by_username(username)
        print(chk)
        following= Follow.query.filter_by(follower_id=chk.id).count()
        followers=Follow.query.filter_by(followed_id=chk.id).count()
        blgs=Blogs.query.filter_by(user_id=chk.id).order_by(Blogs.blog_time.desc()).all()
        blogs=[]
        for blg in blgs:
            l=Likes.query.filter_by(blog_id=blg.id).count()
            dl=Dislikes.query.filter_by(blog_id=blg.id).count()
            cmnt=Comments.query.filter_by(blog_id=blg.id).count()
            # print({'id':blg.id,'title':blg.blog_title,'preview':blg.blog_preview,'content':blg.blog_content,'date':blg.blog_time.strftime("%m/%d/%Y"),'time':blg.blog_time.strftime( "%I:%M %p"),'user':blg.user.username,'image':blg.blog_img})
            blogs.append({'id':blg.id,'title':blg.blog_title,'preview':blg.blog_preview,'content':blg.blog_content,'date':blg.blog_time.strftime("%d %b"),'time':blg.blog_time.strftime( "%I:%M %p"),'user':blg.user.username,'image':blg.blog_img,'likes':l,'dislikes':dl,'comments':cmnt})
        totalpost=Blogs.query.filter_by(user_id=chk.id).count()
        return {'username':chk.username, 'totalpost':totalpost, 'followers':followers,'following':following,'fullname':chk.fullname,'about':chk.about,'profile_pic':chk.profile_img,'blogs':blogs}


search_req = reqparse.RequestParser()

search_req.add_argument('username',  help="username")
class SearchAPI(Resource):
    def post (self):
        args = search_req.parse_args()
        # fullname = args.get("email")
        username = args.get("username")
        data=[]
        if username:
            q='%'+username+'%'
            users=Users.query.filter(Users.username.like(q)).all()
            print (users)
            for user in users:
                data.append({'username':user.username})
        # if fullname:
        #     q='%'+fullname+'%'
        #     users=Users.query.filter(Users.fullname.like(q)).all()
        #     for user in users:
        #         data[user]={'username':user.username}
        print(data)
        return {'users':data}
    

follow_req = reqparse.RequestParser()
follow_req.add_argument('follower',  help="username")
follow_req.add_argument('following',  help="username")
class FollowAPI(Resource):
    @auth_required('token')
    # @marshal_with(fl_fields)
    def post(self):
        args = follow_req.parse_args()
        follower = args.get("follower")
        following=args.get("following")
        flwr=Users.query.filter_by(username=follower).first()
        fl=Users.query.filter_by(username=following).first()
        print(follower,following)
        fc=Follow.query.filter_by(followed_id=fl.id,follower_id=flwr.id).first()
        if fc:
            # flash('You already follow this user!!',category='danger')
            return {'response':'you already follow the user'},400
        else:
            f=Follow(followed_id=fl.id,follower_id=flwr.id)
            db.session.add(f)
            db.session.commit()
            # flash('followed!!',category='success')
            return {'response':'followed!!'},200
        

unfollow_req = reqparse.RequestParser()
unfollow_req.add_argument('follower',  help="username")
unfollow_req.add_argument('unfollowing',  help="username")
class UnfollowAPI(Resource):
    @auth_required('token')
    # @marshal_with(fl_fields)
    def post(self):
        args = unfollow_req.parse_args()
        follower = args.get("follower")
        unfollowing=args.get("unfollowing")
        flwr=Users.query.filter_by(username=follower).first()
        unfl=Users.query.filter_by(username=unfollowing).first()
        print(follower,unfollowing)
        fc=Follow.query.filter_by(followed_id=unfl.id,follower_id=flwr.id).first()
        if fc:
            # flash('You already follow this user!!',category='danger')
            Follow.query.filter_by(followed_id=unfl.id,follower_id=flwr.id).delete()
            db.session.commit()
            return {'response':'unfollowed'},200
        else:
            # f=Follow(followed_id=unfollowing,follower_id=follower)
            # db.session.add(f)
            # db.session.commit()
            # flash('followed!!',category='success')
            return {'response':'you are not following the user!!'},400
        
luk_req = reqparse.RequestParser()
# search_req.add_argument('fullname',  help="fullname")
luk_req.add_argument('like',  help="username")
luk_req.add_argument('blog',  help="username")
luk_req.add_argument('username',  help="username")

class LikeUnlikeAPI(Resource):
    @auth_required('token')
    def post (self):
        args = luk_req.parse_args()
        like =args.get('like')
        user = args.get("username")
        blog=args.get("blog")
        print(like,user,blog)
        # print(type(like))
        # print(like==True)
        # print(like=='False')
        if like=='True':
            l=Likes.query.filter_by(blog_id=blog,user_id=current_user.id).first()
            dl=Dislikes.query.filter_by(blog_id=blog,user_id=current_user.id).first()
            if l:
                return{'like':'done'}
            if dl:
                Dislikes.query.filter_by(blog_id=blog,user_id=current_user.id).delete()
                nl=Likes(blog_id=blog,user_id=current_user.id)
                db.session.add(nl)
                db.session.commit()
            else:
                nl=Likes(blog_id=blog,user_id=current_user.id)
                db.session.add(nl)
                db.session.commit()
        elif like=='False':
            l=Likes.query.filter_by(blog_id=blog,user_id=current_user.id).first()
            dl=Dislikes.query.filter_by(blog_id=blog,user_id=current_user.id).first()
            if dl:
                return{'dislike':'done'}
            if l:
                Likes.query.filter_by(blog_id=blog,user_id=current_user.id).delete()
                nl=Dislikes(blog_id=blog,user_id=current_user.id)
                db.session.add(nl)
                db.session.commit()
            else:
                nl=Dislikes(blog_id=blog,user_id=current_user.id)
                db.session.add(nl)
                db.session.commit()



cmnt_req = reqparse.RequestParser()
# search_req.add_argument('fullname',  help="fullname")
cmnt_req.add_argument('cmnt',  help="username")
# cmnt_req.add_argument('blog',  help="username")
cmnt_req.add_argument('user',  help="username")
class CommentAPI(Resource):
    @cache.memoize(timeout=10)
    @auth_required('token')
    def get(self,id):
        comments=[]
        cmnts=Comments.query.filter_by(blog_id=id).order_by(Comments.comment_time.desc()).all()
        for cmnt in cmnts:
            usr=Users.query.filter_by(id=cmnt.user_id).first()
            comments.append({'comment':cmnt.comment,'username':usr.username,'id':cmnt.id,'date':cmnt.comment_time.strftime("%d %b"),'time':cmnt.comment_time.strftime( "%I:%M %p")})
        return{'comments':comments}

    @auth_required('token')
    def post (self,id):
        args = cmnt_req.parse_args()
        cmnt =args.get('cmnt')
        user = args.get("user")
        c=Comments(blog_id=id,user_id=current_user.id,comment=cmnt,comment_time=datetime.now())
        db.session.add(c)
        db.session.commit()
        return{'cmnt':'comment-done'}
    
    @auth_required('token')
    def delete(self,id):
        Comments.query.filter_by(id=id).delete()
        db.session.commit()


class ExportblogAPI(Resource):
    @auth_required('token')
    def get(self):
            blgs=Blogs.query.filter_by(user_id=current_user.id).all()
            if(blgs):
                cnt = 0  
                bl = []
                for blg in blgs:
                    cnt+=1
                    bl.append({"SNo":cnt ,"Blog_title":blg.blog_title,"Blog_preview":blg.blog_preview,'Blog_content':blg.blog_content, "Last_modified": str(blg.blog_time)})

                List_exp = tasks.export_blog.delay(bl, current_user.username, current_user.email)
                return jsonify("Blogs Exported")
            else:
                return jsonify(" No Blogs to Export"),400
                # raise Exception("No Blogs to export")
            # with open('backend/application/static/lists_info.csv', 'w', encoding='utf8', newline='') as f:
            #     file = csv.DictWriter(f,fieldnames=l[0].keys(),restval='')
            #     file.writeheader()
            #     file.writerows(l)
            
        # except:
        #     return jsonify("Couldn't export")






