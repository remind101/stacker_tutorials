# Modifying and Creating Templates

In stacker resources are defined in blueprints. A blueprint is a python class that is responsible for creating a CloudFormation template. Usually this is built using troposphere.

## Troposphere

The troposphere library allows for easier creation of the AWS CloudFormation JSON by writing Python code to describe the AWS resources.

To facilitate catching CloudFormation or JSON errors early the library has property and type checking built into the classes.

*Example troposphere script to create an S3 bucket:*

```
from troposphere import Output, Ref, Template
from troposphere.s3 import Bucket, PublicRead

t = Template()

s3bucket = t.add_resource(Bucket("S3Bucket"))

t.add_output(Output(
    "BucketName",
    Value=Ref(s3bucket),
    Description="Name of S3 bucket to hold website content"
))

```

[Repo](https://github.com/cloudtools/troposphere/)

[Examples](https://github.com/cloudtools/troposphere/tree/master/examples)

## awacs

We also created a seperate library to create AWS policy objects in python because of how many different configuration options there are. Awacs and troposphere integrate together and allow you to create any desired AWS resource with proper permissions.

*Example awacs permissions:*

```
from awacs.aws import Action, Allow, Policy, Principal, Statement
from awacs.iam import ARN as IAM_ARN
from awacs.s3  import ARN as S3_ARN

account = "123456789012"
user = "user/Bob"

pd = Policy(
    Version="2012-10-17",
    Id="S3-Account-Permissions",
    Statement=[
        Statement(
            Sid="1",
            Effect=Allow,
            Principal=Principal("AWS", [IAM_ARN(account, user)]),
            Action=[Action("s3", "*")],
            Resource=[S3_ARN("my_corporate_bucket/*"),],
        ),
    ],
)
``` 

[Repo](https://github.com/cloudtools/awacs)

[Examples](https://github.com/cloudtools/awacs/tree/master/examples)


## Setting Up

Let's create a custom blueprint for our website so that anyone on the web can view it. The [AWS documentation](http://docs.aws.amazon.com/AmazonS3/latest/user-guide/static-website-hosting.html) for websites hosted on s3 tells us that we need to have the following bucket policy.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::example-bucket/*"
            ]
        }
    ]
}
```

Let's go ahead and create a directory where our custom blueprints will live.

``` mkdir local_blueprints ```

Then, let's let our configuration file know that it should be looking for blueprints in the local path and not the $PYTHON_PATH. We add `sys_path` to the top of it with our local path as the parameter. We also update our class_path to use the class of the new `Website` blueprint which we will be creating.

*Updated infra.yaml file*

```
sys_path: .

stacks:
  - name: myBucketStack
    class_path: local_blueprints.website.Website
    variables:
      Buckets:
        sampleBucket:
          WebsiteConfiguration:
            ErrorDocument: error.html
            IndexDocument: index.html

```

## Creating the blueprint

Our blueprint will be a child class of the original stacker s3 blueprint that we were using. 

If you look at the [code](https://github.com/remind101/stacker_blueprints/blob/master/stacker_blueprints/s3.py) of the blueprint you can see that we have created a method (`additional_bucket_statements`) that can be used by subclasses to add additional statements to bucket policy, we will be overriding this function and adding the suggested permissions.

>Creating classes with simple methods which can be overridden by child classes is a recommend pattern as it allows you to easily extend a class while maintaing a generic base class. 

We need create the new blueprint:

``` touch local_blueprints/website.py ```

and create a new `Website` class which inherits from the base s3 class and overrides the `additional_bucket_statements` method. 

*local_blueprints/website.py*

```
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

```

All done! 

When we run:

```
stacker build prod.env infra.yaml -i
```

we can see that our bucket policy has been updated, now when you go the the domain of the bucket that was created you should be able to see the sample webpage!