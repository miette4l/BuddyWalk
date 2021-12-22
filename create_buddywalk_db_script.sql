Create database BuddyWalk;

use BuddyWalk;

--The below tables 'user_details' and 'user_login' were created for registration and login
--These functionalities have not been added in current version.

--Create table user_details (
--user_ID INTEGER NOT NULL,
--first_name VARCHAR (50) NOT NULL,
--last_name VARCHAR (50) NOT NULL,
--address VARCHAR (100) NOT NULL,
--city VARCHAR (50) NOT NULL,
--postcode VARCHAR (10) NOT NULL,
--phone_number INTEGER NOT NULL,
--email_address VARCHAR (100) NOT NULL,
--PRIMARY KEY (user_ID)
--);
--
--Create table user_login (
--user_ID INTEGER NOT NULL,
--user_username VARCHAR (50) NOT NULL,
--user_password VARCHAR (50) NOT NULL,
--PRIMARY KEY (user_username),
--FOREIGN KEY (user_ID) REFERENCES user_details(user_ID)
--);
--
--INSERT INTO user_details
--(user_ID, first_name, last_name, address, city, postcode, phone_number, email_address)
--VALUES
--(001, 'Jenny', 'Simms', '46_Roseberry_Avenue', 'London','N102LJ', '7967648', 'jsimms@hotmail.com'),
--(002, 'Lyla', 'Plumber', '149_St_Marys_Road', 'London','N98NR', '7795405', 'lplumber@gmail.com'),
--(003, 'Freddie', 'Taylor', '237_Regents_Park_Road', 'London', 'N33LF', '7635608', 'ftaylor@gmail.com'),
--(004, 'Daniella', 'Smith', '28_Featherstone_Road', 'London', 'NW72BN', '765350', 'dsmith@gmail.com'),
--(005, 'Therese', 'Shah', '131_East_End_Road', 'London', 'N20SZ', '7645308', 'tshah@hotmail.com'),
--(006, 'Francesca', 'Dumait', 'Manor_House_Friern_Barnet_Lane','London','N200NL', '7864398', 'fdumait@hotmail.com'),
--(007, 'Harriet', 'Bennett', '3_Westmoreland_Road', 'London','NW99RL', '7658493', 'hbennett@hotmail.com'),
--(008, 'Lily', 'Wells', '67_Hampstead_High_Street','London','NW31QP', '7856983', 'lwells@hotmail.com'),
--(009, 'Olivia', 'James', '255_Upper_Street','London','N11RY', '7892569', 'ojames@gmail.com'),
--(010, 'Carla', 'Stratton', '19_Talacre_Street','London','NW53PH', '7637876', 'cstratton@hotmail.com'),
--(011, 'Henrietta', 'Gibbs', '61_Markfield_Road','London','N154QA', '7659230', 'hgibbs@gmail.com'),
--(012, 'Joanne', 'Sumption', '15_Dukes_Mews','London','N102QP', '7638980', 'jsumption@me.com'),
--(013, 'Bea', 'Hibberd', '9_Oxford_Avenue','London','N145AF', '7867987', 'bhibberd@hotmail.com'),
--(014, 'Nicki', 'Taylor', '120_Bethnal_Green_Road','London','E26DG', '7986745', 'ntaylor@me.com'),
--(015, 'Imani', 'Ingrid', '161_Greyhound_Lane', 'London', 'SW165NJ', '7698476', 'iingrid@gmail.com'),
--(016, 'Bryce', 'Collins', '163_Bromley_Road', 'London', 'SE62NZ', '7986548', 'bcollins@hotmail.com'),
--(017, 'Cali', 'Jones', '70_Cecile_Park', 'London', 'N89AU', '7792608', 'cjones@btinternet.com'),
--(018, 'Sacha', 'Esmailji', '8_Halefield_Road', 'London', 'N179XR', '7658427', 'sesmailji@googlemail.com'),
--(019, 'Elouise', 'Odetola', '74_Lordship_Lane', 'London', 'SE228HF', '7865885', 'eodetola@gmail.com'),
--(020, 'Iben', 'Holden', '3_Percy_Street', 'London', 'W1T1DE', '7638986', 'iholden@hotmail.com')
--;
--
--INSERT INTO user_login
--(user_ID, user_username, user_password)
--VALUES
--(001, 'jjsimms46', 'Warlord37'),
--(002, 'Lylaplum', 'fishes235'),
--(003, 'ftaytay', 'fantom34'),
--(004, 'DanniS', 'truffles13'),
--(005, 'Shahtay3', 'kibble123'),
--(006, 'FranDumait', 'shipping89'),
--(007, 'harrietbenn', 'shalala34'),
--(008, 'Lilwells', 'triportreat9'),
--(009, 'OliviaJJ', 'privatjames35'),
--(010, 'CStratton', 'benzo89'),
--(011, 'HenriGibbs', 'thabow34'),
--(012, 'JoSumpt', 'barrow16'),
--(013, 'BeaBeaHibberd', 'jelly99'),
--(014, 'NixTaylor', 'Bethnal89'),
--(015, 'Imingrid', 'greyhound66'),
--(016, 'BryceCo', 'bromleyR88'),
--(017, 'CalJones', 'cecilback9'),
--(018, 'SachaE', 'Halefield17'),
--(019, 'Odetoto', 'Lordship1993'),
--(020, 'IbenH', 'percysquare')
--;

Create table journey_requests (
user_id VARCHAR(50) NOT NULL,
user_username VARCHAR (50) NOT NULL,
CurrentLocLat DOUBLE (33, 30) NOT NULL,
CurrentLocLng DOUBLE (33, 30) NOT NULL,
DestinationLat DOUBLE (33, 30) NOT NULL,
DestinationLng DOUBLE (33, 30) NOT NULL,
ToD VARCHAR (50) NOT NULL,
phone_number VARCHAR(50) NOT NULL,
matched VARCHAR(10) DEFAULT 'False'
);

Create table matches (
user_id_1 VARCHAR(50) NOT NULL,
user_id_2 VARCHAR(50) NOT NULL
);