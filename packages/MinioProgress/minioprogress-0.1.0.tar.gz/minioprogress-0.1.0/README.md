# MinioProgress

A progressbar for minio upload.

You can import this lib and put the progress class into any
minio operation and it will show a progressbar.

# Example

```python
# Import
from MinioProgress.Progress import Progress

# Example with fput_object
client.fput_object(
    "my-bucket", "my-object", "my-filename",
    progress=Progress() # Pass the Progress class
)
```
