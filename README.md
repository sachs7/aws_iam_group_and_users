# Create IAM Users with the Required Permissions

Make sure you have the Boto3 library installed (`pip install boto3`) and have configured your AWS credentials using aws configure or environment variables (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY) before running the script.

You can run this script from the command line, and it will create the specified number of IAM users with full permissions to EC2, CloudFormation, S3, and RDS.

For example, to create three users, you can run:

```
python3 create_iam_user.py --username user --count 3
```


# Recommended way

AWS recommends first creating a User Group and then adding required permissions to it, then associating the user with that group.

```
python3 create_group_and_iam_users.py --username myuser --count 2 --group mygroup --password xbauvgc --aws_access_key YOUR_ACCESS_KEY --aws_secret_key YOUR_SECRET_KEY
```

**Example Runs:**

When the user/groups exist but creating a new Console password:

```
(base) ➜✗ python3 create_group_and_iam_users.py --username myuser --count 2 --group mygroup --password xboiugd --aws_access_key YOUR_ACCESS_KEY --aws_secret_key YOUR_SECRET_KEY

IAM group 'mygroup' already exists. Skipping group creation.

IAM user 'myuser_1' already exists. Skipping user creation.

Created console password for IAM user 'myuser_1'.

IAM user 'myuser_2' already exists. Skipping user creation.

Created console password for IAM user 'myuser_2'.
```


When the user/groups exist and the users have console password created:

```
(base) ➜✗ python3 create_group_and_iam_users.py --username myuser --count 2 --group mygroup --password xoiudfkgjh --aws_access_key YOUR_ACCESS_KEY --aws_secret_key YOUR_SECRET_KEY

IAM group 'mygroup' already exists. Skipping group creation.

IAM user 'myuser_1' already exists. Skipping user creation.

An error occurred while updating console password: An error occurred (EntityAlreadyExists) when calling the CreateLoginProfile operation: Login Profile for user myuser_1 already exists.

IAM user 'myuser_2' already exists. Skipping user creation.

An error occurred while updating console password: An error occurred (EntityAlreadyExists) when calling the CreateLoginProfile operation: Login Profile for user myuser_2 already exists.
 
```
