import transform
import load


df, content_type = transform.transform()
load.load(df)

print("Load complete")