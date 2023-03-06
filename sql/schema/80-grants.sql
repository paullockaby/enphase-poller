GRANT USAGE ON SCHEMA public TO solar;
GRANT SELECT,INSERT ON TABLE public.production TO solar;
GRANT SELECT,INSERT ON TABLE public.consumption TO solar;
GRANT SELECT,INSERT ON TABLE public.inverter TO solar;

-- only enable this user if you want to use grafana or something
GRANT USAGE ON SCHEMA public TO readonly;
GRANT SELECT ON TABLE public.production TO readonly;
GRANT SELECT ON TABLE public.consumption TO readonly;
GRANT SELECT ON TABLE public.inverter TO readonly;
