drop table if exists test_cases;
create table test_cases (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);
