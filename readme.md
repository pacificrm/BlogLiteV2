# Local Setup

- Run `pip install -r requirements.txt` to install all dependencies written in `requirements.txt` which is inside `backend` folder

# Local Development Run

- `python3 app.py` It will start the flask app in `development`. This is for running app on local system.
- `npm run serve` for serving the app from frontend on Vue

# Folder Structure of `backend`

- `project.sqlite3` is the sqlite database. It can be anywhere on the machine, just the adjustment in the path in `app.py` is required. One of the database is shipped for testing.
- The application code for my app is `/`
- `templates` is the default folder where templates are stored which is used for sending mails.
- `application` contains the `api`, `cache.py`, `clry.py`, `emailgen.py`, `models.py`, `tasks.py` and `static` folder.
- `static` a folder in which we have `IMG` folder which has images used in the app. Also the graphs generated are saved in it which is further encoded to send to frontend and decoded over there.
- `Project Documentation` having a brief description about app
- A `readme` file and `requirements` file

# Folder Structure of `frontend`

- `node_modules` required for running VueJS CLI
- `public` having public components
- `src` is the default folder where frontend components and routers are located.
- `components` which has vue components for frontend, `router` which contains `index.js` for defining different routes, `App.vue` the page on which app is being served, `index.js` for app start and `store` to create the store for vue.
- A `readme` file and other required configurations.

```
mad2-project
├── backend
|   ├── app.py
|   ├── api.py
|   ├── cache.py
|   ├── cachingdata.py
|   ├── clery.py
|   ├── database.sqlite3
|   ├── emailgenr.py
|   ├── models.py
|   ├── tasks.py
|   ├── templates
|   |       ├── blogs_csv.html
|   |       ├── daily_reminder.html
|   |       └── monthly_report.html
|   └── Static
|
├── frontend/
│   ├── public
|   ├──src
|   |    ├── assets
|   |    |      ├── Blogs
|   |    |      └── Profile
|   |    ├── components
|   |    |      ├── CommentBlog.vue
|   |    |      ├── EditBlog.vue
|   |    |      ├── EditProfile.vue
|   |    |      ├── LoginSignup.vue
|   |    |      ├── MyFollowers.vue
|   |    |      ├── MyFollowing.vue
|   |    |      ├── NavBar.vue
|   |    |      ├── PostBlog.vue
|   |    |      ├── PostEngage.vue
|   |    |      ├── ReadBlog.vue
|   |    |      ├── SPage.vue
|   |    |      ├── StartPage.vue
|   |    |      └── UserProfile.vue
|   |    ├── router/index.js
|   |    ├── store/inex.js
|   |    ├── App.vue
|   |    └── main.js
|   ├── .gitignore
|   ├── babel.config.js
|   ├── jsconfig.json
|   ├── package-lock.json
|   ├── package.json
|   ├── README.md
|   └── vue.config.js
├── Bloglite.yaml
├── requirements.txt
├── Project_Report_ BLOG-LITEV2.pdf
└── readme.md

```
