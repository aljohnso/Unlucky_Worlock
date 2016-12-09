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
drop table if exists Master;
create TABLE Master (
  id integer PRIMARY KEY AUTOINCREMENT ,
  Trip_Name TEXT not NULL,
  Dates TEXT not NULL,
  Details_Short TEXT not NULL,
  Post_Time TEXT not NULL,
  Participant_num Integer not Null,
  Partcipant_cap  Integer not NULL,
  Trip_Location Integer NOT NULL
);
drop table if exists Trips;
CREATE TABLE Trips(
  id integer PRIMARY KEY AUTOINCREMENT,
  Master_Key integer not NULL,
  FOREIGN KEY(Master_Key) REFERENCES Master(id),
  Details TEXT not NULL,
  Cordinator_Name TEXT not NULL,
  Cordinator_Email TEXT not NULL,
  Cordinator_Phone Integer not NULL,
  Gear_List TEXT not NULL,
  Trip_Meeting_Place TEXT not NULL,
  Additonal_Costs Integer not NULL,
  Total_Cost Integer NOT NULL,
  Cost_BreakDown Text NOT NULL,
  Car_Cap Integer NOT NULL,
  Substance_Frre Integer NOT NULL,
  Weather_Forcast blob NOT NULL
)
drop table if exists Participants;
CREATE TABLE Participants(
  id integer PRIMARY KEY AUTOINCREMENT,
  Trips_Key integer not NULL,
  FOREIGN KEY(Trips_Key) REFERENCES Trips(id),
  Participant TEXT not null,
  Phone integer not NULL,
  Driver Integer not NULL,
  Car_Capacity Integer not NULL
)
