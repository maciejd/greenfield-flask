drop table if exists test_cases;
create table test_cases (
  id integer primary key autoincrement,
  title text not null,
  ts_id integer not null,
  foreign key (ts_id) references test_suites(id)
);
drop table if exists test_suites;
create table test_suites (
  id integer primary key autoincrement,
  title text not null
);
