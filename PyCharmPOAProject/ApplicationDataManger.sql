drop table if exists Trips;
create table Trips (
  id integer primary key autoincrement,
  Trip_Name TEXT not null,
  Trip_Capacity INTEGER not null,
  Trip_Info TEXT not null,
  Trip_Participants TEXT not NULL
);
-- drop table if exists detailedTrips;--consider table of tables or use a more complex table
-- create table detailedTrips (
--   id integer primary key autoincrement,
--   Trip_Name TEXT not null,
--   Trip_Capacity INTEGER not null,
--   Trip_Info TEXT not null,
--   Trip_Participants TEXT not NULL
--
-- )
