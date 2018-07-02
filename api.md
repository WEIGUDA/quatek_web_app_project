## UserResource
### get
>`127.0.0.1:3000/user?job_name=00001`  
获取单个用户  

>`127.0.0.1:3000/user`  
获取所有用户  

>`127.0.0.1:3000/user?setoff=0&limit=5`  
按 setoff 和 limit 获取用户,`setoff` 和 `limit`无默认值

```
result

[
    {
        "category": 1,
        "created_time": "Fri, 22 Jun 2018 14:20:56 GMT",
        "department": "生产",
        "gender": "女",
        "hire_date": "2018/6/22",
        "job_number": "00001",
        "password": "2d17fd0487802e750e2788e459906740d0ce77e58e7fdbd122144a4ade848123",
        "telephone": "13812788888",
        "title": "职员",
        "train_state": "true",
        "username": "user1"
    },
    {
        "category": 1,
        "created_time": "Fri, 22 Jun 2018 14:21:12 GMT",
        "department": "生产",
        "gender": "男",
        "hire_date": "2018/6/22",
        "job_number": "00002",
        "password": "2d17fd0487802e750e2788e459906740d0ce77e58e7fdbd122144a4ade848123",
        "telephone": "13812788888",
        "title": "职员",
        "train_state": "false",
        "username": "user2"
    },
    {
        "category": 1,
        "created_time": "Fri, 22 Jun 2018 14:21:19 GMT",
        "department": "生产",
        "gender": "男",
        "hire_date": "2018/6/22",
        "job_number": "00003",
        "password": "2d17fd0487802e750e2788e459906740d0ce77e58e7fdbd122144a4ade848123",
        "telephone": "13812788888",
        "title": "职员",
        "train_state": "false",
        "username": "user3"
    },
    {
        "category": 1,
        "created_time": "Fri, 22 Jun 2018 14:21:23 GMT",
        "department": "生产",
        "gender": "男",
        "hire_date": "2018/6/22",
        "job_number": "00004",
        "password": "2d17fd0487802e750e2788e459906740d0ce77e58e7fdbd122144a4ade848123",
        "telephone": "13812788888",
        "title": "职员",
        "train_state": "false",
        "username": "user4"
    },
    {
        "category": 1,
        "created_time": "Fri, 22 Jun 2018 14:21:30 GMT",
        "department": "生产",
        "gender": "男",
        "hire_date": "2018/6/22",
        "job_number": "00005",
        "password": "2d17fd0487802e750e2788e459906740d0ce77e58e7fdbd122144a4ade848123",
        "telephone": "13812788888",
        "title": "职员",
        "train_state": "false",
        "username": "user5"
    }
]
```

### post

>`127.0.0.1:3000/user`

```
post example

{
	"username": "use1",
	"password": "user233",
	"category": "1",
	"job_number": "00001",
	"gender": "男",
	"telephone": "13812788888",
	"title": "职员",
	"department": "生产",
	"hire_date": "2018/6/22",
	"train_state": "false"
}
```
>添加用户名为`user1`,工号为`00001`的用户  
>工号`job_number `，必须要，不能省略

### patch
>`127.0.0.1:3000/user`

```
input json

{
	"job_number": "00001",
	"gender": "女",
	"train_state": "true"
}


```
>更新工号为`00001`的用户`性别`和`train_state`  
>`job_number ` 必须要，不能省略


### delete
>`127.0.0.1:3000/user?job_number=00001`  
删除工号为`00001`的用户



<br><br><br><br>

## MachineResource
### get
>`127.0.0.1:3000/gate/machine?machine_name=0001`  
获取单个机器  

>`127.0.0.1:3000/gate/machine`  
获取所有机器  

>`127.0.0.1:3000/gate/machine?setoff=0&limit=5`  
按 setoff 和 limit 获取机器，`setoff` 和 `limit` 无默认值

```
result

[
    {
        "created_time": "Fri, 29 Jun 2018 14:35:24 GMT",
        "foot_max": 80,
        "foot_min": 0,
        "hand_max": 80,
        "hand_min": 0,
        "machine_name": "machine1",
        "machine_number": "0001",
        "machine_type": "type1",
        "state": "true"
    },
    {
        "created_time": "Fri, 29 Jun 2018 14:35:31 GMT",
        "foot_max": 100,
        "foot_min": 0,
        "hand_max": 100,
        "hand_min": 0,
        "machine_name": "machine2",
        "machine_number": "0002",
        "machine_type": "type1",
        "state": "false"
    },
    {
        "created_time": "Fri, 29 Jun 2018 14:35:37 GMT",
        "foot_max": 100,
        "foot_min": 0,
        "hand_max": 100,
        "hand_min": 0,
        "machine_name": "machine3",
        "machine_number": "0003",
        "machine_type": "type1",
        "state": "false"
    },
    {
        "created_time": "Fri, 29 Jun 2018 14:35:41 GMT",
        "foot_max": 100,
        "foot_min": 0,
        "hand_max": 100,
        "hand_min": 0,
        "machine_name": "machine4",
        "machine_number": "0004",
        "machine_type": "type1",
        "state": "false"
    },
    {
        "created_time": "Fri, 29 Jun 2018 14:35:47 GMT",
        "foot_max": 100,
        "foot_min": 0,
        "hand_max": 100,
        "hand_min": 0,
        "machine_name": "machine5",
        "machine_number": "0005",
        "machine_type": "type1",
        "state": "false"
    }
]
```

### post
>`127.0.0.1:3000/gate/machine`

```
input json

{
	"machine_type": "type1",
	"machine_name": "machine1",
	"machine_number": "0001",
	"hand_max": "100",
	"hand_min": "0",
	"foot_max": "100",
	"foot_min": "0",
	"state": "false"
}


```
>添加机器编号为`0001`的闸机  
>`machine_number ` 必须要，不能省略

### patch
>`127.0.0.1:3000/gate/machine`

```
input json

{
	"machine_number": "0001",
	"hand_max": "80",
	"foot_min": "80",
	"state": "true"
}


```
>更新机器编号为`0001`的闸机`hand_max`,`foot_min`,`state`  
>`machine_number ` 必须要，不能省略


### delete
>`127.0.0.1:3000/gate/machine?machine_number=0001`  
删除机器编号为`0001`的闸机

<br><br><br><br>

## MachineTemplate
### get
>`127.0.0.1:3000/gate/machine/template?setoff=0&limit=5`  
按 setoff 和 limit 获闸机页面数据，`setoff`默认为0，`limit`默认为10

```
result

[
    {
        "foot_max": 80,
        "foot_min": 0,
        "hand_max": 80,
        "hand_min": 0,
        "machine_name": "machine1",
        "machine_number": "0001",
        "machine_type": "type1",
        "state": "true"
    },
    {
        "foot_max": 100,
        "foot_min": 0,
        "hand_max": 100,
        "hand_min": 0,
        "machine_name": "machine2",
        "machine_number": "0002",
        "machine_type": "type1",
        "state": "false"
    },
    {
        "foot_max": 100,
        "foot_min": 0,
        "hand_max": 100,
        "hand_min": 0,
        "machine_name": "machine3",
        "machine_number": "0003",
        "machine_type": "type1",
        "state": "false"
    },
    {
        "foot_max": 100,
        "foot_min": 0,
        "hand_max": 100,
        "hand_min": 0,
        "machine_name": "machine4",
        "machine_number": "0004",
        "machine_type": "type1",
        "state": "false"
    },
    {
        "foot_max": 100,
        "foot_min": 0,
        "hand_max": 100,
        "hand_min": 0,
        "machine_name": "machine5",
        "machine_number": "0005",
        "machine_type": "type1",
        "state": "false"
    }
]
```

<br><br><br><br>


## Static test

### get
>`127.0.0.1:3000/gate/static?job_number=00001`  
>获取某一用户的所有静电测试

>`127.0.0.1:3000/gate/static?job_number=00001&setoff=0&limit=5`  
>按 setoff 和 limit 获某一用户的静电测试，`setoff` 和 `limit` 无默认值

```
result

[
    {
        "created_time": "Sat, 30 Jun 2018 13:40:26 GMT",
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "machine_number": "0001",
        "right_foot": 90,
        "test_result": "false",
        "test_state": "true"
    },
    {
        "created_time": "Sat, 30 Jun 2018 13:41:05 GMT",
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "machine_number": "0001",
        "right_foot": 90,
        "test_result": "false",
        "test_state": "true"
    },
    {
        "created_time": "Sat, 30 Jun 2018 13:41:08 GMT",
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "machine_number": "0001",
        "right_foot": 90,
        "test_result": "false",
        "test_state": "true"
    },
    {
        "created_time": "Sat, 30 Jun 2018 13:41:09 GMT",
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "machine_number": "0001",
        "right_foot": 90,
        "test_result": "false",
        "test_state": "true"
    },
    {
        "created_time": "Sat, 30 Jun 2018 13:52:49 GMT",
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "machine_number": "0002",
        "right_foot": 90,
        "test_result": "false",
        "test_state": "true"
    }
]

```

###post

>`127.0.0.1:3000/gate/static`

```
post example

{
	"test_state": "true",
	"test_result": "false",
	"hand": "20",
	"left_foot": "80",
	"right_foot": "90",
	"job_number": "00001",
	"machine_number": "0001"
}
```
>添加工号为`00001`用户的静电测试  
>所有字段都要，不能省略

### patch
>`static_test`不能更新

### delete
>`127.0.0.1:3000/gate/static?job_number=00001`  
删除工号为`00001`用户的所有静电测试

<br><br><br><br>

## StaticTemplate
### get
>`127.0.0.1:3000/gate/static/template?setoff=0&limit=5`  
按 setoff 和 limit 获取静电测试页面数据，`setoff`默认为0，`limit`默认为10

```
result

[
    {
        "category": 3,
        "created_time": "Sat, 30 Jun 2018 13:40:26 GMT",
        "department": "生产",
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "machine_number": "0001",
        "right_foot": 90,
        "test_id": "1725f54c-7c28-11e8-a31d-3035add391b6",
        "test_result": "false",
        "test_state": "true",
        "username": "user1"
    },
    {
        "category": 3,
        "created_time": "Sat, 30 Jun 2018 13:41:05 GMT",
        "department": "生产",
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "machine_number": "0001",
        "right_foot": 90,
        "test_id": "2e821f88-7c28-11e8-92bf-3035add391b6",
        "test_result": "false",
        "test_state": "true",
        "username": "user1"
    },
    {
        "category": 3,
        "created_time": "Sat, 30 Jun 2018 13:41:08 GMT",
        "department": "生产",
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "machine_number": "0001",
        "right_foot": 90,
        "test_id": "303c648c-7c28-11e8-80f5-3035add391b6",
        "test_result": "false",
        "test_state": "true",
        "username": "user1"
    },
    {
        "category": 3,
        "created_time": "Sat, 30 Jun 2018 13:41:09 GMT",
        "department": "生产",
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "machine_number": "0001",
        "right_foot": 90,
        "test_id": "30b1b034-7c28-11e8-a56c-3035add391b6",
        "test_result": "false",
        "test_state": "true",
        "username": "user1"
    },
    {
        "category": 3,
        "created_time": "Sat, 30 Jun 2018 13:52:49 GMT",
        "department": "生产",
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "machine_number": "0002",
        "right_foot": 90,
        "test_id": "d2259826-7c29-11e8-8df3-3035add391b6",
        "test_result": "false",
        "test_state": "true",
        "username": "user1"
    }
]
```

<br><br><br><br>

## SearchStatic
### get
>`127.0.0.1:3000/gate/static/template/search?query=user1`  
按 `query` 获取静电测试页面数据，`query` 目前支持查询 `姓名`、`工号`、`机器号`、`部门`

```
result

[
    {
        "category": 3,
        "created_time": "Sat, 30 Jun 2018 13:40:26 GMT",
        "department": "生产",
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "machine_number": "0001",
        "right_foot": 90,
        "test_id": "1725f54c-7c28-11e8-a31d-3035add391b6",
        "test_result": "false",
        "test_state": "true",
        "username": "user1"
    },
    {
        "category": 3,
        "created_time": "Sat, 30 Jun 2018 13:41:05 GMT",
        "department": "生产",
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "machine_number": "0001",
        "right_foot": 90,
        "test_id": "2e821f88-7c28-11e8-92bf-3035add391b6",
        "test_result": "false",
        "test_state": "true",
        "username": "user1"
    },
    {
        "category": 3,
        "created_time": "Sat, 30 Jun 2018 13:41:08 GMT",
        "department": "生产",
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "machine_number": "0001",
        "right_foot": 90,
        "test_id": "303c648c-7c28-11e8-80f5-3035add391b6",
        "test_result": "false",
        "test_state": "true",
        "username": "user1"
    },
    {
        "category": 3,
        "created_time": "Sat, 30 Jun 2018 13:41:09 GMT",
        "department": "生产",
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "machine_number": "0001",
        "right_foot": 90,
        "test_id": "30b1b034-7c28-11e8-a56c-3035add391b6",
        "test_result": "false",
        "test_state": "true",
        "username": "user1"
    },
    {
        "category": 3,
        "created_time": "Sat, 30 Jun 2018 13:52:49 GMT",
        "department": "生产",
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "machine_number": "0002",
        "right_foot": 90,
        "test_id": "d2259826-7c29-11e8-8df3-3035add391b6",
        "test_result": "false",
        "test_state": "true",
        "username": "user1"
    }
]
```

<br><br><br><br>


## CardResource

### get
>`127.0.0.1:3000/gate/card?card_id=00001`  
获取单个卡片  

>`127.0.0.1:3000/gate/card`  
获取所有卡片  

>`127.0.0.1:3000/gate/card?setoff=0&limit=5`  
按 setoff 和 limit 获取卡片，`setoff` 和 `limit` 无默认值

```
result

[
    {
        "card_id": "00001",
        "category": 3,
        "created_time": "Fri, 29 Jun 2018 15:31:26 GMT",
        "job_number": "00001"
    },
    {
        "card_id": "00002",
        "category": 3,
        "created_time": "Fri, 29 Jun 2018 15:31:34 GMT",
        "job_number": "00002"
    },
    {
        "card_id": "00003",
        "category": 3,
        "created_time": "Fri, 29 Jun 2018 15:31:41 GMT",
        "job_number": "00003"
    },
    {
        "card_id": "00004",
        "category": 3,
        "created_time": "Mon, 02 Jul 2018 10:28:46 GMT",
        "job_number": "00004"
    },
    {
        "card_id": "00005",
        "category": 3,
        "created_time": "Mon, 02 Jul 2018 10:28:52 GMT",
        "job_number": "00005"
    }
]
```

### post
>`127.0.0.1:3000/gate/card`

```
input json

{
	"card_id": "00001",
	"category": "3",
	"job_number": "00001"
}


```
>添加卡号为`00001`的卡片  
>`card_id ` 必须要，不能省略

### patch
>`127.0.0.1:3000/gate/card`

```
input json

{
	"card_id": "00001",
	"category": "1"
}


```

>更新卡号为`00001`的`category`  
>`card_id ` 必须要，不能省略


### delete
>127.0.0.1:3000/gate/card?card_id=00001  
删除卡号为`00001`的卡片

<br><br><br><br>

## CardTemplate
### get
>`127.0.0.1:3000/gate/card/template?setoff=0&limit=5`  
按 setoff 和 limit 获取卡片页面数据，`setoff`默认为0，`limit`默认为10

```
result

[
    {
        "card_id": "00001",
        "category": 1,
        "department": "生产",
        "job_number": "00001",
        "username": "user1"
    },
    {
        "card_id": "00002",
        "category": 3,
        "department": "生产",
        "job_number": "00002",
        "username": "user2"
    },
    {
        "card_id": "00003",
        "category": 3,
        "department": "生产",
        "job_number": "00003",
        "username": "user3"
    },
    {
        "card_id": "00004",
        "category": 3,
        "department": "生产",
        "job_number": "00004",
        "username": "user4"
    },
    {
        "card_id": "00005",
        "category": 3,
        "department": "生产",
        "job_number": "00005",
        "username": "user5"
    }
]
```

<br><br><br><br>

## SearchCard
### get
>`127.0.0.1:3000/gate/card/template/search?query=user1`  
按 `query` 获取卡片页面数据，`query` 目前支持查询 `姓名`、`工号`、`卡号`、`部门`

```
result

[
    {
        "card_id": "00001",
        "category": 1,
        "department": "生产",
        "job_number": "00001",
        "username": "user1"
    }
]
```

<br><br><br><br>

## Attendance

### get
>`127.0.0.1:3000/gate/attendance?job_number=00001`  
>获取某一用户的所有考勤

>`127.0.0.1:3000/gate/static?job_number=00001&setoff=0&limit=5`  
>按 setoff 和 limit 获某一用户的考勤，`setoff` 和 `limit` 无默认值

```
result

[
    {
        "created_time": "Sat, 30 Jun 2018 14:25:41 GMT",
        "job_number": "00001",
        "machine_number": "0001",
        "state": "false",
        "working_time": "8"
    }
]

```

###post

>`127.0.0.1:3000/gate/attendance`

```
post example

{
	"state": "false",
	"working_time": "8",
	"job_number": "00001",
	"machine_number": "0001"
}
```
>添加工号为`00001`的考勤  
>所有字段都要，不能省略

### patch
>`attendance`不能更新

### delete
>`127.0.0.1:3000/gate/attendance?job_number=00001`  
删除工号为`00001`用户的所有考勤

<br><br><br><br>

## AttendanceTemplate
### get
>`127.0.0.1:3000/gate/attendance/template?setoff=0&limit=5`  
按 setoff 和 limit 获考勤页面数据，`setoff`默认为0，`limit`默认为10

```
result

[
    {
        "category": 1,
        "department": "生产",
        "job_number": "00001",
        "machine_number": "0001",
        "username": "user1",
        "working_time": "8"
    },
    {
        "category": 1,
        "department": "生产",
        "job_number": "00002",
        "machine_number": "0001",
        "username": "user2",
        "working_time": "8"
    },
    {
        "category": 1,
        "department": "生产",
        "job_number": "00003",
        "machine_number": "0001",
        "username": "user3",
        "working_time": "8"
    }
]
```