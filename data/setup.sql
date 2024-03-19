sqlite3 eirgrid_data.db
.mode csv
.import combined_df.csv energy_data

UPDATE energy_data
SET
`NI Generation` = NULLIF(`NI Generation`, ''),
`NI Demand` = NULLIF(`NI Demand`, ''),
`NI Wind Availability` = NULLIF(`NI Wind Availability`, ''),
`NI Wind Generation` = NULLIF(`NI Wind Generation`, ''),
`IE Generation` = NULLIF(`IE Generation`, ''),
`IE Demand` = NULLIF(`IE Demand`, ''),
`IE Wind Availability` = NULLIF(`IE Wind Availability`, ''),
`IE Wind Generation` = NULLIF(`IE Wind Generation`, ''),
SNSP = NULLIF(SNSP, ''),
`NI Solar Availability` = NULLIF(`NI Solar Availability`, ''),
`NI Solar Generation` = NULLIF(`NI Solar Generation`, ''),
`Moyle I/C` = NULLIF(`Moyle I/C`, ''),
`IE Hydro` = NULLIF(`IE Hydro`, ''),
`EWIC I/C` = NULLIF(`EWIC I/C`, ''),
`Inter-Jurisdictional Flow` = NULLIF(`Inter-Jurisdictional Flow`, '');


-- Create a new table with the correct data types
CREATE TABLE energy_data_new (
    DateTime TEXT,
    `NI Generation` REAL,
    `NI Demand` REAL,
    `NI Wind Availability` REAL,
    `NI Wind Generation` REAL,
    `IE Generation` REAL,
    `IE Demand` REAL,
    `IE Wind Availability` REAL,
    `IE Wind Generation` REAL,
    `SNSP` REAL,
    `NI Solar Availability` REAL,
    `NI Solar Generation` REAL,
    `Moyle I/C` REAL,
    `IE Hydro` REAL,
    `EWIC I/C` REAL,
    `Inter-Jurisdictional Flow` REAL
);

 -- Insert data from the old table into the new table
INSERT INTO energy_data_new (DateTime, `NI Generation`, `NI Demand`, `NI Wind Availability`, `NI Wind Generation`, `IE Generation`, `IE Demand`, `IE Wind Availability`, `IE Wind Generation`, `SNSP`, `NI Solar Availability`, `NI Solar Generation`, `Moyle I/C`, `IE Hydro`, `EWIC I/C`, `Inter-Jurisdictional Flow`)
SELECT `DateTime`, `NI Generation`, `NI Demand`, `NI Wind Availability`, `NI Wind Generation`, `IE Generation`, `IE Demand`, `IE Wind Availability`, `IE Wind Generation`, `SNSP`, `NI Solar Availability`, `NI Solar Generation`, `Moyle I/C`, `IE Hydro`, `EWIC I/C`, `Inter-Jurisdictional Flow`
FROM energy_data;


SELECT * FROM energy_data_new LIMIT 10;
PRAGMA table_info(energy_data_new);
PRAGMA table_info(energy_data);


-- Optionally, rename the old table for backup
ALTER TABLE energy_data RENAME TO energy_data_old;

-- Rename the new table to the original name
ALTER TABLE energy_data_new RENAME TO energy_data;

-- If everything looks good, you may drop the old table
DROP TABLE energy_data_old;


SELECT * FROM energy_data LIMIT 10;
