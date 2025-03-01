import os

from aws_cdk import Stack, Aws, triggers
from aws_cdk.aws_iam import PolicyDocument, PolicyStatement, Effect, ManagedPolicy, Role, ServicePrincipal
from constructs import Construct

import aws_cdk.aws_lambda as lambda_


class IamSsmStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        sagemaker_role_arn = self.node.try_get_context("sagemaker_role")
        sagemaker_role = Role.from_role_arn(self, "sagemaker_role", role_arn=sagemaker_role_arn)

        user_role_arn = self.node.try_get_context("user_role")
        user_role = Role.from_role_arn(self, "user_role", role_arn=user_role_arn)

        # noinspection PyUnusedLocal
        ssh_client_policy = \
            ManagedPolicy(self, "SSHSageMakerClientPolicy",
                          managed_policy_name="SSHSageMakerClientPolicy",
                          document=PolicyDocument(statements=[
                              PolicyStatement(
                                  effect=Effect.ALLOW,
                                  actions=[
                                      "ssm:DescribeInstanceInformation",
                                      "ssm:ListTagsForResource",
                                      "ssm:GetCommandInvocation",
                                  ],
                                  resources=["*"]
                              ),
                              PolicyStatement(
                                  effect=Effect.ALLOW,
                                  actions=[
                                      "ssm:StartSession",
                                      "ssm:SendCommand",
                                  ],
                                  resources=[f"arn:{Aws.PARTITION}:ssm:*:{Aws.ACCOUNT_ID}:managed-instance/mi-*"],
                                  conditions={
                                      "StringEquals": {
                                          "ssm:resourceTag/SSHOwner": "${aws:userid}"
                                      }
                                  }
                              ),
                              PolicyStatement(
                                  effect=Effect.ALLOW,
                                  actions=[
                                      "ssm:TerminateSession",
                                  ],
                                  resources=[f"arn:{Aws.PARTITION}:ssm:*:{Aws.ACCOUNT_ID}:session/*"],
                                  conditions={
                                      "StringLike": {
                                          "ssm:resourceTag/aws:ssmmessages:session-id": "${aws:userid}"
                                      }
                                  }
                              ),
                              PolicyStatement(
                                  effect=Effect.ALLOW,
                                  actions=[
                                      "ssm:StartSession",
                                  ],
                                  resources=[
                                      f"arn:{Aws.PARTITION}:ssm:*::document/AWS-StartSSHSession",
                                      f"arn:{Aws.PARTITION}:ssm:*:{Aws.ACCOUNT_ID}:document/SSM-SessionManagerRunShell"
                                  ]
                              ),
                              PolicyStatement(
                                  effect=Effect.ALLOW,
                                  actions=[
                                      "ssm:SendCommand",
                                  ],
                                  resources=[f"arn:{Aws.PARTITION}:ssm:*::document/AWS-RunShellScript"]
                              ),
                              PolicyStatement(
                                  effect=Effect.ALLOW,
                                  actions=[
                                      "logs:StartQuery",
                                  ],
                                  resources=[f"arn:{Aws.PARTITION}:logs:*:{Aws.ACCOUNT_ID}:log-group:/aws/sagemaker/*"]
                              ),
                              PolicyStatement(
                                  effect=Effect.ALLOW,
                                  actions=[
                                      "logs:GetQueryResults",
                                  ],
                                  resources=["*"]
                              ),
                          ]))

        # noinspection PyUnusedLocal
        ssh_server_policy = \
            ManagedPolicy(self, "SSHSageMakerServerPolicy",
                          managed_policy_name="SSHSageMakerServerPolicy",
                          document=PolicyDocument(statements=[
                              PolicyStatement(
                                  effect=Effect.ALLOW,
                                  actions=[
                                      "iam:PassRole",
                                  ],
                                  resources=[sagemaker_role.role_arn],
                                  conditions={
                                      "StringEquals": {
                                          "iam:PassedToService": "ssm.amazonaws.com"
                                      }
                                  }
                              ),
                              PolicyStatement(
                                  effect=Effect.ALLOW,
                                  actions=[
                                      "ssm:AddTagsToResource",
                                  ],
                                  resources=[sagemaker_role.role_arn],
                              ),
                              PolicyStatement(
                                  effect=Effect.ALLOW,
                                  actions=[
                                      "ssm:CreateActivation",
                                      "ssm:ListAssociations",
                                      "ssm:ListInstanceAssociations",
                                      "ec2messages:GetMessages",
                                      "ec2messages:AcknowledgeMessage",
                                      "ec2messages:SendReply",
                                      "ec2messages:DeleteMessage",
                                      "ssmmessages:CreateControlChannel",
                                      "ssmmessages:CreateDataChannel",
                                      "ssmmessages:OpenControlChannel",
                                      "ssmmessages:OpenDataChannel"
                                  ],
                                  resources=["*"]
                              ),
                              PolicyStatement(
                                  effect=Effect.ALLOW,
                                  actions=[
                                      "ssm:UpdateInstanceInformation",
                                  ],
                                  resources=[f"arn:{Aws.PARTITION}:ssm:*:{Aws.ACCOUNT_ID}:managed-instance/mi-*"],
                                  conditions={
                                      "StringLike": {
                                          "ssm:resourceTag/SSHOwner": "*"
                                      }
                                  }
                              ),
                          ]))

        ssh_server_policy.attach_to_role(sagemaker_role)
        ssh_client_policy.attach_to_role(user_role)

        with open(os.path.join(os.path.dirname(__file__), "trust_relationship_lambda.py")) as lambda_path:
            code = lambda_path.read()

        code = code.replace("<<SAGEMAKER_ROLE_ARN>>", sagemaker_role.role_name)

        role = Role(self, "TrustRelationshipLambdaRole",
                    assumed_by=ServicePrincipal("lambda.amazonaws.com"),
                    inline_policies={
                        "TrustRelationshipLambdaPolicy": PolicyDocument(statements=[
                            PolicyStatement(
                                effect=Effect.ALLOW,
                                actions=["iam:UpdateAssumeRolePolicy"],
                                resources=[sagemaker_role_arn]
                            )
                        ])})

        triggers.TriggerFunction(self, "TrustRelationshipLambdaTrigger",
                                 runtime=lambda_.Runtime.PYTHON_3_9,
                                 role=role,
                                 handler="index.handler",
                                 code=lambda_.Code.from_inline(code))
