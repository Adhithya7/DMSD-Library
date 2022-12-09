CREATE OR REPLACE FUNCTION abort_insert()
RETURNS trigger LANGUAGE plpgsql as $$
BEGIN
RETURN null;
END $$;

-- CREATE TRIGGER TOTAL_BOOKS_BORROWED
-- BEFORE INSERT ON RESERVES
-- FOR EACH ROW
-- WHEN (10 >= ALL(SELECT COUNT(*)
--                 FROM (SELECT BOR_NO as txn, RID FROM BORROWS WHERE RDTIME is null
--                       UNION ALL
--                       SELECT RESERVATION_NO as txn, RID from RESERVES) AS C
--                 GROUP BY RID))
-- EXECUTE PROCEDURE abort_insert();

