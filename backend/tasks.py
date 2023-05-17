from clery import celery
from jinja2 import Template
from weasyprint import HTML
import csv
import os
from emailgenr import send_email
from models import db,Users,Blogs,Follow,Comments,Likes,Dislikes

def format_report(template1,data,User="User"):
    with open(template1) as file:
        temp = Template(file.read())
        return temp.render(blgs=data,user=User)


def pdf_report(d,User):
    msg = format_report("./templates/monthly_report.html",data=d,User=User)
    html = HTML(string=msg)
    file_name = str(User)+"_BlogLite"+".pdf"
    print(file_name)
    html.write_pdf(target=file_name)

wrkng_dir = os.path.abspath(os.path.dirname(__file__))
path_s = os.path.join(wrkng_dir, "static/")
path_t = os.path.join(wrkng_dir, "templates/")



@celery.task()
def export_blog(bl, username, email):
        with open(path_s+'blogs_info_'+username+'.csv', 'w', encoding='utf8', newline='') as f:
            file = csv.DictWriter(f,fieldnames=bl[0].keys(),restval='')
            file.writeheader()
            file.writerows(bl)
        # filename=path_s+'blogs_info_'+username+'.csv'
        # send_email(to_address=email, subject="Status of your Download Card Your download has been successfully completed card.",
        #            attachment=filename)
        
        with open(path_t+'blogs_csv.html','r') as f:
            template = Template(f.read())
        send_email(to_address=email,subject='Exported List Details',message=template.render(user=username,data=bl),content="html",attachment=path_s+'blogs_info_'+username+'.csv')
        # send_email(to_address=email,subject='Exported Blogs Details',message="This is the all blog you posted till now.",attachment=path_s+'blogs_info_'+username+'.csv')    
        return "Csv created."
    # except:
    #     send_email(email, "Status of your Download Card",
    #                "The card id you specified does not exist, therefore we have not attached the CSV file.")


@celery.task()
def daily_reminder():
    user_details =Users.query.all()
    for u in user_details :
        email = u.email
        usr = Users.query.filter_by(email = u.email).first()
        username = usr.username
        
        blgs = Blogs.query.filter_by(user_id=u.id)
        cd=[]
        for blg in blgs:
            cd.append({"blog_id":blg.id ,"blog_title":blg.blog_title,"blog_preview":blg.blog_preview,'blog_content':blg.blog_content, "last_modified": str(blg.blog_time)})
            
        with open(path_t+'daily_reminder.html','r') as f:
            template = Template(f.read())
        send_email(email,'Daily Reminder',template.render(user=username,  blgs=cd),content="html")

@celery.task()
def monthly_reminder():
    user_details =Users.query.all()
    user_email_list =[]
    data =[]
    u_list =[]
    
    for u in user_details :
        user_email_list.append(u.email)
        user = Users.query.filter_by(email = u.email).first()
        username = user.username
        u_list.append(username)
        blgs = Blogs.query.filter_by(user_id=u.id).all()
        details = []
        count=0
        for blg in blgs:
            count+=1
            details.append({"SNo":count ,"blog_title":blg.blog_title,"blog_preview":blg.blog_preview,'blog_content':blg.blog_content, "last_modified": str(blg.blog_time)})
        pdf_report(details,username)
        with open(path_t+'monthly_report.html','r') as f:
            template = Template(f.read())
        send_email(u.email,'Monthly Report',template.render(user=username,blgs=details),content="html",attachment="./"+str(username)+"_BlogLite.pdf")    
    # data.append(details)

