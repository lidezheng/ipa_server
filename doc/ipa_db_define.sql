

-- ipa详情表
create table if not exists ipa(
    id int not null auto_increment comment '主键id',
    filename varchar(64) not null default '' comment 'ipa唯一名字',
    title varchar(128) not null default '' comment '标题',
    identifier varchar(128) not null default '' comment 'ipa标识符',
    version varchar(128) not null default '' comment 'ipa版本号',
    update_desc varchar(256) not null default '' comment '打包描述',
    file_size int not null default '0' comment '文件字节数',

    status tinyint(1) not null default 1 comment '0屏蔽, 1正常',
    create_time datetime not null default CURRENT_TIMESTAMP comment '创建时间',
    update_time datetime not null default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP comment '最近修改时间',
    primary key (id)
)engine=innodb default charset=utf8mb4 comment 'ipa详情表';

