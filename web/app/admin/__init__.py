from flask import url_for,redirect,abort
from flask_admin import BaseView, expose, AdminIndexView
from flask_login import login_required, current_user
from flask_admin.contrib.sqla import ModelView #数据库模型
from flask_admin.contrib.fileadmin import FileAdmin #文件管理
from os import path,pardir

basepath = path.abspath(path.join(path.dirname(__file__),pardir,pardir,'upload')) #路径



# 默认的主页视图
class MyHomeView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        print('调用了MyHomeView')
        arg1 = '周和'
        return self.render('admin/myhome.html', arg1=arg1)


# 基础视图一般用于添加一些统计表单
class MyView(BaseView):
    # 新增视图的默认页面
    @expose('/')
    @login_required
    def index(self):
        # 路由的用法和renter_template一样
        return self.render('admin/myview.html')

    # 生成url
    @expose('/test')
    @login_required
    def test(self):
        return self.render('admin/test.html')


# 模型视图
class MyUserModel(ModelView):

    #重写判断是否登录,登录会返回True
    def is_accessible(self):
        return current_user.is_authenticated

    #如果is_accessible是False没有登录就会执行下面代码
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))

    # 重写标签字典
    column_labels = {
        "id": "ID",
        "username": "帐号",
        "password": "密码",
        "email": "邮箱",
        "posts": "文章关联"
    }
    # 重写显示列表
    column_list = ('id', 'username', 'password', 'email')
    # 重写可搜索字段
    column_searchable_list = ('username', 'id')


class MyPostModel(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))

    column_labels = {
        "id": "ID",
        "title": "标题",
        "tag": "标签",
        "body": "文章",
        "body_html": "MarkDown",
        "created": "创建时间",
        "author_id": "发表用户",
        "comments": "关联评论",
        "author": "创建用户"
    }
    column_list = ("id", "tag","title", "body", "body_html", "created")
    column_searchable_list = ('title', 'id')


class MyCommentModel(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))

    column_labels = {
        "id": "ID",
        "body": "评论",
        "created": "创建时间",
        "POST": "关联文章"
    }
    column_list = ("id", "body", "created")
    column_searchable_list = ('body', 'id')

class MyTagModel(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))

    column_labels = {
        "id": "ID",
        "title":"标签"
    }
    column_list = ("id","title")
    column_searchable_list = ("id","title")

class MyFile(FileAdmin):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("auth.login"))