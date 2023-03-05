DO $$
    BEGIN
        IF EXISTS (SELECT 1 FROM pg_catalog.pg_available_extensions WHERE name = 'pg_partman' AND name NOT IN (SELECT extname FROM pg_catalog.pg_extension)) THEN
            CREATE SCHEMA partman;
            CREATE EXTENSION pg_partman SCHEMA partman;

            DELETE FROM partman.part_config WHERE parent_table = 'public.inverter';
            DELETE FROM partman.part_config WHERE parent_table = 'public.production';
            DELETE FROM partman.part_config WHERE parent_table = 'public.consumption';

            DROP TABLE IF EXISTS partman.template_public_inverter;
            DROP TABLE IF EXISTS partman.template_public_production;
            DROP TABLE IF EXISTS partman.template_public_consumption;

            PERFORM partman.create_parent(
                           p_parent_table := 'public.inverter',
                           p_control := 'last_report_date',
                           p_type := 'native',
                           p_interval := 'monthly',
                           p_start_partition := date_trunc('month', now())::text
                       );
            PERFORM partman.create_parent(
                           p_parent_table := 'public.production',
                           p_control := 'reading_time',
                           p_type := 'native',
                           p_interval := 'monthly',
                           p_start_partition := date_trunc('month', now())::text
                       );
            PERFORM partman.create_parent(
                           p_parent_table := 'public.consumption',
                           p_control := 'reading_time',
                           p_type := 'native',
                           p_interval := 'monthly',
                           p_start_partition := date_trunc('month', now())::text
                       );

            DROP TABLE public.inverter_default;
            DROP TABLE public.production_default;
            DROP TABLE public.consumption_default;
        ELSE
            CREATE TABLE public.inverter PARTITION OF public.inverter DEFAULT;
            CREATE TABLE public.production PARTITION OF public.production DEFAULT;
            CREATE TABLE public.consumption PARTITION OF public.consumption DEFAULT;
        END IF;
    END
$$;
