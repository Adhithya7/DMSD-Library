CREATE TABLE
    PUBLISHER(
        PUBLISHERID serial PRIMARY KEY,
        PUBNAME VARCHAR(100),
        ADDRESS VARCHAR(100)
    );

CREATE TABLE
    DOCUMENT(
        DOCID serial PRIMARY KEY,
        TITLE VARCHAR(200),
        PDATE TIMESTAMP,
        PUBLISHERID int,
        FOREIGN KEY (PUBLISHERID) REFERENCES PUBLISHER(PUBLISHERID)
    );

CREATE TABLE
    PERSON(
        PID int PRIMARY KEY,
        PNAME VARCHAR(100)
    );

CREATE TABLE
    BOOK(
        DOCID int PRIMARY KEY,
        ISBN VARCHAR(100),
        FOREIGN KEY (DOCID) REFERENCES DOCUMENT(DOCID)
    );

CREATE TABLE
    AUTHORS(
        PID int,
        DOCID int,
        FOREIGN KEY (DOCID) REFERENCES BOOK(DOCID),
        FOREIGN KEY (PID) REFERENCES PERSON(PID),
        PRIMARY KEY (PID, DOCID) 
    );

CREATE TABLE
    JOURNAL_VOLUME(
        DOCID int PRIMARY KEY,
        VOLUME_NO int,
        EDITOR int,
        FOREIGN KEY (DOCID) REFERENCES DOCUMENT(DOCID),
        FOREIGN KEY (EDITOR) REFERENCES PERSON(PID)
    );

CREATE TABLE
    JOURNAL_ISSUE(
        DOCID int,
        ISSUE_NO int CHECK (ISSUE_NO < 11),
        SCOPE VARCHAR(100),
        FOREIGN KEY (DOCID) REFERENCES JOURNAL_VOLUME(DOCID),
        PRIMARY KEY (DOCID, ISSUE_NO)
    );

CREATE TABLE
    GEDITS(
        DOCID int,
        ISSUE_NO int,
        PID int,
        FOREIGN KEY (PID) REFERENCES PERSON(PID),
        FOREIGN KEY (DOCID, ISSUE_NO) REFERENCES JOURNAL_ISSUE(DOCID, ISSUE_NO),
        PRIMARY KEY (DOCID, ISSUE_NO, PID)
    );

CREATE TABLE
    PROCEEDINGS(
        DOCID int PRIMARY KEY,
        CDATE TIMESTAMP,
        CLOCATION VARCHAR(150),
        CEDITOR VARCHAR(150),
        FOREIGN KEY (DOCID) REFERENCES DOCUMENT(DOCID)
    );

CREATE TABLE
    CHAIRS(
        PID int,
        DOCID int,
        FOREIGN KEY (DOCID) REFERENCES PROCEEDINGS(DOCID),
        FOREIGN KEY (PID) REFERENCES PERSON(PID),
        PRIMARY KEY (PID, DOCID)
    );

CREATE TABLE
    BRANCH(
        BID serial PRIMARY KEY,
        LNAME VARCHAR(150),
        LOCATION VARCHAR(150)
    );

CREATE TABLE
    RESERVATION(
        RES_NO serial PRIMARY KEY,
        DTIME TIMESTAMP DEFAULT now()
    );

CREATE TABLE
    BORROWING(
        BOR_NO serial PRIMARY KEY,
        BDTIME TIMESTAMP DEFAULT now(),
        RDTIME TIMESTAMP DEFAULT NULL
    );

CREATE TABLE
    READER(
        RID serial PRIMARY KEY,
        RTYPE VARCHAR(30) CHECK (RTYPE in ('Student', 'Senior Citizen', 'Staff', 'Citizen')),
        RNAME VARCHAR(100),
        RADDRESS VARCHAR(300),
        PHONE_NO VARCHAR(50)
    );

CREATE TABLE
    COPY(
        DOCID int,
        COPYNO int,
        BID int,
        POSITION VARCHAR(30),
        FOREIGN KEY (DOCID) REFERENCES DOCUMENT(DOCID),
        FOREIGN KEY (BID) REFERENCES DOCUMENT(DOCID),
        PRIMARY KEY (DOCID, COPYNO, BID)
    );

CREATE TABLE
    RESERVES(
        RID int,
        RESERVATION_NO serial,
        DOCID int,
        COPYNO int,
        BID int,
        FOREIGN KEY (DOCID, COPYNO, BID) REFERENCES COPY (DOCID, COPYNO, BID),
        FOREIGN KEY (RESERVATION_NO) REFERENCES RESERVATION (RES_NO) ON DELETE CASCADE,
        FOREIGN KEY (RID) REFERENCES READER (RID),
        PRIMARY KEY (RESERVATION_NO, DOCID, COPYNO)
    );

CREATE TABLE
    BORROWS(
        BOR_NO serial,
        DOCID int,
        COPYNO int,
        BID int,
        RID int,
        FOREIGN KEY (DOCID, COPYNO, BID) REFERENCES COPY (DOCID, COPYNO, BID),
        FOREIGN KEY (BOR_NO) REFERENCES BORROWING (BOR_NO),
        FOREIGN KEY (RID) REFERENCES READER (RID),
        PRIMARY KEY (BOR_NO, DOCID, COPYNO, BID)
    );