#### 功能
1. 通过pt-table-checksum,pt-table-sync对mysql进行数据一致性检测并修复并发发送邮件报表

#### 使用
```
[root@databaseops mysql-tool]# python3 mysql_repl_checksum.py
Checking if all tables can be checksummed ...
Starting checksum ...
            TS ERRORS  DIFFS     ROWS  DIFF_ROWS  CHUNKS SKIPPED    TIME TABLE
07-08T09:25:34      0      1        9          7       1       0   0.013 test.t1
email is send sucess

# A software update is available:
DELETE FROM `test`.`t1` WHERE `id`='18' LIMIT 1 /*percona-toolkit src_db:test src_tbl:t1 src_dsn:P=3306,h=10.16.24.197,p=...,u=root dst_db:test dst_tbl:t1 dst_dsn:P=3306,h=10.16.24.198,p=...,u=root lock:1 transaction:1 changing_src:repl_checksum.checksum replicate:repl_checksum.checksum bidirectional:0 pid:127555 user:root host:databaseops*/;
DELETE FROM `test`.`t1` WHERE `id`='20' LIMIT 1 /*percona-toolkit src_db:test src_tbl:t1 src_dsn:P=3306,h=10.16.24.197,p=...,u=root dst_db:test dst_tbl:t1 dst_dsn:P=3306,h=10.16.24.198,p=...,u=root lock:1 transaction:1 changing_src:repl_checksum.checksum replicate:repl_checksum.checksum bidirectional:0 pid:127555 user:root host:databaseops*/;
DELETE FROM `test`.`t1` WHERE `id`='22' LIMIT 1 /*percona-toolkit src_db:test src_tbl:t1 src_dsn:P=3306,h=10.16.24.197,p=...,u=root dst_db:test dst_tbl:t1 dst_dsn:P=3306,h=10.16.24.198,p=...,u=root lock:1 transaction:1 changing_src:repl_checksum.checksum replicate:repl_checksum.checksum bidirectional:0 pid:127555 user:root host:databaseops*/;
DELETE FROM `test`.`t1` WHERE `id`='24' LIMIT 1 /*percona-toolkit src_db:test src_tbl:t1 src_dsn:P=3306,h=10.16.24.197,p=...,u=root dst_db:test dst_tbl:t1 dst_dsn:P=3306,h=10.16.24.198,p=...,u=root lock:1 transaction:1 changing_src:repl_checksum.checksum replicate:repl_checksum.checksum bidirectional:0 pid:127555 user:root host:databaseops*/;
DELETE FROM `test`.`t1` WHERE `id`='26' LIMIT 1 /*percona-toolkit src_db:test src_tbl:t1 src_dsn:P=3306,h=10.16.24.197,p=...,u=root dst_db:test dst_tbl:t1 dst_dsn:P=3306,h=10.16.24.198,p=...,u=root lock:1 transaction:1 changing_src:repl_checksum.checksum replicate:repl_checksum.checksum bidirectional:0 pid:127555 user:root host:databaseops*/;
DELETE FROM `test`.`t1` WHERE `id`='28' LIMIT 1 /*percona-toolkit src_db:test src_tbl:t1 src_dsn:P=3306,h=10.16.24.197,p=...,u=root dst_db:test dst_tbl:t1 dst_dsn:P=3306,h=10.16.24.198,p=...,u=root lock:1 transaction:1 changing_src:repl_checksum.checksum replicate:repl_checksum.checksum bidirectional:0 pid:127555 user:root host:databaseops*/;
DELETE FROM `test`.`t1` WHERE `id`='30' LIMIT 1 /*percona-toolkit src_db:test src_tbl:t1 src_dsn:P=3306,h=10.16.24.197,p=...,u=root dst_db:test dst_tbl:t1 dst_dsn:P=3306,h=10.16.24.198,p=...,u=root lock:1 transaction:1 changing_src:repl_checksum.checksum replicate:repl_checksum.checksum bidirectional:0 pid:127555 user:root host:databaseops*/;
sync is success
```

#### 邮件
<img width="493" alt="image" src="https://user-images.githubusercontent.com/40233339/177898322-6ab89eba-3610-4514-ab63-4265db3d6d51.png">
