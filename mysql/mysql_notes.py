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
