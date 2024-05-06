-- ================================ ms_category ================================
-- auto-generated definition
create table ms_category
(
    category_id   integer default nextval('ms_category_id_seq'::regclass) not null
        constraint ms_category_pk
            primary key,
    category_name varchar
);

alter table ms_category
    owner to postgres;

-- auto-generated definition
create sequence ms_category_id_seq
    as integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

alter sequence ms_category_id_seq owner to postgres;

alter sequence ms_category_id_seq owned by ms_category.category_id;



-- ================================ ms_member ================================
-- auto-generated definition
create table ms_member
(
    member_id   varchar(6) not null
        constraint ms_member_pk
            primary key,
    member_name varchar,
    phone       varchar(16),
    address     varchar,
    email       varchar,
    outlet_id   varchar(4)
);

alter table ms_member
    owner to postgres;

create index ms_member_member_id_index
    on ms_member (member_id);


-- ================================ ms_merk ================================
-- auto-generated definition
create table ms_merk
(
    merk_id     integer default nextval('ms_merk_id_seq'::regclass) not null
        constraint ms_merk_pk
            primary key,
    merk_name   varchar,
    category_id integer                                             not null
        constraint ms_merk_ms_category_category_id_fk
            references ms_category
);

alter table ms_merk
    owner to postgres;


-- ================================ ms_merk_id_seq ================================
-- auto-generated definition
create sequence ms_merk_id_seq
    as integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

alter sequence ms_merk_id_seq owner to postgres;

alter sequence ms_merk_id_seq owned by ms_merk.merk_id;


-- ================================ ms_outlet ================================
-- auto-generated definition
create table ms_outlet
(
    outlet_id   varchar not null
        constraint ms_outlet_pk
            primary key,
    outlet_name varchar,
    address     varchar,
    phone       varchar
);

alter table ms_outlet
    owner to postgres;


-- ================================ ms_payment_type ================================
-- auto-generated definition
create table ms_payment_type
(
    type_id   serial
        constraint ms_payment_type_pk
            primary key,
    type_name varchar
);

alter table ms_payment_type
    owner to postgres;


-- ================================ ms_payment_type_id_seq ================================
-- auto-generated definition
create sequence ms_payment_type_type_id_seq
    as integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

alter sequence ms_payment_type_type_id_seq owner to postgres;

alter sequence ms_payment_type_type_id_seq owned by ms_payment_type.type_id;


-- ================================ ms_product ================================
-- auto-generated definition
create table ms_product
(
    sku          varchar           not null
        constraint ms_product_pk
            primary key,
    part_number  varchar,
    product_name varchar,
    merk_id      integer           not null
        constraint ms_product_ms_merk_merk_id_fk
            references ms_merk,
    vehicle      varchar,
    category_id  integer           not null
        constraint ms_product_ms_category_category_id_fk
            references ms_category,
    outlet_id    varchar           not null
        constraint ms_product_ms_outlet_outlet_id_fk
            references ms_outlet,
    qty          integer default 0 not null,
    harga_beli   numeric default 0 not null,
    harga_jual   numeric default 0 not null,
    barcode      numeric(12)
        constraint ms_product_pk2
            unique
);

alter table ms_product
    owner to postgres;


-- ================================ ms_rekening ================================
-- auto-generated definition
create table ms_rekening
(
    rek_no   numeric not null,
    rek_name varchar,
    rek_bank varchar,
    status   boolean,
    id       serial
        constraint ms_rekening_pk
            primary key
);

alter table ms_rekening
    owner to postgres;


-- ================================ ms_rekening_id_seq ================================
-- auto-generated definition
create sequence ms_rekening_id_seq
    as integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

alter sequence ms_rekening_id_seq owner to postgres;

alter sequence ms_rekening_id_seq owned by ms_rekening.id;


-- ================================ ms_user ================================
-- auto-generated definition
create table ms_user
(
    user_id varchar(5) not null
        constraint ms_user_pk
            primary key,
    name    varchar,
    level   numeric(1),
    pin     numeric(6)
);

alter table ms_user
    owner to postgres;

create index ms_user_user_id_index
    on ms_user (user_id);


-- ================================ tx_ofaktur ================================
-- auto-generated definition
create table tx_ofaktur
(
    head_fak       varchar not null
        constraint tx_ofaktur_pk
            primary key,
    ordinal_number varchar not null
);

alter table tx_ofaktur
    owner to postgres;


-- ================================ tx_receipt ================================
-- auto-generated definition
create table tx_receipt
(
    faktur       varchar                      not null
        constraint tx_receipt_pk
            primary key,
    date_tx      date    default CURRENT_DATE not null,
    store_buy    varchar,
    total_faktur numeric default 0            not null,
    discount     numeric default 0            not null,
    other_fee    numeric default 0,
    other_note   varchar,
    update_date  date    default CURRENT_DATE not null
);

alter table tx_receipt
    owner to postgres;


-- ================================ tx_receipt_detail ================================
-- auto-generated definition
create table tx_receipt_detail
(
    faktur       varchar           not null,
    sku          varchar           not null,
    part_number  varchar,
    product_name varchar,
    merk_name    varchar,
    qty          numeric default 0 not null,
    price        numeric default 0 not null,
    constraint tx_receipt_detail_pk
        primary key (faktur, sku)
);

alter table tx_receipt_detail
    owner to postgres;


-- ================================ tx_trans ================================
-- auto-generated definition
create table tx_trans
(
    faktur       varchar                      not null
        constraint tx_trans_pk
            primary key,
    date_tx      date    default CURRENT_DATE not null,
    tx_type      varchar,
    due_date     varchar,
    member_id    varchar
        constraint tx_trans_ms_member_member_id_fk
            references ms_member,
    status       boolean default false        not null,
    other_fee    numeric default 0            not null,
    other_note   varchar,
    update_date  date    default CURRENT_DATE not null,
    total_faktur numeric default 0            not null,
    payment_id   integer
        constraint tx_trans_ms_payment_type_type_id_fk
            references ms_payment_type,
    payment_info varchar default ''::character varying,
    time_tx      time    default CURRENT_TIME
);

alter table tx_trans
    owner to postgres;


-- ================================ tx_trans_detail ================================
-- auto-generated definition
create table tx_trans_detail
(
    faktur       varchar not null,
    sku          varchar not null,
    part_number  varchar,
    product_name varchar,
    merk_name    varchar,
    qty          numeric,
    price        numeric,
    constraint tx_trans_detail_pk
        primary key (faktur, sku)
);

alter table tx_trans_detail
    owner to postgres;

