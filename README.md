**AWS MFA Session Script**

**Overview**

This script facilitates the process of obtaining and using AWS MFA (Multi-Factor Authentication) credentials in your local development environment. It is designed to simplify the process of generating a new session token and setting the necessary AWS environment variables for secure access to AWS services. This is particularly useful when working with the AWS CLI or AWS SDKs.

Prerequisites
- Python installed on your system.
- AWS CLI installed and configured with at least one profile.
- Your AWS IAM user should be configured for MFA.
- boto3 library installed in Python.
- tmux installed on your system (optional, for terminal multiplexing).

Usage
Step 1: Run the Script
Open a terminal and navigate to the directory containing the script. Execute the script by typing:

```
python get_new_mfa_token.py
```

Enter your MFA token when prompted. The script will generate a new file (e.g., .mfa) in your home directory. This file contains export commands to set the AWS environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_SESSION_TOKEN).

Step 2: Source the Environment Variables Automatically
To automatically load the AWS environment variables in each new shell session, add the following line to your .zshrc or .bashrc file:

```
source ~/.mfa
```

Make sure to replace ~/.mfa with the actual path to the file generated by the script. Now start a new session, either by sourcing your
.bashrc or .zshrc, or simply by closing your terminal window and opening it up again. 

Then again, you might just open a new tmux window.

Step 3: Start tmux (Optional)
If you use tmux, start a new session:

```
tmux
```

The environment variables set previously will be available in the tmux session, enabling you to use AWS CLI or SDKs with the updated credentials.

Notes
- The script only updates the environment variables for the current shell session and any child processes (like tmux sessions started from this shell).
- If you open a new terminal or shell session, the .mfa file sourced from .zshrc or .bashrc will ensure that the AWS environment variables are automatically loaded.
- Keep your MFA device handy at all times!

Troubleshooting
If you encounter any issues:

- Ensure your AWS CLI is correctly configured.
- Check that you have the necessary permissions to perform the actions in the script.
- Verify that your MFA device is working and the token you enter is correct.

For further assistance, consult AWS documentation or reach out to your AWS administrator.
