import boto3


def find_stopped_instances(region: str = "ap-south-1"):
    ec2 = boto3.client("ec2", region_name=region)

    resp = ec2.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": ["stopped"]}]
    )

    results = []
    for reservation in resp.get("Reservations", []):
        for inst in reservation.get("Instances", []):
            name = ""
            for tag in inst.get("Tags", []):
                if tag.get("Key") == "Name":
                    name = tag.get("Value", "")
                    break

            results.append(
                {
                    "ResourceType": "EC2_INSTANCE",
                    "InstanceId": inst["InstanceId"],
                    "Name": name,
                    "InstanceType": inst.get("InstanceType", ""),
                    "State": inst.get("State", {}).get("Name", ""),
                    "Region": region,
                }
            )

    return results

