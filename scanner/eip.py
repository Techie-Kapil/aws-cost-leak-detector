import boto3


def find_unassociated_eips(region: str = "ap-south-1"):
    ec2 = boto3.client("ec2", region_name=region)
    resp = ec2.describe_addresses()

    results = []
    for addr in resp.get("Addresses", []):
        # Unused if it has no AssociationId (not attached to instance/eni)
        if "AssociationId" not in addr:
            results.append(
                {
                    "ResourceType": "EIP",
                    "PublicIp": addr.get("PublicIp", ""),
                    "AllocationId": addr.get("AllocationId", ""),
                    "Region": region,
                }
            )

    return results

