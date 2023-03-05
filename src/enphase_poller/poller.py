import importlib.metadata
import json
import logging
from datetime import datetime

import psycopg
import requests
import tenacity

logger = logging.getLogger(__name__)


def get_version(package_name: str = __name__) -> str:
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        return "0.0.0"


class APIClient:
    def __init__(self: "APIClient", api_url: str) -> None:
        self.api_url = api_url
        self.session = requests.session()
        self.session.headers.update({"User-Agent": ""})

    @tenacity.retry(
        stop=(tenacity.stop_after_delay(30)),
        wait=tenacity.wait_random(min=1, max=2),
        before_sleep=tenacity.before_sleep_log(logger, logging.ERROR),
        reraise=True,
    )
    def call(self: "APIClient", path: str) -> dict:
        api_url = self.api_url.rstrip("/")
        path = path.lstrip("/")
        result = self.session.get(f"{api_url}/{path}")
        result.raise_for_status()

        try:
            return result.json()
        except json.JSONDecodeError:
            logger.error("received invalid data from API:")
            logger.error(result.content)
            raise


def run(
    api_url: str,
) -> None:
    client = APIClient(api_url)

    data = {
        "production": client.call("/production.json"),
        "inverters": client.call("/api/v1/production/inverters"),
    }

    inverter_data = []
    for inverter in data["inverters"]:
        inverter_data.append(
            {
                "last_report_date": datetime.fromtimestamp(inverter["lastReportDate"]),
                "dev_type": inverter["devType"],
                "serial_number": inverter["serialNumber"],
                "last_report_watts": inverter["lastReportWatts"],
                "max_report_watts": inverter["maxReportWatts"],
            },
        )

    production_data = {}
    for datum in data["production"]["production"]:
        if datum.get("measurementType", "") == "production":
            production_data = {
                "reading_time": datetime.fromtimestamp(datum["readingTime"]),
                "apprnt_pwr": datum["apprntPwr"],
                "pwr_factor": datum["pwrFactor"],
                "react_pwr": datum["reactPwr"],
                "rms_current": datum["rmsCurrent"],
                "rms_voltage": datum["rmsVoltage"],
                "vah_today": datum["vahToday"],
                "vah_lifetime": datum["vahLifetime"],
                "varh_lag_today": datum["varhLagToday"],
                "varh_lag_lifetime": datum["varhLagLifetime"],
                "varh_lead_today": datum["varhLeadToday"],
                "varh_lead_lifetime": datum["varhLeadLifetime"],
                "w_now": datum["wNow"],
                "wh_today": datum["whToday"],
                "wh_last7days": datum["whLastSevenDays"],
                "wh_lifetime": datum["whLifetime"],
            }

    consumption_data = {}
    for datum in data["production"]["consumption"]:
        if datum.get("measurementType", "") == "total-consumption":
            consumption_data = {
                "reading_time": datetime.fromtimestamp(datum["readingTime"]),
                "apprnt_pwr": datum["apprntPwr"],
                "pwr_factor": datum["pwrFactor"],
                "react_pwr": datum["reactPwr"],
                "rms_current": datum["rmsCurrent"],
                "rms_voltage": datum["rmsVoltage"],
                "vah_today": datum["vahToday"],
                "vah_lifetime": datum["vahLifetime"],
                "varh_lag_today": datum["varhLagToday"],
                "varh_lag_lifetime": datum["varhLagLifetime"],
                "varh_lead_today": datum["varhLeadToday"],
                "varh_lead_lifetime": datum["varhLeadLifetime"],
                "w_now": datum["wNow"],
                "wh_today": datum["whToday"],
                "wh_last7days": datum["whLastSevenDays"],
                "wh_lifetime": datum["whLifetime"],
            }

    # use environment variables to connect
    with psycopg.connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
                INSERT INTO public.production (
                    reading_time,
                    apprnt_pwr, pwr_factor, react_pwr,
                    rms_current, rms_voltage,
                    vah_today, vah_lifetime,
                    varh_lag_today, varh_lag_lifetime, varh_lead_today, varh_lead_lifetime,
                    w_now, wh_today, wh_last7days, wh_lifetime
                )
                VALUES (
                    %(reading_time)s,
                    %(apprnt_pwr)s, %(pwr_factor)s, %(react_pwr)s,
                    %(rms_current)s, %(rms_voltage)s,
                    %(vah_today)s, %(vah_lifetime)s,
                    %(varh_lag_today)s, %(varh_lag_lifetime)s, %(varh_lead_today)s, %(varh_lead_lifetime)s,
                    %(w_now)s, %(wh_today)s, %(wh_last7days)s, %(wh_lifetime)s
                )
            """,
            production_data,
        )

        cur.execute(
            """
                INSERT INTO public.consumption (
                    reading_time,
                    apprnt_pwr, pwr_factor, react_pwr,
                    rms_current, rms_voltage,
                    vah_today, vah_lifetime,
                    varh_lag_today, varh_lag_lifetime, varh_lead_today, varh_lead_lifetime,
                    w_now, wh_today, wh_last7days, wh_lifetime
                )
                VALUES (
                    %(reading_time)s,
                    %(apprnt_pwr)s, %(pwr_factor)s, %(react_pwr)s,
                    %(rms_current)s, %(rms_voltage)s,
                    %(vah_today)s, %(vah_lifetime)s,
                    %(varh_lag_today)s, %(varh_lag_lifetime)s, %(varh_lead_today)s, %(varh_lead_lifetime)s,
                    %(w_now)s, %(wh_today)s, %(wh_last7days)s, %(wh_lifetime)s
                )
            """,
            consumption_data,
        )

        cur.executemany(
            """
                INSERT INTO public.inverter (
                    last_report_date,
                    dev_type, serial_number,
                    last_report_watts, max_report_watts
                )
                VALUES (
                    %(last_report_date)s,
                    %(dev_type)s, %(serial_number)s,
                    %(last_report_watts)s, %(max_report_watts)s
                )
                ON CONFLICT DO NOTHING
            """,
            inverter_data,
        )

        conn.commit()
