\copy publisher (pubname,address) from 'csvs/PUBLISHER.csv' delimiter ',' CSV HEADER;

SELECT setval('publisher_publisherid_seq', 22, FALSE);

\copy person (pid,pname) from 'csvs/PERSON.csv' delimiter ',' CSV HEADER;

\copy document (title,pdate,publisherid) from 'csvs/DOCUMENT.csv' delimiter ',' CSV HEADER;

SELECT setval('document_docid_seq', 101, FALSE);

\copy book (docid,isbn) from 'csvs/BOOK.csv' delimiter ',' CSV HEADER;

\copy journal_volume (docid,volume_no,editor) from 'csvs/JOURNAL_VOLUME.csv' delimiter ',' CSV HEADER;

\copy proceedings (docid,cdate,clocation,ceditor) from 'csvs/PROCEEDINGS.csv' delimiter ',' CSV HEADER;

\copy authors (pid,docid) from 'csvs/AUTHORS.csv' delimiter ',' CSV HEADER;

\copy journal_issue (docid,issue_no,scope) from 'csvs/JOURNAL_ISSUE.csv' delimiter ',' CSV HEADER;

\copy gedits (docid,issue_no,pid) from 'csvs/GEDITS.csv' delimiter ',' CSV HEADER;

\copy chairs (pid,docid) from 'csvs/CHAIRS.csv' delimiter ',' CSV HEADER;

\copy reader (rtype,rname,raddress,phone_no) from 'csvs/READER.csv' delimiter ',' CSV HEADER;

SELECT setval('reader_rid_seq',31,FALSE);

\copy branch (lname,location) from 'csvs/BRANCH.csv' delimiter ',' CSV HEADER;

SELECT setval('branch_bid_seq', 11, FALSE);

\copy copy (docid,copyno,bid,position) from 'csvs/COPY.csv' delimiter ',' CSV HEADER;