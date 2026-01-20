import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

import argparse

from scanner.ebs import find_unattached_volumes
from scanner.ec2 import find_stopped_instances
from scanner.eip import find_unassociated_eips
from scanner.snapshots import find_old_snapshots
from reporting.report import save_csv, save_json


def main():
    parser = argparse.ArgumentParser(
        description="AWS Cost Leak Detector (Safe FinOps Scanner)"
    )
    parser.add_argument("--region", default="ap-south-1", help="AWS region to scan")
    parser.add_argument(
        "--snapshot-days",
        type=int,
        default=30,
        help="Detect EBS snapshots older than N days",
    )
    parser.add_argument(
        "--output",
        default="json,csv",
        help="Comma-separated formats: json,csv",
    )

    args = parser.parse_args()
    region = args.region
    snapshot_days = args.snapshot_days
    formats = {f.strip().lower() for f in args.output.split(",") if f.strip()}

    volumes = find_unattached_volumes(region=region)
    instances = find_stopped_instances(region=region)
    eips = find_unassociated_eips(region=region)
    snaps = find_old_snapshots(region=region, older_than_days=snapshot_days)

    all_findings = [*volumes, *instances, *eips, *snaps]

    print(f"\nRegion: {region}")
    print(f"EBS Unattached Volumes: {len(volumes)}")
    print(f"EC2 Stopped Instances:  {len(instances)}")
    print(f"Unused Elastic IPs:     {len(eips)}")
    print(f"Old Snapshots ({snapshot_days}d+): {len(snaps)}")
    print(f"Total Findings:         {len(all_findings)}")

    if not all_findings:
        print("\n✅ Overall: No cost-leak candidates found.")
        return

    print("\n📄 Reports generated:")
    if "json" in formats:
        print("- JSON:", save_json(all_findings))
    if "csv" in formats:
        print("- CSV: ", save_csv(all_findings))


if __name__ == "__main__":
    main()

