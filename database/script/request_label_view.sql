-- Request to insert 'Labelisation' in 'Collection' table

-- Insert Labelisation in heroku database

begin;
set transaction read write;
INSERT INTO view_ref (view_name)
     VALUES ('label')
         ON CONFLICT (view_name)
            DO NOTHING;
COMMIT;

-- Control the insert
SELECT * FROM view_ref;


-- Insert Labelisation in local database

-- INSERT INTO view_ref (view_name)
--      VALUES ('label')
--          ON CONFLICT (view_name)
--             DO NOTHING;

-- Control the insert
-- SELECT * FROM view_ref;