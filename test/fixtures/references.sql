CREATE TABLE bob (
    id int, name varchar(255),
    sam_id int,
    FOREIGN KEY (sam_id) REFERENCES sam(sam_id)
);
CREATE TABLE sam (
    sam_id int, name varchar,
    thirdfield varchar(256),
    fourth int
);
