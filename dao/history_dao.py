import config
from datetime_tool import get_now_time
from util.common.sqlite_tool import SqliteTemplate


def get_sqlite():
    return SqliteTemplate(config.database)


def create_table():
    # 建表语句
    sql = "create table if not exists history(" \
          "id integer primary key autoincrement," \
          "content text not null," \
          "createtime text not null," \
          "imgurl text not null" \
          ");"
    print(sql)
    sqlite = get_sqlite()
    sqlite.create_table(sql)
    sqlite.close()


def select_all():
    # 查询语句
    sql = "select * from history order by createtime desc;"
    print(sql)
    sqlite = get_sqlite()
    result = sqlite.select(sql)
    sqlite.close()
    return result


def insert_history(content: str, img_url: str):
    # 查询语句
    sql = "insert into history values(NULL, ?, ?,?);"
    print(sql)
    sqlite = get_sqlite()
    sqlite.insert(sql, [content, str(get_now_time()), img_url])
    sqlite.close()


def get_item_imgurl(id: int):
    sql = "select imgurl from history where id = %s;" % id
    print(sql)
    sqlite = get_sqlite()
    result = sqlite.select(sql)
    sqlite.close()
    return result[0][0]


def remove_history(id: int):
    sql = "delete from history where id = %s;" % id
    print(sql)
    sqlite = get_sqlite()
    sqlite.delete(sql)
    sqlite.close()


def remove_all():
    sql = "delete from history;"
    sqlite = get_sqlite()
    sqlite.insert(sql, id)
    sqlite.close()


if __name__ == '__main__':
    # create_table()
    print(get_item_imgurl(71))
