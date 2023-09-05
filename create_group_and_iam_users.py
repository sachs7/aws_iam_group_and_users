import boto3
import argparse
from botocore.exceptions import ClientError


def create_iam_group_if_not_exists(group_name, policies, iam):
    try:
        # Try to create the IAM group
        iam.create_group(GroupName=group_name)

        # Attach policies to the group
        for policy_arn in policies:
            iam.attach_group_policy(GroupName=group_name, PolicyArn=policy_arn)

        print(f"IAM group '{group_name}' created and policies attached.")

    except ClientError as e:
        if e.response["Error"]["Code"] == "EntityAlreadyExists":
            print(f"\nIAM group '{group_name}' already exists. Skipping group creation.")
        else:
            print(f"\nAn error occurred while creating IAM group: {e}")


def update_group_policies(group_name, new_policies, iam):
    try:
        # Get the current attached policies
        response = iam.list_attached_group_policies(GroupName=group_name)
        attached_policies = [
            policy["PolicyArn"] for policy in response["AttachedPolicies"]
        ]

        # Attach new policies that are not already attached
        for policy_arn in new_policies:
            if policy_arn not in attached_policies:
                iam.attach_group_policy(GroupName=group_name, PolicyArn=policy_arn)
                print(f"\nAdded policy '{policy_arn}' to group '{group_name}'.")

    except ClientError as e:
        print(f"\nAn error occurred while updating group policies: {e}")


def create_iam_user(username, group_name, password, iam):
    try:
        # Try to create the IAM user
        iam.create_user(UserName=username)

        # Add the user to the group
        iam.add_user_to_group(GroupName=group_name, UserName=username)

        print(f"\nIAM user '{username}' created and added to group '{group_name}'.")

    except ClientError as e:
        if e.response["Error"]["Code"] == "EntityAlreadyExists":
            print(f"\nIAM user '{username}' already exists. Skipping user creation.")
        else:
            print(f"\nAn error occurred while creating IAM user: {e}")

    try:
        # Create login profile with a password
        iam.create_login_profile(UserName=username, Password=password, PasswordResetRequired=False)
        print(f"\nCreated console password for IAM user '{username}'.\n")

    except ClientError as e:
        print(f"\nAn error occurred while creating console password: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Create AWS IAM users with console access."
    )
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of IAM users to create (default is 1)",
    )
    parser.add_argument("--username", required=True, help="Username for the IAM users")
    parser.add_argument("--group", required=True, help="Name of the IAM group")
    parser.add_argument("--password", required=True, help="Password for console access")
    parser.add_argument('--aws_access_key', required=True, help='AWS Access Key')
    parser.add_argument('--aws_secret_key', required=True, help='AWS Secret Access Key')

    args = parser.parse_args()

    if args.count < 1:
        print("Count must be greater than or equal to 1.")
        return

    # Specify the policies you want to attach to the group
    policies = [
        "arn:aws:iam::aws:policy/AmazonEC2FullAccess",
        "arn:aws:iam::aws:policy/AWSCloudFormationFullAccess",
        "arn:aws:iam::aws:policy/AmazonS3FullAccess",
        "arn:aws:iam::aws:policy/AmazonRDSFullAccess",
        "arn:aws:iam::aws:policy/IAMFullAccess",
    ]

    # Initialize IAM client with provided AWS keys
    iam = boto3.client('iam', aws_access_key_id=args.aws_access_key, aws_secret_access_key=args.aws_secret_key)

    create_iam_group_if_not_exists(args.group, policies, iam)
    update_group_policies(args.group, policies, iam)  # Update group policies

    for i in range(args.count):
        username = f"{args.username}_{i+1}"
        create_iam_user(username, args.group, args.password, iam)


if __name__ == "__main__":
    main()
