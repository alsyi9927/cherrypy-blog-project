# -*- coding: utf-8 -*-
import cherrypy
import psycopg2
import hashlib

from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('.'))


CP_CONF = {
    '/css': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static/css',
        'tools.staticdir.root': '/opt/python-project2'
    },

    '/js': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'static/js',
        'tools.staticdir.root': '/opt/python-project2'
    }

}

# PostgreSQL 연결 설정
db_config = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'nb1234',
    'host': '192.168.56.101',
    'port': '5432'
}

# 데이터베이스 연결 함수
def db_connect():
    conn = psycopg2.connect(**db_config)
    return conn

class BlogApp:
    # 로그인 전 홈 화면 로그인 화면으로 연결
    @cherrypy.expose
    def index(self):
        raise cherrypy.HTTPRedirect('/login')

    # 회원가입 페이지
    @cherrypy.expose
    def signup(self):
        return open('./templates/signup.html', encoding="UTF-8")

    # 회원가입 처리
    @cherrypy.expose
    def register(self, username, password):
        conn = db_connect()
        cursor = conn.cursor()
        # 비밀번호를 MD5를 사용하여 해싱
        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        conn.close()
        return "Registration successful. You can now <a href='/login'>login</a>."

    # 로그인 페이지
    @cherrypy.expose
    def login(self):
        return open('./templates/login.html', encoding="UTF-8")

    # 로그인 처리
    @cherrypy.expose
    def authenticate(self, username, password):
        conn = db_connect()
        cursor = conn.cursor()
        # username, password = kwargs.get("username"), kwargs.get('password', "")
        # print(f"username :{username}, password:{password}")
        cursor.execute("SELECT password FROM users WHERE username = %s", (username, ))
        stored_password = cursor.fetchone()
        conn.close()

        # MD5로 해싱된 비밀번호 비교
        if stored_password and hashlib.md5(password.encode('utf-8')).hexdigest() == stored_password[0]:
            cherrypy.session['username'] = username
            raise cherrypy.HTTPRedirect('/dashboard')
        else:
            return "Login failed. Please check your username and password."

    # 대시보드 페이지
    @cherrypy.expose 
    def dashboard(self):
        if 'username' in cherrypy.session:
            conn = db_connect()
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, username,content FROM boards")
            posts = cursor.fetchall()
            # print(posts)
            conn.close()
            tmpl = env.get_template('/templates/list.html')
            return tmpl.render(posts=posts)
        else:
            raise cherrypy.HTTPRedirect('/login')
                
    # 등록 페이지
    @cherrypy.expose
    def post(self):
        if 'username' in cherrypy.session:
            tmpl = env.get_template('/templates/post.html')
            username = cherrypy.session['username']
        
            return tmpl.render(username=username)
        else:
            raise cherrypy.HTTPRedirect('/login')
        
    # 등록 처리
    @cherrypy.expose
    def post_process(self, title, content):
        if 'username' in cherrypy.session:
            conn = db_connect()
            cursor = conn.cursor()
            username = cherrypy.session['username']
            cursor.execute("INSERT INTO boards (title, username, content) VALUES (%s, %s, %s)", (title, username, content))
            conn.commit()
            conn.close()
            raise cherrypy.HTTPRedirect('/dashboard')
        else:
            raise cherrypy.HTTPRedirect('/login')
    
    # 삭제 처리
    @cherrypy.expose
    def delete_post(self, id):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM boards WHERE id = %s", (id, ))
        user = cursor.fetchone()
        if cherrypy.session['username'] ==user[0]:
            cursor.execute("DELETE FROM boards WHERE id = %s", (id, ))
            conn.commit()
            conn.close()
        else: 
            cherrypy.response.status = 403
            
    # 세부사항 페이지
    @cherrypy.expose
    def detail(self, id):
        tmpl = env.get_template('/templates/detail.html')
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT title, content, username FROM boards WHERE id = %s", (id,))
        content = cursor.fetchone()
        return tmpl.render(username=content[2], title = content[0], content = content[1])
        
    # 수정 페이지
    @cherrypy.expose
    def edit(self, id):
        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM boards WHERE id = %s", (id, ))
        user = cursor.fetchone()
        if cherrypy.session['username'] ==user[0]:
            conn.close()
        else: 
            cherrypy.response.status = 403
            
    # 로그아웃
    @cherrypy.expose
    def logout(self):
        cherrypy.session.pop('username', None)
        raise cherrypy.HTTPRedirect('/login')

if __name__ == '__main__':
    cherrypy.config.update({"tools.sessions.on": True})
    
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8080})
    
    cherrypy.quickstart(BlogApp(), config=CP_CONF)

