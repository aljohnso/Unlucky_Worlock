drop table if exists Trips;
create table Trips (
  id integer primary key autoincrement,
  Trip_Name TEXT not null,
  Trip_Capacity INTEGER not null,
  Trip_Info TEXT not null,
  Trip_Participants Text not NULL
);