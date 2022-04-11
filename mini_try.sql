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
select * from users;

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

insert into lists values('movies','tenet',2),('movies','minion',2),('chocolates','kitkat',2),('chocolates','5star',2);
insert into lists values('games','gta5',1),('games','a_creed',1),('games','pubg',1);
insert into lists values('prepartion','finance',1);
insert into lists values('preparation','ITIL',1);
insert into lists values('preparation','python',1);
select * from lists;

insert into tasks(task_desc,t_status,user_id) values('#meet at 10AM','0',1);
insert into tasks(task_desc,t_status,user_id) values('visit temple','0',1);
insert into tasks(task_desc,t_status,user_id) values('#gift for mom #bday','0',2);
insert into tasks(task_desc,t_status,user_id) values('meet a friend #imp','0',2);
select * from tasks;
delete from tasks where task_id=8;

delete from lists where list_name='prepartion';
select * from lists;

create table hashtags(
hashtag varchar(255),
user_id int,
task_id int,
foreign key (task_id) references tasks(task_id) on delete cascade on update cascade,
foreign key (user_id) references users(user_id)
);

insert into hashtags values('#meet',1,1),('#gift',2,3),('#bday',2,3),('#play',2,7),('#sample',2,12);
select * from hashtags;

select task_desc from tasks,hashtags where tasks.task_id=hashtags.task_id and hashtag="#bday"; 

delete from tasks where task_id=12;
select * from tasks;
update tasks set task_desc="#meet a friend" where task_id=4;
insert into hashtags values('#meet',2,4);
delete from hashtags where hashtag in ('#','#sample');
alter table hashtags add primary key(hashtag,user_id,task_id);
select * from hashtags;
update tasks set task_desc="sample task" where task_id=13;
update tasks set task_desc="sample #task" where task_id=13;
delete from tasks where task_id=13;
select * from hashtags;