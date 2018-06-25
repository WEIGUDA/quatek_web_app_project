## User
### get
>`127.0.0.1:3000/user?category=1&setoff=0&limit=10`

>`category ` 如果不填，默认1,也就是普通用户，`setoff` 如果不填，默认0, `limit` 如果不填，默认10

```
result

[
    {
        "category": "1",
        "department": "生产",
        "gender": "男",
        "hire_date": "2018/6/22",
        "job_number": "00001",
        "password": "2d17fd0487802e750e2788e459906740d0ce77e58e7fdbd122144a4ade848123",
        "telephone": "13812788888",
        "title": "职员",
        "train_state": "false",
        "username": "user1"
    },
    {
        "category": "1",
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
        "category": "1",
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
        "category": "1",
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
        "category": "1",
        "department": "生产",
        "gender": "男",
        "hire_date": "2018/6/22",
        "job_number": "00005",
        "password": "2d17fd0487802e750e2788e459906740d0ce77e58e7fdbd122144a4ade848123",
        "telephone": "13812788888",
        "title": "职员",
        "train_state": "false",
        "username": "user5"
    },
    {
        "category": "1",
        "department": "生产",
        "gender": "男",
        "hire_date": "2018/6/22",
        "job_number": "00006",
        "password": "2d17fd0487802e750e2788e459906740d0ce77e58e7fdbd122144a4ade848123",
        "telephone": "13812788888",
        "title": "职员",
        "train_state": "false",
        "username": "user6"
    },
    {
        "category": "1",
        "department": "生产",
        "gender": "男",
        "hire_date": "2018/6/22",
        "job_number": "00007",
        "password": "2d17fd0487802e750e2788e459906740d0ce77e58e7fdbd122144a4ade848123",
        "telephone": "13812788888",
        "title": "职员",
        "train_state": "false",
        "username": "user7"
    },
    {
        "category": "1",
        "department": "生产",
        "gender": "男",
        "hire_date": "2018/6/22",
        "job_number": "00008",
        "password": "2d17fd0487802e750e2788e459906740d0ce77e58e7fdbd122144a4ade848123",
        "telephone": "13812788888",
        "title": "职员",
        "train_state": "false",
        "username": "user8"
    },
    {
        "category": "1",
        "department": "生产",
        "gender": "男",
        "hire_date": "2018/6/22",
        "job_number": "00009",
        "password": "2d17fd0487802e750e2788e459906740d0ce77e58e7fdbd122144a4ade848123",
        "telephone": "13812788888",
        "title": "职员",
        "train_state": "false",
        "username": "user9"
    },
    {
        "category": "1",
        "department": "生产",
        "gender": "女",
        "hire_date": "2018/6/22",
        "job_number": "00010",
        "password": "2d17fd0487802e750e2788e459906740d0ce77e58e7fdbd122144a4ade848123",
        "telephone": "13812788888",
        "title": "职员",
        "train_state": "false",
        "username": "user10"
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
>`job_number `也就是工号，必须要，不能省略

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

>`job_number ` 必须要，不能省略


### delete
>127.0.0.1:3000/user?job_number=00001



<br><br><br><br>

## Machine
### get
>`127.0.0.1:3000/gate/machine?machine_type=type1&setoff=0&limit=10`
>`setoff` 如果不填，默认0, `limit` 如果不填，默认10

```
result

[
    {
        "foot_lower": 0,
        "foot_upper": 80,
        "hand_lower": 0,
        "hand_upper": 80,
        "machine_name": "machine1",
        "machine_number": "0001",
        "machine_type": "type1",
        "state": "false"
    },
    {
        "foot_lower": 0,
        "foot_upper": 80,
        "hand_lower": 0,
        "hand_upper": 80,
        "machine_name": "machine2",
        "machine_number": "0002",
        "machine_type": "type1",
        "state": "false"
    },
    {
        "foot_lower": 0,
        "foot_upper": 80,
        "hand_lower": 0,
        "hand_upper": 80,
        "machine_name": "machine3",
        "machine_number": "0003",
        "machine_type": "type1",
        "state": "false"
    },
    {
        "foot_lower": 0,
        "foot_upper": 100,
        "hand_lower": 0,
        "hand_upper": 100,
        "machine_name": "machine4",
        "machine_number": "0004",
        "machine_type": "type1",
        "state": "false"
    },
    {
        "foot_lower": 0,
        "foot_upper": 100,
        "hand_lower": 0,
        "hand_upper": 100,
        "machine_name": "machine5",
        "machine_number": "0005",
        "machine_type": "type1",
        "state": "false"
    },
    {
        "foot_lower": 0,
        "foot_upper": 100,
        "hand_lower": 0,
        "hand_upper": 100,
        "machine_name": "machine6",
        "machine_number": "0006",
        "machine_type": "type1",
        "state": "false"
    },
    {
        "foot_lower": 0,
        "foot_upper": 100,
        "hand_lower": 0,
        "hand_upper": 100,
        "machine_name": "machine7",
        "machine_number": "0007",
        "machine_type": "type1",
        "state": "false"
    },
    {
        "foot_lower": 0,
        "foot_upper": 100,
        "hand_lower": 0,
        "hand_upper": 100,
        "machine_name": "machine8",
        "machine_number": "0008",
        "machine_type": "type1",
        "state": "false"
    },
    {
        "foot_lower": 0,
        "foot_upper": 100,
        "hand_lower": 0,
        "hand_upper": 100,
        "machine_name": "machine9",
        "machine_number": "0009",
        "machine_type": "type1",
        "state": "false"
    },
    {
        "foot_lower": 0,
        "foot_upper": 100,
        "hand_lower": 0,
        "hand_upper": 100,
        "machine_name": "machine10",
        "machine_number": "0010",
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
	"hand_upper": "100",
	"hand_lower": "0",
	"foot_upper": "100",
	"foot_lower": "0",
	"state": "false"
}


```
>`machine_number ` 必须要，不能省略

### patch
>`127.0.0.1:3000/gate/machine`

```
input json

{
	"machine_number": "0001",
	"hand_upper": "80",
	"foot_upper": "80",
	"state": "true"
}


```

>`machine_number ` 必须要，不能省略


### delete
>127.0.0.1:3000/gate/machine?machine_number=0001



<br><br><br><br>


## Static test

### get

>`127.0.0.1:3000/gate/static_test?job_number=00001&setoff=0&limit=10`

>`setoff` 如果不填，默认0, `limit` 如果不填，默认10

```
result

[
    {
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "right_foot": 90,
        "test_result": "false",
        "test_state": "true"
    },
    {
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "right_foot": 90,
        "test_result": "false",
        "test_state": "true"
    },
    {
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "right_foot": 90,
        "test_result": "false",
        "test_state": "true"
    },
    {
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "right_foot": 90,
        "test_result": "false",
        "test_state": "true"
    },
    {
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "right_foot": 90,
        "test_result": "false",
        "test_state": "true"
    },
    {
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "right_foot": 90,
        "test_result": "false",
        "test_state": "true"
    },
    {
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "right_foot": 90,
        "test_result": "false",
        "test_state": "true"
    },
    {
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "right_foot": 90,
        "test_result": "false",
        "test_state": "true"
    },
    {
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "right_foot": 90,
        "test_result": "false",
        "test_state": "true"
    },
    {
        "hand": 20,
        "job_number": "00001",
        "left_foot": 80,
        "right_foot": 90,
        "test_result": "false",
        "test_state": "true"
    }
]

```

###post

>`127.0.0.1:3000/gate/static_test`

```
post example

{
	"test_state": "true",
	"test_result": "false",
	"hand": "20",
	"left_foot": "80",
	"right_foot": "90",
	"job_number": "00001"
}
```
>所有字段都要，不能省略

### patch
>`static_test`暂时不能更新

### delete
>`static_test`暂时不能删除

<br><br><br><br>


## Card

```

post example
{
	"card_id": "00001",
	"category": "3",
	"job_number": "00001",
	"department": "生产"
}
```
### get
>`127.0.0.1:3000/gate/card?dapartment=生产&setoff=0&limit=10`

>获得某一部门的所有卡片
>`setoff` 如果不填，默认0, `limit` 如果不填，默认10

```
result

[
    {
        "card_id": "00001",
        "category": 3,
        "department": "生产",
        "job_number": "00001"
    },
    {
        "card_id": "00002",
        "category": 3,
        "department": "生产",
        "job_number": "00001"
    },
    {
        "card_id": "00003",
        "category": 3,
        "department": "生产",
        "job_number": "00001"
    },
    {
        "card_id": "00004",
        "category": 3,
        "department": "生产",
        "job_number": "00001"
    },
    {
        "card_id": "00005",
        "category": 3,
        "department": "生产",
        "job_number": "00001"
    },
    {
        "card_id": "00006",
        "category": 3,
        "department": "生产",
        "job_number": "00001"
    },
    {
        "card_id": "00007",
        "category": 3,
        "department": "生产",
        "job_number": "00001"
    },
    {
        "card_id": "00008",
        "category": 3,
        "department": "生产",
        "job_number": "00001"
    },
    {
        "card_id": "00009",
        "category": 3,
        "department": "生产",
        "job_number": "00001"
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
	"job_number": "00001",
	"department": "生产"
}


```
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

>`card_id ` 必须要，不能省略


### delete
>127.0.0.1:3000/gate/card?card_id=00001

<br><br><br><br>



## Attendance

### get

>`127.0.0.1:3000/gate/attendance?job_number=00001&setoff=0&limit=10`

>`setoff` 如果不填，默认0, `limit` 如果不填，默认10

```
result

[
    {
        "job_number": "00001",
        "state": "false",
        "working_time": "8"
    },
    {
        "job_number": "00001",
        "state": "false",
        "working_time": "8"
    },
    {
        "job_number": "00001",
        "state": "false",
        "working_time": "8"
    },
    {
        "job_number": "00001",
        "state": "false",
        "working_time": "8"
    },
    {
        "job_number": "00001",
        "state": "false",
        "working_time": "8"
    },
    {
        "job_number": "00001",
        "state": "false",
        "working_time": "8"
    },
    {
        "job_number": "00001",
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
	"job_number": "00001"
}
```
>所有字段都要，不能省略

### patch
>`static_test`暂时不能更新

### delete
>`static_test`暂时不能删除