PRAGMA foreign_keys = ON ;
drop table if exists Master;
create TABLE Master (
  id integer PRIMARY KEY AUTOINCREMENT ,
  Trip_Name TEXT not NULL,
  Deparure_Date TEXT not NULL,
  Return_Date TEXT not NULL,
  Details_Short TEXT not NULL,
  Post_Time TEXT not NULL,
  Participant_num Integer not Null,
  Partcipant_cap  Integer not NULL,
  Trip_Location Integer NOT NULL
);
drop table if exists Trips;
CREATE TABLE Trips(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  Master_Key integer not NULL,
  Details TEXT not NULL,
  Coordinator_Name TEXT not NULL,
  Coordinator_Email TEXT not NULL,
  Coordinator_Phone Integer not NULL,
  Gear_List TEXT not NULL,
  Trip_Meeting_Place TEXT not NULL,
  Additional_Costs Integer not NULL,
  Total_Cost Integer NOT NULL,
  Cost_BreakDown Text NOT NULL,
  Car_Cap Integer NOT NULL,
--   Num_Cars_On_Trip Integer NOT NULL,
  Substance_Frre Integer NOT NULL,
  Weather_Forcast blob NOT NULL,
  FOREIGN KEY(Master_Key) REFERENCES Master(id) ON DELETE CASCADE
);
drop table if exists Participants;
CREATE TABLE Participants(
  id integer PRIMARY KEY AUTOINCREMENT,
  Trips_Key integer not NULL,
  Participant TEXT not null,
  Phone integer not NULL,
  Email TEXT NOT NULL,
  Driver Integer not NULL,
  Car_Capacity Integer not NULL,
  FOREIGN KEY(Trips_Key) REFERENCES Trips(id) ON DELETE CASCADE
);



