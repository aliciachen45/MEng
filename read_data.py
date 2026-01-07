import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
bucket_name = os.getenv("AWS_BUCKET_NAME")
region = os.getenv("AWS_REGION")

# Initialize the connection
s3 = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region,
)


def read_single_log(uid):
    """
    Fetch a single JSON file from S3 and return it as a Python dictionary.
    """
    file_key = f"logs/{uid}.json"

    try:
        # 1. Request the file from S3
        response = s3.get_object(Bucket=bucket_name, Key=file_key)

        # 2. Read the binary stream and decode it
        content = response["Body"].read().decode("utf-8")

        # 3. Parse JSON
        data = json.loads(content)
        return data

    except s3.exceptions.NoSuchKey:
        print(f"Error: File {file_key} does not exist.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_all_logs():
    """
    List ALL files in the logs folder and read them into a list.
    """
    all_data = []

    # 1. List objects in the bucket that start with 'logs/'
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix="logs")

    if "Contents" not in response:
        print("No files found.")
        return []

    print(f"Found {len(response['Contents'])} files. Downloading...")

    # 2. Loop through every file found
    for item in response["Contents"]:
        file_key = item["Key"]

        # Skip the folder itself if it appears as an item
        if file_key.endswith("/"):
            continue

        # Get the object
        obj_response = s3.get_object(Bucket=bucket_name, Key=file_key)
        content = obj_response["Body"].read().decode("utf-8")
        data = json.loads(content)

        all_data.append(data)
        print(f" - Loaded: {file_key}")

    return all_data


# --- USAGE EXAMPLES ---

# Example 1: Read one specific user
uid_to_check = "user123"
user_data = read_single_log(uid_to_check)
if user_data:
    print("User Score:", user_data.get("final_score", "N/A"))

print("-" * 20)

# Example 2: Load EVERYTHING for analysis
full_dataset = get_all_logs()
print(f"Total participants loaded: {len(full_dataset)}")
print(full_dataset)
