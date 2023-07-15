# Install 
pip install pymysqleasy

# first
```
from pymysqleasy import MysqlEasy

conn = MysqlEasy(
    host="127.0.0.1",
    user="xxx",
    password="xxx",
    port=3306,
    database="test"
)
ret = conn.first(table_name="user",condition={
    "id": ["=", "1"]
})
print(ret)

```