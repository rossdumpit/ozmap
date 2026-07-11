# import transform
# import load
# import ingest


# data, content_type = ingest.extract()
# df, content_type = transform.transform(data, content_type)
# load.load(df)

# print("Load complete")

# if __name__ == "__main__":
#     df, content_type = transform.transform(data, content_type)
#     load.load(df)
#     print("Load complete")

import transform
import load
import ingest

if __name__ == "__main__":
    data, content_type = ingest.extract()
    df, content_type = transform.transform(data, content_type)
    load.load(df)
    print("Load complete")