import config
from util.date_tool import get_datetime
from util.sqlite_tool import SqliteTemplate


def get_sqlite():
    return SqliteTemplate(config.database)


# 插入语句
insert_sql = "insert into history values(NULL, ?, ?,?);"
# 查询语句
select_sql = "select * from history;"
# 通过id查询
select_id_sql = "select * from history where id = ?;"
# 通过时间查询
select_time_sql = "select * from history where createtime > ? and createtime < ?;"
# 删除表中全部数据
delete_all_sql = "delete * from history;"
# 通过id删除记录
delete_id_sql = "delete from history where id = ?;"


def create_table():
    # 建表语句
    sql = "create table if not exists history(" \
          "id integer primary key autoincrement," \
          "content text not null," \
          "createtime text not null," \
          "imgurl text not null" \
          ");"
    sqlite = get_sqlite()
    sqlite.create_table(sql)
    sqlite.close()


def select_all():
    # 查询语句
    sql = "select * from history order by createtime desc;"
    sqlite = get_sqlite()
    result = sqlite.select(sql)
    sqlite.close()
    return result


def insert_history(content: str, img_url: str):
    # 查询语句
    sql = "insert into history values(NULL, ?, ?,?);"
    sqlite = get_sqlite()
    sqlite.insert(sql, [content, str(get_datetime()), img_url])
    sqlite.close()


def remove_history(id):
    sql = "delete from history where id = ?;"
    sqlite = get_sqlite()
    sqlite.delete(sql, [id])
    sqlite.close()


def remove_all():
    sql = "delete from history;"
    sqlite = get_sqlite()
    sqlite.insert(sql, id)
    sqlite.close()

if __name__ == '__main__':
    create_table()

class HistoryTemplate(SqliteTemplate):
    # 调用父类构造器，连接数据库
    def __init__(self, db_name):
        super(HistoryTemplate, self).__init__(db_name)

    # 关闭数据库
    def Close(self):
        super(HistoryTemplate, self).close()

    # 向数据库中插入一条记录
    def Insert_History(self, history):
        super(HistoryTemplate, self).insert(insert_sql, history)

    # 查询表中所有数据
    def Select_History(self):
        results = super(HistoryTemplate, self).select(select_sql)
        return results

    # 按照id查询表中数据
    def Select_Id_History(self, id):
        result = super(HistoryTemplate, self).select(select_id_sql, id)
        return result

    # 按照开始截止时间查询表中数据
    def Select_Time_History(self, start_time, end_time):
        results = super(HistoryTemplate, self).select(select_time_sql, start_time, end_time)
        return results

    # 按照id删除表中记录
    def Delete_Id_History(self, id):
        super(HistoryTemplate, self).delete(delete_id_sql, id)

    # 删除全部表中数据
    def Delete_All_History(self):
        super(HistoryTemplate, self).delete(delete_id_sql)
