DO $$ 
DECLARE
    table_rec RECORD;
    column_rec RECORD;
    search_query TEXT;
    keyword TEXT := 'Data''; DROP DATABASE test; --';
    user_id INTEGER := 1;
BEGIN
    -- Loop through the specified tables
    FOR table_rec IN 
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        AND table_name IN ('users', 'education', 'work_experience', 'skills')
    LOOP
        -- Loop through all columns in each table
        FOR column_rec IN
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public'
            AND table_name = table_rec.table_name
            AND data_type IN ('character varying', 'text')
        LOOP
            -- Construct the dynamic query to search for the keyword in the specific column
            IF table_rec.table_name = 'users' THEN
                search_query := format(
                    'SELECT * FROM %I WHERE %I::text ILIKE %L AND user_id = %L', 
                    table_rec.table_name, 
                    column_rec.column_name, 
                    '%' || keyword || '%', 
                    user_id
                );
            ELSE
                search_query := format(
                    'SELECT * FROM %I WHERE %I::text ILIKE %L AND user_id = %L', 
                    table_rec.table_name, 
                    column_rec.column_name, 
                    '%' || keyword || '%', 
                    user_id
                );
            END IF;

            -- Execute the dynamic query
            EXECUTE search_query;
        END LOOP;
    END LOOP;
END $$;

-- \i C://Users//Doug Brown//Desktop//Dannys Stuff//Job//PreferredPartnerDB//scrapers//src//database//sample_query.sql