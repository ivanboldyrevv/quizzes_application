drop table if exists "user" cascade;
drop table if exists "quiz" cascade;
drop table if exists "question" cascade;
drop table if exists "user_stats" cascade;
drop table if exists "option" cascade;

create table if not exists "user" (
    user_id uuid primary key,
    username bpchar not null
);

create table if not exists "quiz" (
    quiz_id uuid primary key,
    quiz_name bpchar,
    difficult_level bpchar,
    creation_date date,
    created_by_id uuid references "user" (user_id)
);

create table if not exists "question" (
    question_id uuid primary key,
    question_text bpchar,
    quiz_id uuid references "quiz" (quiz_id)
);

create table if not exists "option" (
    option_id uuid primary key,
    option_text bpchar,
    is_correct boolean,
    question_id uuid references "question" (question_id)
);

create table if not exists "user_stats" (
    stat_id uuid primary key,
    accept_rate float not null,
    dispatch_date timestamp not null,
    user_id uuid references "user" (user_id),
    quiz_id uuid references "quiz" (quiz_id)
);