# Artifacts

*Datajudge* allows the user to interact with artifacts. It exposes some APIs to persist input data or generic artifact and to fetch them from a backend storage. The library comes with five plugin out-of-the-box for various backend:

- `Azure`
  - Support interaction with Azure blob storage (WASBS filesystem).
- `S3`
  - Support interaction with S3-based storages (e.g. AWS, Minio)
- `FTP`
- `HTTP`
- `Local filesystem`
