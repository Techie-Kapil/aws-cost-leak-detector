import boto3
from datetime import datetime, timezone


def find_old_snapshots(region: str = "ap-south-1", older_than_days: int = 30):
    ec2 = boto3.client("ec2", region_name=region)

    resp = ec2.describe_snapshots(OwnerIds=["self"])
    now = datetime.now(timezone.utc)

    results = []
    for snap in resp.get("Snapshots", []):
        start = snap["StartTime"]  # timezone-aware datetime
        age_days = (now - start).days

        if age_days >= older_than_days:
            results.append(
                {
                    "ResourceType": "EBS_SNAPSHOT",
                    "SnapshotId": snap.get("SnapshotId", ""),
                    "VolumeId": snap.get("VolumeId", ""),
                    "VolumeSizeGiB": snap.get("VolumeSize", ""),
                    "StartTime": str(start),
                    "AgeDays": age_days,
                    "Region": region,
                }
            )

    # Optional: oldest first
    results.sort(key=lambda x: x["AgeDays"], reverse=True)
    return results

