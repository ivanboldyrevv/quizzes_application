create table if not exists "user" (
    uid uuid primary key,
    username bpchar,
    password bpchar
);

insert into "user" values ('676e0207-4a40-4185-abec-24d300736abd', 'test1', 'pass')