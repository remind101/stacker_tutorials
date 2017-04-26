from stacker_blueprints.s3 import Buckets
from awacs.aws import (Statement, Principal)
from awacs import s3
from troposphere import Join

class Website(Buckets):

    # Override method from Buckets class
    def additional_bucket_statements(self, bucket_arn):
        return[Statement(
            Effect="Allow",
            # This permission applies to the s3.GetObject method
            Action=[s3.GetObject],
            # This permission applies to anyone ('*')
            Principal=Principal("*"),
            # Applying policy to every object in bucket
            Resource=[Join("/", [bucket_arn, "*"])]
        )]
