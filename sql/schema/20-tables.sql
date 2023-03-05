CREATE TABLE public.production (
    reading_time timestamp with time zone DEFAULT statement_timestamp() NOT NULL,
    apprnt_pwr numeric(12, 3) not null,
    pwr_factor numeric(12, 3) not null,
    react_pwr numeric(12, 3) not null,
    rms_current numeric(12, 3) not null,
    rms_voltage numeric(12, 3) not null,
    vah_today numeric(12, 3) not null,
    vah_lifetime numeric(15, 3) not null,
    varh_lag_today numeric(12, 3) not null,
    varh_lag_lifetime numeric(15, 3) not null,
    varh_lead_today numeric(12, 3) not null,
    varh_lead_lifetime numeric(15, 3) not null,
    w_now numeric(12, 3) not null,
    wh_today numeric(12, 3) not null,
    wh_last7days numeric(15, 3) not null,
    wh_lifetime numeric(15, 3) not null
)
PARTITION BY RANGE (reading_time);

CREATE TABLE public.consumption (
    reading_time timestamp with time zone DEFAULT statement_timestamp() NOT NULL,
    apprnt_pwr numeric(12, 3) not null,
    pwr_factor numeric(12, 3) not null,
    react_pwr numeric(12, 3) not null,
    rms_current numeric(12, 3) not null,
    rms_voltage numeric(12, 3) not null,
    vah_today numeric(12, 3) not null,
    vah_lifetime numeric(15, 3) not null,
    varh_lag_today numeric(12, 3) not null,
    varh_lag_lifetime numeric(15, 3) not null,
    varh_lead_today numeric(12, 3) not null,
    varh_lead_lifetime numeric(15, 3) not null,
    w_now numeric(12, 3) not null,
    wh_today numeric(12, 3) not null,
    wh_last7days numeric(15, 3) not null,
    wh_lifetime numeric(15, 3) not null
)
PARTITION BY RANGE (reading_time);

CREATE TABLE public.inverter (
    last_report_date timestamp with time zone DEFAULT statement_timestamp() NOT NULL,
    dev_type smallint not null,
    serial_number text not null,
    last_report_watts smallint not null,
    max_report_watts smallint not null,
    unique (last_report_date, serial_number, dev_type)
)
PARTITION BY RANGE (last_report_date);
