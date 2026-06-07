from dagster import asset
from dagster import Definitions
from dagster import ScheduleDefinition
from dagster import define_asset_job
import ingest
import transform
import load

@asset
def raw_data():
    data, content_type = ingest.extract()
    return data, content_type

@asset
def transformed_data(raw_data):
    data, content_type = raw_data
    df, content_type = transform.transform(data, content_type)
    return df

@asset
def ed_pres_table(transformed_data):
    load.load(transformed_data)



aihw_job = define_asset_job(
    name="aihw_pipeline",
    selection=[raw_data, transformed_data, ed_pres_table]
)

yearly_schedule = ScheduleDefinition(
    job=aihw_job,
    cron_schedule="0 9 1 7 *"
)

defs = Definitions(
    assets=[raw_data, transformed_data, ed_pres_table],
    jobs=[aihw_job],
    schedules=[yearly_schedule]
)