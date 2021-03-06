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

"""
    链接: https://developer.aliyun.com/article/731666?spm=a2c6h.12873581.0.0.795e6bf44hrzO1&groupCode=database
    mysql 优化:
    

"""

#  注意:  但在一条SQL里，对于一张表的查询 一次只能使用一个索引

"""
    mysql 支持表间关联关系 这就是嵌套循环, 关联表的数据量越大, 查询效率越低.
    mysql 对 join 嵌套循环的优化:
    Nested Loop Join算法:
        NLJ 算法:将驱动表/外部表的结果集作为循环基础数据. 普通Nested-Loop一次只将一行传入内层循环, 所以外层循环(的结果集)有多少行, 
        内存循环便要执行多少次.在内部表的连接上有索引的情况下，其扫描成本为O(Rn),若没有索引,则扫描成本为O(Rn*Sn)
    Block Nested-Loop Join算法:
        将外部循环的结果集放入 JOIN BUFFER中, 内层循环与整个JOIN BUFFER中的数据做比较, 减少循环次数.
    MySQL使用Join Buffer有以下要点:
      1. join_buffer_size变量决定buffer大小。
      2. 只有在join类型为all, index, range的时候才可以使用join buffer。
      3. 能够被buffer的每一个join都会分配一个buffer, 也就是说一个query最终可能会使用多个join buffer。
      4. 第一个nonconst table不会分配join buffer, 即便其扫描类型是all或者index。
      5. 在join之前就会分配join buffer, 在query执行完毕即释放。
      6. join buffer中只会保存参与join的列, 并非整个数据行。

"""

"""
    mysql group by 执行原理:
    
    group by 有三种实现方式:
        1.  松散索引扫描:  mysql 完全利用索引来实现group by, 并不需要扫描所有满足条件的索引键即可完成操作得出结果
        满足条件:
            GROUP BY 条件字段必须在同一个索引中最前面的连续位置;
            在使用GROUP BY 的同时，只能使用 MAX 和 MIN 这两个聚合函数;
            如果引用到了该索引中 GROUP BY 条件之外的字段条件的时候，必须以常量形式存在;
        2. 紧凑索引扫描: 需要读取所有满足条件的索引键，然后再根据读取恶的数据来完成 GROUP BY 操作得到相应结果。
        满足条件:
            当 GROUP BY 条件字段并不连续或者不是索引前缀部分的时候, 但是在Query 语句中存在一个常量值来引用缺失的索引键
        3. 临时表:
            无法找到合适的索引可以利用的时候，就不得不先读取需要的数据，然后通过临时表来完成 GROUP BY 操作

"""
"""
    mysql order by 执行原理:
    1. 索引排序
    2. filesort
        如果需要排序的数据量小于“排序缓冲区”，MySQL使用内存进行“快速排序”操作。如果内存不够排序，
        那么MySQL会先将数据分块，可对每个独立的块使用“快速排序”进行排序，再将各个块的排序结果放到磁盘上，
        然后将各个排好序的块进行“归并排序”，最后返回排序结果。
    两次回表传输排序:
        1. 第一次回表:  where 条件取出 rowid 并将 rowid及排序字段放到排序缓冲取中, 如果能放下就内存排序,
        否则就放到临时文件进行归并排序.
        2. 第二次回表: 按排序好的rowid 从数据文件中取出所要查询的数据. 
    单次回表传输排序:
        1. 第一次回表就取出查询所需要的所有列.
        弊端:  如果查询的数据量过大, 就必须建立临时文件进行归并排序, 如果临时文件过多就会降低排序效率.
        2. 如果查询字段中包含 BLOB, TEXT 类型用 两次回表.
        3. 如果单行字节 大于 max_length_for_sort_data 用两次回表.
"""
