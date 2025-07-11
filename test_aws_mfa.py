import os
import pytest
from unittest.mock import patch, mock_open, MagicMock
import boto3
from botocore.exceptions import ClientError

import sys
import importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

spec = importlib.util.spec_from_file_location("aws_mfa", "/Users/rsherman/src/aws-mfa/aws-mfa.py")
aws_mfa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aws_mfa)

unset_aws_credentials = aws_mfa.unset_aws_credentials
get_mfa_tokens = aws_mfa.get_mfa_tokens
update_mfa_file = aws_mfa.update_mfa_file


class TestUnsetAwsCredentials:
    def test_unset_aws_credentials_removes_existing_env_vars(self):
        with patch.dict(os.environ, {
            'AWS_ACCESS_KEY_ID': 'test_access_key',
            'AWS_SECRET_ACCESS_KEY': 'test_secret_key',
            'AWS_SESSION_TOKEN': 'test_session_token'
        }):
            unset_aws_credentials()
            assert 'AWS_ACCESS_KEY_ID' not in os.environ
            assert 'AWS_SECRET_ACCESS_KEY' not in os.environ
            assert 'AWS_SESSION_TOKEN' not in os.environ

    def test_unset_aws_credentials_no_error_when_vars_not_set(self):
        with patch.dict(os.environ, {}, clear=True):
            unset_aws_credentials()


class TestGetMfaTokens:
    @patch('boto3.client')
    def test_get_mfa_tokens_success(self, mock_boto_client):
        mock_sts = MagicMock()
        mock_boto_client.return_value = mock_sts
        
        mock_credentials = {
            'AccessKeyId': 'test_access_key',
            'SecretAccessKey': 'test_secret_key',
            'SessionToken': 'test_session_token',
            'Expiration': 'test_expiration'
        }
        
        mock_sts.get_session_token.return_value = {
            'Credentials': mock_credentials
        }
        
        serial_code = 'arn:aws:iam::123456789012:mfa/test-user'
        token_code = '123456'
        
        result = get_mfa_tokens(serial_code, token_code)
        
        mock_boto_client.assert_called_once_with('sts')
        mock_sts.get_session_token.assert_called_once_with(
            DurationSeconds=86400,
            SerialNumber=serial_code,
            TokenCode=token_code
        )
        assert result == mock_credentials

    @patch('boto3.client')
    def test_get_mfa_tokens_invalid_token(self, mock_boto_client):
        mock_sts = MagicMock()
        mock_boto_client.return_value = mock_sts
        
        mock_sts.get_session_token.side_effect = ClientError(
            {'Error': {'Code': 'AccessDenied', 'Message': 'Invalid MFA token'}},
            'GetSessionToken'
        )
        
        serial_code = 'arn:aws:iam::123456789012:mfa/test-user'
        token_code = '000000'
        
        with pytest.raises(ClientError):
            get_mfa_tokens(serial_code, token_code)


class TestUpdateMfaFile:
    def test_update_mfa_file_writes_correct_format(self):
        credentials = {
            'AccessKeyId': 'test_access_key',
            'SecretAccessKey': 'test_secret_key',
            'SessionToken': 'test_session_token'
        }
        
        filepath = '/tmp/test_credentials'
        
        with patch('builtins.open', mock_open()) as mock_file:
            update_mfa_file(filepath, credentials)
            
            mock_file.assert_called_once_with(filepath, 'w')
            handle = mock_file()
            
            expected_calls = [
                ('export AWS_ACCESS_KEY_ID=test_access_key\n',),
                ('export AWS_SECRET_ACCESS_KEY=test_secret_key\n',),
                ('export AWS_SESSION_TOKEN=test_session_token\n',)
            ]
            
            actual_calls = [call[0][0] for call in handle.write.call_args_list]
            expected_strings = [call[0] for call in expected_calls]
            assert actual_calls == expected_strings

    def test_update_mfa_file_handles_file_permissions_error(self):
        credentials = {
            'AccessKeyId': 'test_access_key',
            'SecretAccessKey': 'test_secret_key',
            'SessionToken': 'test_session_token'
        }
        
        filepath = '/readonly/test_credentials'
        
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            with pytest.raises(PermissionError):
                update_mfa_file(filepath, credentials)


class TestMainScriptFlow:
    def test_script_has_main_guard(self):
        """Test that the script has proper __main__ guard"""
        with open('/Users/rsherman/src/aws-mfa/aws-mfa.py', 'r') as f:
            content = f.read()
        assert "if __name__ == '__main__':" in content
        
    def test_script_imports_successfully(self):
        """Test that the script can be imported without executing main block"""
        # This test passes if import doesn't raise an exception
        assert aws_mfa is not None
        assert hasattr(aws_mfa, 'unset_aws_credentials')
        assert hasattr(aws_mfa, 'get_mfa_tokens')
        assert hasattr(aws_mfa, 'update_mfa_file')