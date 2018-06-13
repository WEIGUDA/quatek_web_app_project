## 定义数据模型

```
class User(db.Document):
	 # 集合名称 user
    meta = {
        'collection': 'user'
    }
    username = db.StringField()
    password = db.StringField()
    created_time = db.DateTimeField(default=datetime.now)

```

## 查询数据
```
查询所有数据
users = User.objects().all()
查询满足条件的数据
user1 = User.objects(name="chandler").first()
```

## 添加数据
```
user1 = User(name='quatek', is_completed=False)
user1.save()
```

## 数据排序
```
users = User.objects().order_by('created_time')

```

## 更新数据
```
user1 = User.objects(name="chandler").first()
user1.update(password="chandler123", is_completed=True)
```

## 删除数据
```
user1 = User.objects(name="chandler").first()
user1.delete()
```

## 分页
```
def view_users(page=1):
    users = User.objects.paginate(page=page, per_page=10)
```