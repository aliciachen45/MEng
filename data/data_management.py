import boto3
import json
import os
from dotenv import load_dotenv
import random
import csv
import pandas as pd

load_dotenv()
access_key = os.getenv("AWS_ACCESS_KEY")
secret_key = os.getenv("AWS_SECRET_KEY")
bucket_name = os.getenv("BUCKET_NAME")
region = os.getenv("REGION_NAME")

s3 = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name=region,
)


def save_to_s3(data, uid):
    """
    Uploads the experiment data directly to an S3 bucket.
    """
    file_key = f"logs/{uid}.json"
    json_content = json.dumps(data, indent=2)

    try:
        s3.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json_content,
            ContentType="application/json",
        )
        print(
            f"Successfully uploaded log for {uid} to S3 bucket {bucket_name}."
        )
    except Exception as e:
        print(json_content)
        print(uid)
        print(f"FAILED to upload to S3: {e}")


def assign_participant_to_group(id):
    file_key = "tracker/assignment_counts.json"

    # Define your 6 groups
    groups = ["1", "2", "3", "4", "5", "6"]

    try:
        # 1. Try to get the existing counts
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
        group_assignments = json.loads(response["Body"].read().decode("utf-8"))
    except s3.exceptions.NoSuchKey:
        # 2. If file doesn't exist, initialize it
        group_assignments = {g: [] for g in groups}

    # 3. Find groups with the minimum number of participants
    min_count = min(len(ids) for ids in group_assignments.values())
    candidates = [
        g for g, ids in group_assignments.items() if len(ids) == min_count
    ]

    # 4. Pick one randomly from the candidates (the tied groups)
    assigned_group = random.choice(candidates)

    # 5. Increment and save back to S3
    group_assignments[assigned_group].append(id)
    s3.put_object(
        Bucket=bucket_name,
        Key=file_key,
        Body=json.dumps(group_assignments, indent=2),
        ContentType="application/json",
    )

    print(
        f"Assigned {id} to Group {assigned_group}. Current distribution: "
        f"{ {g: len(ids) for g, ids in group_assignments.items()} }"
    )

    return assigned_group


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


def get_single_log(id):
    """
    Fetch a single JSON file from S3 and return it as a Python dictionary.

    id is the unique identifier for the reponse, formated as {child_id}_{response_id}
    """
    file_key = f"logs/{id}.json"

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


def get_group_assignments():
    """
    Fetch the group assignment tracker from S3 and return it as a Python dictionary.
    """
    file_key = "tracker/assignment_counts.json"

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
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []


def clear_all_data():
    """
    WARNING: Deletes all logs in the S3 bucket under the 'logs/' prefix.
    Use with caution.
    """

    def clear_logs():
        try:
            # 1. List objects in the bucket that start with 'logs/'
            response = s3.list_objects_v2(Bucket=bucket_name, Prefix="logs")

            if "Contents" not in response:
                print("No files found to delete.")
                return

            print(f"Found {len(response['Contents'])} files. Deleting...")

            # 2. Loop through every file found and delete it
            for item in response["Contents"]:
                file_key = item["Key"]

                # Skip the folder itself if it appears as an item
                if file_key.endswith("/"):
                    continue

                s3.delete_object(Bucket=bucket_name, Key=file_key)
                print(f" - Deleted: {file_key}")

            print("All logs deleted.")

        except Exception as e:
            print(f"Error during deletion: {e}")

    def clear_groups():
        # Clearing the group assignment tracker as well
        try:
            s3.delete_object(
                Bucket=bucket_name, Key="tracker/assignment_counts.json"
            )
            print("Cleared group assignment tracker.")
        except Exception as e:
            print(f"Error clearing group assignment tracker: {e}")

    clear_logs()
    clear_groups()


def get_last_trial_info(response_id):
    """
    Checks if a log exists for the uid and returns the
    highest trial number found and the existing data.
    """
    existing_data = get_single_log(response_id)
    if not existing_data:
        return 0, 0

    # Find the maximum trial sequence number already recorded
    trial_nums = []
    scores = []
    for key, value in existing_data.items():
        if "type" in key:
            try:
                # Extract the number after 'seq_'
                num = int(key.split("_")[-1])
                trial_nums.append(num)
                scores.append(value.get("total_score", 0))
            except ValueError:
                continue
    print(f"Existing trial numbers for {response_id}: {trial_nums}")
    print(f"Existing scores for {response_id}: {scores}")

    last_num = max(trial_nums) if trial_nums else 0
    max_score = max(scores) if scores else 0
    return last_num, max_score


def flatten_log(data, inclusion_criteria=lambda x: True):
    rows = []

    status = inclusion_criteria(data)

    meta = {
        "unique_id": data.get("unique_id"),
        "child_id": data.get("child_id"),
        "response_id": data.get("response_id"),
        "group": data.get("group"),
        "status": "include" if status else "exclude",
    }

    for key, value in data.items():
        if key.startswith("trial"):
            row = meta.copy()
            trial_data = value.copy()
            if isinstance(trial_data.get("choice1"), dict):
                trial_data["choice1"] = trial_data["choice1"].get(
                    "clicked_side1", [None]
                )[0]

            row.update(trial_data)
            rows.append(row)

    return rows


def covnert_logs_to_raw_csv(logs, filename):
    rows = []

    for log in logs:
        log_rows = flatten_log(log)
        rows.extend(log_rows)

    df = pd.DataFrame(rows)

    df.to_csv(f"{filename}", index=False)

    print(f"Data successfully saved to {filename}")
    return df


def include_only_pass_training_first(data):
    """
    Returns False if any trial_type has > 1 occurrence in the Training Phase.
    """
    training_counts = {}

    for key, value in data.items():
        if key.startswith("trial"):
            if value.get("test_trial") is False:
                t_type = value.get("trial_type")

                training_counts[t_type] = training_counts.get(t_type, 0) + 1

                if training_counts[t_type] > 1:
                    return False

    return True


if __name__ == "__main__":
    # Example usage
    print(get_single_log("_"))
    # logs = get_all_logs()
    # group_assignments = get_group_assignments()
    # print(f"Total logs retrieved: {len(logs)}")
    # # print(logs[3])
    # covnert_logs_to_raw_csv(logs, "all_logs.csv")
    # print(group_assignments)
