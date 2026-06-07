import transform
import load
import ingest


data, content_type = ingest.extract()
df, content_type = transform.transform(data, content_type)
load.load(df)

print("Load complete")