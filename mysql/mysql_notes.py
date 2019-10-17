"""
    mysql 查询死锁步骤:

    1、查询是否锁表 show OPEN TABLES where In_use > 0;

    2、查询进程

        show processlist   查询到相对应的进程===然后 kill    id

    补充：

    查看正在锁的事务

    SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCKS;



    查看等待锁的事务

    SELECT * FROM INFORMATION_SCHEMA.INNODB_LOCK_WAITS;

"""

"""
    mysql where 与 having 的区别:
    where 作用与 表和视图， 用来控制进入聚集函数的行。where 子句中不包含聚集函数。
    having 在分组和聚集函数后选取行。
    
    group by: 
        当 聚集函数在 select 中时，先执行 group by, 在执行聚集函数。
"""
