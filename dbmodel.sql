 create database master ;
 use master;
create table users(id integer primary key auto_increment, name varchar(20), email varchar(20), password varchar(20) );

create table books(book_id integer primary key, book_name varchar(20), book_count integer);


create table issue_books(student_id integer, bookid integer, issue_date date,\
 return_date date, book_count integer,foreign key(student_id) references users(id),\
 foreign key(bookid) references books(book_id));


create table admin(admin_id integer primary key, admin_name varchar(20),\
 admin_password varchar(20), admin_email varchar(20));