create table
    IF NOT EXISTS ms_merk (
        merk_id varchar not null constraint ms_merk_pk primary key,
        merk_name varchar
    );

alter table ms_merk owner to postgres;

-- auto-generated definition
create table
    if not exists ms_category (
        category_id varchar not null constraint ms_category_pk primary key,
        category_name varchar,
        merk_id varchar not null constraint ms_category_ms_merk__fk references ms_merk on delete restrict
    );

alter table ms_category owner to postgres;

-- auto-generated definition
create table
    if not exists ms_member (
        member_id varchar(6) not null constraint ms_member_pk primary key,
        member_name varchar,
        phone varchar(16),
        address varchar,
        email varchar,
        outlet_id varchar(4)
    );

alter table ms_member owner to postgres;

create index if not exists ms_member_member_id_index on ms_member (member_id);

-- auto-generated definition
create table
    if not exists ms_rekening (
        rek_no numeric not null,
        rek_name varchar,
        rek_bank varchar,
        status boolean,
        id serial constraint ms_rekening_pk primary key
    );

alter table ms_rekening owner to postgres;

-- auto-generated definition
create table
    if not exists ms_user (
        user_id varchar(5) not null constraint ms_user_pk primary key,
        name varchar,
        level numeric(1),
        pin numeric(6)
    );

alter table ms_user owner to postgres;

create index if not exists ms_user_user_id_index on ms_user (user_id);