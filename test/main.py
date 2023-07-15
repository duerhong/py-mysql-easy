from pymysqleasy import MysqlEasy

"""
Connect to the database
"""
conn = MysqlEasy(
    host="127.0.0.1",
    user="root",
    password="root",
    port=3306,
    database="fanyi"
)

def get_first_data():
    ret = conn.first(
        table_name="log",
        condition={
            "id": ["=", 1]
        },
        fields=['id', 'msg']
    )
    print(ret)


def get_multiple_data():
    ret = conn.get(
        table_name="log",
        condition={
            "id": [">", 1]
        },
        fields=['id', 'msg'],
        start=0,
        len=2
    )
    print(ret)


def get_all_data():
    ret = conn.get(
        table_name="log",
        fields=['id', 'msg']
    )
    print(ret)


def get_total():
    ret = conn.total(
        table_name="log"
    )
    print(ret)


def insert_data():
    """
    if return new data id,please use insertGetId
    """
    ret = conn.insert(
        table_name="log",
        data={
            "msg": "new data",
            "user_id": 1
        }
    )

def update_data():
    ret = conn.update(
        table_name="log",
        data={
            "msg": "new data 111"
        },
        condition={
            "id": ["=", 180]
        }
    )

def delete_data():
    ret = conn.delete(
        table_name="log",
        condition={
            "id": ["=", 180]
        }
    )
    print(ret)


"""
other methods
exex(sql)

group_total(table_name, fields, condition)
"""