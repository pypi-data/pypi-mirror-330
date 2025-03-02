from  fioriapps_downloader.fioriapps_downloader import download_fiori_apps_csv
import pandas as pd
import io
#
csv_bytes = download_fiori_apps_csv()
csv_buffer = io.BytesIO(csv_bytes)  # type: ignore
df = pd.read_csv(csv_buffer)  # type: ignore
num_rows = len(df)
print(f"The number of rows downloaded: {num_rows}")
