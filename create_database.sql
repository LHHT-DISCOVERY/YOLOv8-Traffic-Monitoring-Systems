create database datn;
use datn;
create table nametransportation(
	id_name int primary key,
    vh_name varchar(255)
);

create table transportationviolation(
	id int primary key auto_increment,
    id_name int,
    date_violate date,
    foreign key(id_name) references nametransportation(id_name)
);

-- Khởi tạo 5 loại phương tiện
insert into nametransportation(id_name , vh_name)
values (1,'OTO'),(2,'Xe May'),(3,'Xe Dap'), (4,'Xe Tai'), (5,'Xe Bus');

-- Khởi tạo dữ liệu phương tiện ban dầu vi phạm
insert into transportationviolation(id_name , date_violate) values (1,'2023-02-12') , (2,'2023-02-12'), (3,'2023-02-12'), (4,'2023-02-12'), (5,'2023-02-12')
