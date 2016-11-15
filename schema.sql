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
drop table if exists test_runs;
create table test_runs (
  id integer primary key autoincrement,
  title text not null,
  created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
drop table if exists test_executions;
create table test_executions (
 id integer primary key autoincrement,
 tr_id integer not null, 
 tc_id integer not null,
 status text not null,
 updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 foreign key (tr_id) references test_runs(id),
 foreign key (tc_id) references test_cases(id)
)
