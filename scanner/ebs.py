import boto3


def find_unattached_volumes(region: str = "ap-south-1"):
    ec2 = boto3.client("ec2", region_name=region)

    volumes = ec2.describe_volumes(
        Filters=[{"Name": "status", "Values": ["available"]}]
    )["Volumes"]

    results = []
    for vol in volumes:
        results.append(
            {
                "ResourceType": "EBS_VOLUME",
                "VolumeId": vol["VolumeId"],
                "SizeGiB": vol["Size"],
                "Region": region,
                "CreateTime": str(vol["CreateTime"]),
            }
        )

    return results

