-- drop table "option";
-- drop table "question";
-- drop table "quiz";


-- create table if not exists "quiz" (
--     quiz_id uuid primary key,
--     timestamp_created timestamp,
--     quiz_name bpchar
-- )

-- insert into "quiz" values ('a69d46d4-affb-4708-8819-42793c19ed50', '2025-01-02 04:05:06', 'test-quiz-2');

-- create table if not exists "question" (
--     question_id uuid primary key,
--     question_text bpchar,
--     quiz_id uuid references quiz(quiz_id)
-- )

-- insert into "question" values ('a69d46d4-affb-4708-8819-42793c19ed81', 'test-question-1', 'a69d46d4-affb-4708-8819-42793c19ed80'),
                            --   ('a69d46d4-affb-4708-8819-42793c19ed82',	'test-question-2', 'a69d46d4-affb-4708-8819-42793c19ed80'),
                            --   ('a69d46d4-affb-4708-8819-42793c19ed83',	'test-question-3', 'a69d46d4-affb-4708-8819-42793c19ed80'),
                            --   ('a69d46d4-affb-4708-8819-42793c19ed11',	'test-question-2-1', 'a69d46d4-affb-4708-8819-42793c19ed50')

-- create table if not exists "option" (
--     option_id uuid primary key,
--     option_text bpchar,
--     is_correct boolean,
--     question_id uuid references question(question_id)
-- )

-- insert into "option" values ('a69d46d4-affb-4708-8819-42793c19ed90', 'test-option-1', 'false', 'a69d46d4-affb-4708-8819-42793c19ed81'),
                            -- ('a69d46d4-affb-4708-8819-42793c19ed91', 'test-option-2', true, 'a69d46d4-affb-4708-8819-42793c19ed81'),
                            -- ('a69d46d4-affb-4708-8819-42793c19ed92', 'test-option-3', false, 'a69d46d4-affb-4708-8819-42793c19ed82'),
                            -- ('a69d46d4-affb-4708-8819-42793c19ed93', 'test-option-4', false, 'a69d46d4-affb-4708-8819-42793c19ed82'),
                            -- ('a69d46d4-affb-4708-8819-42793c19ed94', 'test-option-5', true, 'a69d46d4-affb-4708-8819-42793c19ed82'),
                            -- ('a69d46d4-affb-4708-8819-42793c19ed95', 'test-option-6', false, 'a69d46d4-affb-4708-8819-42793c19ed83'),
                            -- ('a69d46d4-affb-4708-8819-42793c19ed96', 'test-option-7', true, 'a69d46d4-affb-4708-8819-42793c19ed83'),
                            -- ('a69d46d4-affb-4708-8819-42793c19ed31', 'test-option-2-1', false, 'a69d46d4-affb-4708-8819-42793c19ed11'),
                            -- ('a69d46d4-affb-4708-8819-42793c19ed32', 'test-option-2-2', true, 'a69d46d4-affb-4708-8819-42793c19ed11')
-- 