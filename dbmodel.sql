 create database master ;
 use master;

/*for students */

create table users(id integer primary key auto_increment, name varchar(20), email varchar(20), password varchar(20) );

create table studentbooks_inventory(BookID integer primary key, BookName varchar(20),
TotalBooksBorrowed integer, ReturnDate date,Total_tokens integer,
 Available_Tokens integer);

create table borrow_books(book_id integer primary key, student_id integer,
 Book_Name varchar(20), Book_Count integer);

/* for admin */

create table adminbooks_inventory(BookID integer primary key, BookName varchar(20) ,
TotalBookCount integer, TotalBooksIssued integer, TotalBooksRegistered integer);

create table admin(admin_id integer primary key,admin_name varchar(20),admin_email varchar(20),admin_password varchar(20));

create table issue_books(student_id integer, book_id integer, issue_date date,\
 return_date date, book_count integer,foreign key(student_id) references users(id),\
 foreign key(book_id) references adminbooks_inventory(BookID));





