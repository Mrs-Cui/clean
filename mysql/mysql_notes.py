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

"""
B-树与B+树:
    
    B-树满足的特性(m 阶B-树):
        1.每个结点最多 m 个子结点。 
        2.除了根结点和叶子结点外，每个结点最少有 m/2（向上取整）个子结点。         
        3.如果根结点不是叶子结点，那根结点至少包含两个子结点。         
        4.所有的叶子结点都位于同一层。        
        5.每个结点都包含 k 个元素（关键字），这里 m/2≤k。      
        6.每个节点中的元素（关键字）从小到大排列。       
        7.每个元素（关键字）字左结点的值，都小于或等于该元素（关键字）。右结点的值都大于或等于该元素（关键字）。
        
    如果数据库已B-树为索引:
        数据结构为: b-tree.webp(如图)
        
    B+树是在B-树上的优化，满足特性:
        1.所有的非叶子节点只存储关键字信息。 
        2.所有卫星数据（具体数据）都存在叶子结点中。       
        3.所有的叶子结点中包含了全部元素的信息。         
        4.所有叶子节点之间都有一个链指针。
    如果数据库已B+树为索引:
        数据结构为: b+tree.webp(如图)
    B-Tree 和 B+Tree 该如何选择呢？都有哪些优劣呢？
        ①B-Tree 因为非叶子结点也保存具体数据，所以在查找某个关键字的时候找到即可返回。
        而 B+Tree 所有的数据都在叶子结点，每次查找都得到叶子结点。所以在同样高度的 B-Tree 和 B+Tree 中，B-Tree 查找某个关键字的效率更高。   
        ②由于 B+Tree 所有的数据都在叶子结点，并且结点之间有指针连接，在找大于某个关键字或者小于某个关键字的数据的时候，
        B+Tree 只需要找到该关键字然后沿着链表遍历就可以了，而 B-Tree 还需要遍历该关键字结点的根结点去搜索。 
        ③由于 B-Tree 的每个结点（这里的结点可以理解为一个数据页）都存储主键+实际数据，
        而 B+Tree 非叶子结点只存储关键字信息，而每个页的大小是有限的，所以同一页能存储的 B-Tree 的数据会比 B+Tree 存储的更少。
        这样同样总量的数据，B-Tree 的深度会更大，增大查询时的磁盘 I/O 次数，进而影响查询效率。 

"""

"""
mysql 主从多线程复制:
    1. 主从复制通过三个线程来完成，在master节点运行的binlog dump的线程，I/O线程和SQL线程运行在slave 节点
        1).master节点的Binlog dump线程，当slave节点与master正常连接的时候，master把更新的binlog 内容推送到slave节点。
        2).slave节点的I/O 线程 ，该线程通过读取master节点binlog日志名称以及偏移量信息将其拷贝到本地relay log日志文件。
        3).slave节点的SQL线程，该线程读取relay log日志信息，将在master节点上提交的事务在本地回放，达到与主库数据保持一致的目的。
    
    问题1:
        Master节点的数据库实例并发跑多个线程同时提交事务，提交的事务按照逻辑的时间（数据库LSN号）顺序地写入binary log日志，,
        slave节点通过I/O线程写到本地的relay log日志，但是slave节点只有SQL单线程来执行relay log中的日志信息重放主库提交得事务，
        造成主备数据库存在延迟（lag）
    解决办法:
        1. slave本地的relay log记录的是master 的binary log日志信息，日志记录的信息按照事务的时间先后顺序记录，
        那么为了保证主备数据一致性，slave节点必须按照同样的顺序执行，如果顺序不一致容易造成主备库数据不一致的风险。
        MySQL 5.6改进：
            MySQL 5.6版本引入并发复制（schema级别），基于schema级别的并发复制核心思想：“不同schema下的表并发提交时的数据不会相互影响，
            即slave节点可以用对relay log中不同的schema各分配一个类似SQL功能的线程，来重放relay log中主库已经提交的事务，保持数据与主库一致”。
            可见MySQL5.6版本的并发复制，一个schema分配一个类似SQL线程的功能。
        实现:
            slave节点开启并发复制（slave_parallel_workers＝3）
    问题2:
        MySQL 5.6基于schema级别的并发复制能够解决当业务数据的表放在不同的database库下，
        但是实际生产中往往大多数或者全部的业务数据表都放在同一个schema下，
        在这种场景即使slave_parallel_workers>0设置也无法并发执行relay log中记录的主库提交数据。 
        高并发的情况下，由于slave无法并发执行同个schema下的业务数据表，依然会造成主备延迟的情况。
    解决办法:
        思考:
            那么如果slave同时可以用多线程的方式，同时执行一个schema下的所有业务数据表，
            将能大大提高slave节点执行ralay log中记录的主库提交事务达到与主库数据同步的目的，实现该功能我们需要解决什么问题？
            1、前面提到过为了保证主库数据一致性，master节点写入的binary log日志按照数据库逻辑时间先后的顺序并且slave节点
            执行relay log中主库提交的事务必须按照一致的顺序否则会造成主备数据不一致的情况。
            2、既然要实现scehma下所有的业务数据表能够并发执行，那么slave必须得知道并发执行relay 
            log中主库提交的事务不能相互影响而且结果必须和主库保持一致。
        实现:
              MySQL 5.7 引入Enhanced Muti-threaded slaves,
              当slave配置slave_parallel_workers>0并且global.slave_parallel_type＝‘LOGICAL_CLOCK’,
              可支持一个schema下，slave_parallel_workers个的worker线程并发执行relay log中主库提交的事务。
              但是要实现以上功能，需要在master机器标记binary log中的提交的事务哪些是可以并发执行，
              虽然MySQL 5.6已经引入了binary log group commit，但是没有将可以并发执行的事务标记出来。
              MySQL5.7引入 binlog_group_commit_sync_delay和 binlog_group_commit_sync_no_delay_count参数即提高binary log组提交并发数量。
              MySQL等待binlog_group_commit_sync_delay毫秒的时间直到binlog_group_commit_sync_no_delay_count个事务数时，将进行一次组提交。
"""
