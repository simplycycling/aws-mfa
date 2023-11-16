import sys
import boto3
import os


def unset_aws_credentials():
    os.environ.pop('AWS_ACCESS_KEY_ID', None)
    os.environ.pop('AWS_SECRET_ACCESS_KEY', None)
    os.environ.pop('AWS_SESSION_TOKEN', None)


def get_mfa_tokens(serial_code, token_code):
    sts = boto3.client('sts')
    response = sts.get_session_token(
        DurationSeconds=86400,
        SerialNumber=serial_code,
        TokenCode=token_code
    )

    return response['Credentials']


def update_mfa_file(filepath, credentials):
    with open(filepath, 'w') as f:
        f.write(f"export AWS_ACCESS_KEY_ID={credentials['AccessKeyId']}\n")
        f.write(f"export AWS_SECRET_ACCESS_KEY={credentials['SecretAccessKey']}\n")
        f.write(f"export AWS_SESSION_TOKEN={credentials['SessionToken']}\n")


if __name__ == '__main__':

    unset_aws_credentials()
    serial_number = # your mfa serial number
    filepath = # the path to your aws credentials file

    token = input("Enter MFA token: ")

    if not token:
        print("No token provided. Exiting.")
        sys.exit(1)

credentials = get_mfa_tokens(serial_number, token)
update_mfa_file(filepath, credentials)
print("MFA token updated!")
