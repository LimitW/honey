use honey;

drop table if exists history;
drop table if exists current;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";

SET names utf8;

create table current
(
	id                  bigint not null auto_increment,
	dt                  date not null,
	url                 text not null,
	province            text not null,
	description         text,
	part                text not null,
	type                int not null,
	status              int not null default 0,
	primary key (id)
)default charset = utf8;

create table history
(
	id                  bigint not null auto_increment,
	dt                  date not null,
	url                 text not null,
	description         text,
	type                int not null,
	part                text not null,
	province            text not null,
	primary key(id)
)default charset = utf8;
