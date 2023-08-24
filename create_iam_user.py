import boto3
import argparse

def create_iam_user(username):
    # Create an IAM client
    iam = boto3.client('iam')
    
    # Create the IAM user
    iam.create_user(UserName=username)
    
    # Attach a policy that grants full access to EC2, CloudFormation, S3, and RDS
    policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
    iam.attach_user_policy(UserName=username, PolicyArn=policy_arn)
    
    policy_arn = "arn:aws:iam::aws:policy/AWSCloudFormationFullAccess"
    iam.attach_user_policy(UserName=username, PolicyArn=policy_arn)
    
    policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
    iam.attach_user_policy(UserName=username, PolicyArn=policy_arn)

    policy_arn = "arn:aws:iam::aws:policy/AmazonRDSFullAccess"
    iam.attach_user_policy(UserName=username, PolicyArn=policy_arn)

    print(f"IAM user '{username}' created with full permissions.")

def main():
    parser = argparse.ArgumentParser(description='Create AWS IAM users with full permissions for EC2, CloudFormation, S3, and RDS')
    parser.add_argument('--count', type=int, default=1, help='Number of IAM users to create (default is 1)')
    parser.add_argument('--username', required=True, help='Username for the IAM users')

    args = parser.parse_args()
    
    if args.count < 1:
        print("Count must be greater than or equal to 1.")
        return
    
    for i in range(args.count):
        username = f"{args.username}_{i+1}"
        create_iam_user(username)

if __name__ == '__main__':
    main()

