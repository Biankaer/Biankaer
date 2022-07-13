#   安装
pip install django
#创建项目
django-admin startproject **name**
#启动项目
python manage.py runserver --nothreading 172.17.19.26:8000
#创建应用
python manage.py startapp **name**不要用text
###django 模型
1.安装MySQL

2.在MySQL中创建库mydb
create database mydb default charset=utf8mb4;

3.修改当前数据库配置 settings.py/DATABASES

##定义模型
1.配置文件中定义
settings.py/INSTALLED_APPS

2.models.py中定义模型

3.生成迁移文件
python manage.py makemigrations

4.执行迁移
python manage.py migrate
class ahau(models.Model):
    title = models.TextField()
    url = models.TextField()
    text = models.TextField()
    ss_date = models.DateField()
    source = models.CharField(max_length=20)