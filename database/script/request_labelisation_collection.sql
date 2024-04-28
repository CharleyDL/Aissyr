-- Request to insert 'Labelisation' in 'Collection' table

-- Insert Labelisation in heroku database
begin;
set transaction read write;
INSERT INTO collection_ref (collection_name)
     VALUES ('labelisation')
         ON CONFLICT (collection_name)
            DO NOTHING;
COMMIT;

-- Control the insert
SELECT * FROM collection_ref;


-- Insert Labelisation in local database

-- INSERT INTO collection_ref (collection_name)
--      VALUES ('labelisation')
--          ON CONFLICT (collection_name)
--             DO NOTHING;

-- Control the insert
-- SELECT * FROM collection_ref;