# csae-pyutils
some python function used in several places

## gsheet_to_df
Converts a Google Sheet to a pandas DataFrame.

```python
sheet_id = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
df = gsheet_to_df(sheet_id)
```

## upload_files_to_owncloud
Uploads files to OEAW ownCloud instance

```python
from csae_pytuils import upload_files_to_owncloud

files = ['/path/to/file1.txt', '/path/to/file2.pdf']
result = upload_files_to_owncloud(
    file_list=files,
    user='your_username',
    pw='your_password',
    folder='my-uploads'
)
```