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

"""
    mysql 表锁与行锁:
    InnoDB的行锁模式及加锁方法
    InnoDB实现了以下两种类型的行锁。
    共享锁（S）：允许一个事务去读一行，阻止其他事务获得相同数据集的排他锁。
    排他锁（X)：允许获得排他锁的事务更新数据，阻止其他事务取得相同数据集的共享读锁和排他写锁。另外，为了允许行锁和表锁共存，实现多粒度锁机制，
    InnoDB还有两种内部使用的意向锁（Intention Locks），这两种意向锁都是表锁。
    意向共享锁（IS）：事务打算给数据行加行共享锁，事务在给一个数据行加共享锁前必须先取得该表的IS锁。
    意向排他锁（IX）：事务打算给数据行加行排他锁，事务在给一个数据行加排他锁前必须先取得该表的IX锁。
    上述锁模式的兼容情况具体如下表所示。
                                             InnoDB行锁模式兼容性列表
    请求锁模式
       是否兼容
    当前锁模式
        X	IX	S	IS
    X	冲突	冲突	冲突	冲突
    IX	冲突	兼容	冲突	兼容
    S	冲突	冲突	兼容	兼容
    IS	冲突	兼容	兼容	兼容
"""
