create database if not exists todo1;
show databases;
use todo1;
show tables;
create table if not exists users(
user_id int primary key auto_increment,
user_name varchar(255) unique,
password varchar(255)
);
select * from users;

insert into users(user_name,password) values('rio','xyz'), ('lisa','abc');

create table if not exists lists(
list_name varchar(255),
list_item varchar(255),
user_id int,
foreign key (user_id) references users(user_id),
primary key(list_name, list_item, user_id)
);

create table if not exists tasks(
task_id int primary key auto_increment,
task_desc varchar(500),
t_status enum('0','1'),
user_id int,
foreign key (user_id) references users(user_id)
);

select * from lists;

select * from tasks;

create table hashtags(
hashtag varchar(255),
user_id int,
task_id int,
foreign key (task_id) references tasks(task_id) on delete cascade on update cascade,
foreign key (user_id) references users(user_id)
);

select * from hashtags;

select task_desc from tasks,hashtags where tasks.task_id=hashtags.task_id and hashtag="#bday"; 

select * from tasks;

alter table hashtags add primary key(hashtag,user_id,task_id);
