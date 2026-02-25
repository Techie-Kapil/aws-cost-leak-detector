# 🚀 AWS Cloud Cost Leak Detector

A secure and automated AWS cost-leak detection system built using **Python and Boto3** to identify unused AWS resources and reduce unnecessary cloud spend.

---

## 📌 Problem

Cloud environments often accumulate unused resources that silently increase AWS bills:

- Unattached EBS Volumes  
- Stopped EC2 Instances  
- Unused Elastic IPs  
- Old EBS Snapshots  

Without visibility, these resources lead to avoidable infrastructure costs.

---

## ✅ Solution

This tool securely scans an AWS account using **read-only IAM permissions** and generates structured reports highlighting potential cost leaks — without modifying or deleting any resources.

---

## 🛠 Tech Stack

- Python 3.12  
- Boto3  
- AWS IAM (Least Privilege)  
- Docker  
- GitHub Actions (CI Automation)

---

## 🔐 Security Design

✔ Uses dedicated IAM user with **ReadOnlyAccess**  
✔ No destructive permissions  
✔ Follows **Least Privilege Principle**  
✔ Safe for production AWS accounts  

> The scanner cannot create, modify, or delete resources.

---

## 📊 What It Detects

| Resource Type | Detection Logic |
|---------------|----------------|
| EBS Volumes | `state = available` |
| EC2 Instances | `instance-state = stopped` |
| Elastic IPs | Not associated with instance |
| Snapshots | Older than defined threshold |

---

## 🐳 Run with Docker

```bash
docker pull ksaini0666/aws-cost-leak-detector

docker run --rm \
  -e AWS_REGION=ap-south-1 \
  -e AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY \
  -e AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY \
  ksaini0666/aws-cost-leak-detector \
  --region ap-south-1 --snapshot-days 30 --output json,csv
```

## 💻 Run Locally

```bash
git clone https://github.com/your-username/aws-cost-leak-detector.git
cd aws-cost-leak-detector

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python main.py --region ap-south-1 --snapshot-days 30 --output json,csv
```


### 💸 Example: Unused Elastic IP

![Unused EIP](screenshots/githubworkflow.png)





