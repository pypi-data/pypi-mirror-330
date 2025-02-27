import asyncio
from datetime import datetime, timedelta, timezone

from dpd_lib.config import settings
from influx import InfluxClient

if __name__ == "__main__":
    client = InfluxClient(
        "dpd-test",
        settings.influx_token,
        settings.influx_org,
        settings.influx_url,
    )
    startTime: datetime = datetime.now(timezone.utc) - timedelta(hours=1)
    endTime: datetime = datetime.now(timezone.utc)

    asyncio.run(
        client.read_seismic(
            type="rsam",
            stations=["PARA"],
            t0=startTime,
            t1=endTime,
            multi_field=False,
        )
    )
    client = InfluxClient(
        "dpd-test",
        settings.influx_token,
        settings.influx_org,
        settings.influx_url,
    )
    asyncio.run(
        client.read_seismic(
            type="spectra",
            stations=["PARA"],
            t0=startTime,
            t1=endTime,
            multi_field=True,
            plot_results=True,
        )
    )

    # Testing Tripwires insert and read
    client = InfluxClient(
        settings.influx_bucket,
        settings.influx_token,
        settings.influx_org,
        settings.influx_url,
    )
    result_dict = {
        "Trip Wire Upper": 1.0,
        "Trip Wire Middle": 1.0,
        "Trip Wire Lower": 1.0,
    }
    timestamp: datetime = datetime.now(timezone.utc)
    asyncio.run(
        client.record_tripwires(
            type="state",
            station="PR01",
            drainage="N/A",
            riverDist="N/A",
            volcano="Testing",
            timestamp=timestamp,
            field_keys=list(result_dict.keys()),
            field_values=list(
                result_dict.values(),
            ),
        )
    )

    asyncio.run(
        client.read_tripwires(
            type="state",
            stations=["PR01"],
            t0=startTime,
            t1=endTime,
            multi_field=True,
        )
    )
