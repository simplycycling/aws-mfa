import os


def strip_values_from_mfa_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    # Modify the lines in memory to strip out the values after the equals sign.
    updated_lines = []
    for line in lines:
        if any(var in line for var in ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN']):
            line = line.split('=')[0] + '=\n'
        updated_lines.append(line)

    # Write the stripped lines back to the file
    with open(filepath, 'w') as f:
        f.writelines(stripped_lines)


def unset_aws_env_variables():
    aws_env_vars = ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN']

    for var in aws_env_vars:
        if var in os.environ:
            del os.environ[var]


if __name__ == '__main__':
    filepath = '/home/me/.mfa'
    strip_values_from_mfa_file(filepath)
    unset_aws_env_variables()
    print("Values stripped and environment variables removed! Remember to reload your shell.")
