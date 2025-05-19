import pymysql
def change_dept(dept_id):
    coon = pymysql.connect(host='localhost', user='root', password='wang2003', db='company')
    cursor = coon.cursor()
    sql = "UPDATE departments_department SET dept_manager_id = null WHERE dept_id = %s"%dept_id
    cursor.execute(sql)
    coon.commit()
    coon.close()
