import os


def strip_values_from_mfa_file(filepath):
    stripped_lines = []

    with open(filepath, 'r') as f:
        for line in f.readlines():
            if line.startswith('export AWS_ACCESS_KEY_ID'):
                stripped_lines.append('export AWS_ACCESS_KEY_ID=\n')
            elif line.startswith('export AWS_SECRET_ACCESS_KEY'):
                stripped_lines.append('export AWS_SECRET_ACCESS_KEY=\n')
            elif line.startswith('export AWS_SESSION_TOKEN'):
                stripped_lines.append('export AWS_SESSION_TOKEN=\n')
            else:
                stripped_lines.append(line)

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
