import json
from typing import List, Dict

from boto3 import Session

from hmd_cli_tools.hmd_cli_tools import (
    fibonacci_wait,
    gen_password,
    format_tags,
    get_account_number,
)


class HmdOrganizationException(Exception):
    pass


class AccountExistsException(HmdOrganizationException):
    def __init__(self, account_name):
        super().__init__(f"Account with name, {account_name}")


class AccountCreationFailedException(HmdOrganizationException):
    def __init__(self, account_name, failure_reason):
        super().__init__(
            f"Creation of account, {account_name}, failed with reason {failure_reason}."
        )


def _get_org_accounts(org_client) -> List[str]:
    """Retrieve account names in the current AWS organization.

    :param org_client: An AWS ``Session`` client of type "organizations"
    :type org_client: An AWS service client.
    :return: A list of account names.
    :rtype: List[str]
    """
    accounts = []
    continue_ = True
    next_token = None
    while continue_:
        result = (
            org_client.list_accounts(NextToken=next_token)
            if next_token
            else org_client.list_accounts()
        )
        accounts += [
            {"Id": acct["Id"], "Name": acct["Name"]} for acct in result["Accounts"]
        ]
        next_token = result.get("NextToken")
        if not next_token:
            continue_ = False

    return accounts


def list_member_accounts(org_session: Session) -> List:
    accounts = []

    for page in (
        org_session.client("organizations").get_paginator("list_accounts").paginate()
    ):
        accounts += page["Accounts"]

    return [
        a
        for a in accounts
        if a.get("Id") != get_account_number(org_session)
        and a.get("Status") == "ACTIVE"
    ]


def create_account(org_session: Session, account_name: str, account_email: str) -> Dict:
    """Create an AWS account.

    Create an AWS account as part of an AWS organization. Wait until the creation completes,
    either with success or failure, and return the status of the operation.

    The return value is of the form::

        {
            'Name': 'string',
            'Id': 'string',
        }


    :param org_session: An AWS ``Session`` object.
    :type org_session: Session
    :param account_name: The name of the new account.
    :type account_name: str
    :param account_email: The account email.
    :type account_email: str
    :raises AccountExistsException: The account name already exists within the organization.
    :raises AccountCreationFailedException: An unexpected error occurred during the account creation process.
    :return: The "CreateAccountStatus" key of the return result when creating the account.
    :rtype: Dict
    """
    org_client = org_session.client("organizations")

    result = None
    for acc in list_member_accounts(org_session):
        if account_name == acc["Name"]:
            result = acc
            return result

    result = org_client.create_account(
        Email=account_email, AccountName=account_name, IamUserAccessToBilling="DENY"
    )

    # Wait for account creation to complete...
    @fibonacci_wait(min_wait=30, terms=15)
    def check_account_create_status(request_id):
        result = org_client.describe_create_account_status(
            CreateAccountRequestId=request_id
        )

        if result["CreateAccountStatus"]["State"] == "FAILED":
            raise AccountCreationFailedException(
                account_name, result["CreateAccountStatus"]["FailureReason"]
            )
        if result["CreateAccountStatus"]["State"] == "SUCCEEDED":
            status = result["CreateAccountStatus"]
            return {"Id": status["AccountId"], "Name": status["AccountName"]}
        elif result["CreateAccountStatus"]["State"] == "FAILED":
            raise Exception(f"Account creation failed: {result['FailureReason']}")
        else:
            return False

    return check_account_create_status(result["CreateAccountStatus"]["Id"])


def get_organization_number(session: Session) -> str:
    organization = (
        session.client("organizations").describe_organization().get("Organization", {})
    )
    return organization.get("MasterAccountId", "")


def create_group(session: Session, group_name: str, aws_managed_policies: List[str]):
    iam_client = session.client("iam")
    try:
        result = iam_client.get_group(GroupName=group_name)["Group"]
    except iam_client.exceptions.NoSuchEntityException:
        result = iam_client.create_group(GroupName=group_name)["Group"]
    for policyArn in [
        f"arn:aws:iam::aws:policy/{policy}" for policy in aws_managed_policies
    ]:
        iam_client.attach_group_policy(GroupName=group_name, PolicyArn=policyArn)
    return result


def create_user(
    session: Session,
    user_name: str,
    groups: List[str] = [],
    aws_managed_policies: List[str] = [],
    gen_login_profile: bool = True,
    gen_api_keys: bool = False,
    tags: Dict = {"ad-hoc": gen_password(include_symbols=False)},
) -> Dict:
    """Create an AWS user.

    The result of the creation process is of the form::

        {
            'Path': 'string',
            'UserName': 'string',
            'UserId': 'string',
            'Arn': 'string',
            'CreateDate': datetime(2015, 1, 1),
            'PasswordLastUsed': datetime(2015, 1, 1),
            'PermissionsBoundary': {
                'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                'PermissionsBoundaryArn': 'string'
            },
            'Tags': [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ],
            'PasswordResetRequired': True|False,
            'Password': 'string'
        }

    :param session: AWS ``Session`` object.
    :type session: Session
    :param user_name: The name of the user to create.
    :type user_name: str
    :param groups: A list of IAM groups into which to put the user, defaults to []
    :type groups: List[str], optional
    :param aws_managed_policies: A list of AWS-managed policy names (just the name, not the ARN), defaults to []
    :type aws_managed_policies: List[str], optional
    :param gen_login_profile: Indicates whether to create a login profile for AWS console access, defaults to True
    :type gen_login_profile: bool, optional
    :param gen_api_keys: Indicates whether to create a set of API Keys, defaults to False
    :type gen_api_keys: bool, optional
    :param tags: Tags to be added to the role
    :type tags: Dict, optional
    :return: Information about the created user (see above).
    :rtype: Dict
    """
    iam_client = session.client("iam")
    user = iam_client.create_user(UserName=user_name, Tags=format_tags(tags))["User"]

    for policyArn in [
        f"arn:aws:iam::aws:policy/{policy}" for policy in aws_managed_policies
    ]:
        response = iam_client.attach_user_policy(
            UserName=user_name, PolicyArn=policyArn
        )

    for group in groups:
        iam_client.add_user_to_group(GroupName=group, UserName=user_name)

    if gen_login_profile:
        password = gen_password()

        login_profile = iam_client.create_login_profile(
            UserName=user_name, Password=password, PasswordResetRequired=True
        )["LoginProfile"]

        user.update(login_profile)
        user["Password"] = password

    if gen_api_keys:
        keys = iam_client.create_access_key(UserName=user_name)
        user["AccessKey"] = keys.get("AccessKey", {}).get("AccessKeyId", "")
        user["SecretAccessKey"] = keys.get("AccessKey", {}).get("SecretAccessKey", "")

    return user


def create_role(
    session: Session,
    role_name: str,
    aws_managed_policies: List[str] = [],
    assume_role_statements: List[Dict] = [],
    tags: Dict = {"ad-hoc": gen_password(include_symbols=False)},
) -> Dict:
    """Create an AWS role.

    The result of the creation process is of the form::
        {
            'Path': 'string',
            'RoleName': 'string',
            'RoleId': 'string',
            'Arn': 'string',
            'CreateDate': datetime(2015, 1, 1),
            'AssumeRolePolicyDocument': 'string',
            'Description': 'string',
            'MaxSessionDuration': 123,
            'PermissionsBoundary': {
                'PermissionsBoundaryType': 'PermissionsBoundaryPolicy',
                'PermissionsBoundaryArn': 'string'
            },
            'Tags': [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ],
            'RoleLastUsed': {
                'LastUsedDate': datetime(2015, 1, 1),
                'Region': 'string'
            }
        }

    :param session: AWS ``Session`` object.
    :type session: Session
    :param role_name: The name of the role to create.
    :type role_name: str
    :param aws_managed_policies: A list of AWS-managed policy names (just the name, not the ARN), defaults to []
    :type aws_managed_policies: List[str], optional
    :param assume_role_statements: A list of assume role resource ARNs, defaults to []
    :type assume_role_statements: List[Dict], optional
    :param tags: Tags to be added to the role
    :type tags: Dict, optional
    :return: Information about the created role (see above).
    :rtype: Dict
    """
    iam_client = session.client("iam")

    role = iam_client.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(
            {"Version": "2012-10-17", "Statement": assume_role_statements}
        ),
        Tags=format_tags(tags),
    )["Role"]

    for policy_arn in [
        f"arn:aws:iam::aws:policy/{policy}" for policy in aws_managed_policies
    ]:
        response = iam_client.attach_role_policy(
            RoleName=role_name, PolicyArn=policy_arn
        )

    return role
