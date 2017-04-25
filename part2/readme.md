# Updating your Stacks

Stacker gives teams the ability to version control their infrastructure just as they would with all their other code. Stacker will detect what has changed in your configurations and only update the resources which need to be changed. 


## Changing Configuration

Let's say that we wanted this s3 bucket to function as a website that is accessible to anyone. We will need to update our bucket stack and redeploy it. 

We update infra.yaml to contain the new website configuration information. This configuration means that when we navigate to the bucket url we will get served up the index.html page.

**infra.yaml**

```
stacks:
  - name: myBucketStack
    class_path: stacker_blueprints.s3.Buckets
    variables:
      Buckets:
        sampleBucket:
          WebsiteConfiguration:
            ErrorDocument: error.html
            IndexDocument: index.html

```


## Preview and deploy

Let's run stacker build with interactive mode (-i flag) turned on, this mode will show you what will be updated in your stack and ask you for confirmation before you actually roll it out. 

>Note: to view a list of all the other flags just run, `stacker` and `stacker build` in your terminal.

So let's run the command:

`stacker build prod.env infra.yaml -i`

this should result in:

```
[2017-04-24T15:41:39] Using Interactive AWS Provider
[2017-04-24T15:41:39] Plan Status:
[2017-04-24T15:41:39] 	prod-buckets-myBucketStack: pending
[2017-04-24T15:41:48] prod-buckets-myBucketStack changes:
Changes:
- Modify sampleBucket (AWS::S3::Bucket)
Execute the above changes? [y/n/v] 
```

we can type `v` for verbose mode to see a more detailed explanation of what changes we are actually deploying. This should look like:

```
Changes:
- Modify sampleBucket (AWS::S3::Bucket)
Execute the above changes? [y/n/v] v
[2017-04-24T15:43:15] Full changeset:
- ResourceChange:
    Action: Modify
    Details:
    - ChangeSource: DirectModification
      Evaluation: Static
      Target: {Attribute: Properties, Name: WebsiteConfiguration, RequiresRecreation: Never}
    LogicalResourceId: sampleBucket
    PhysicalResourceId: prod-buckets-mybucketstack-samplebucket-1pwgs8yplchmi
    Replacement: 'False'
    ResourceType: AWS::S3::Bucket
    Scope: [Properties]
  Type: Resource

Execute the above changes? [y/n] 
```

We can see that we are simply modifying a bucket and not replacing or recreating it, this changelog information can be really useful when deploying risky updates to mission critical resources. Let's go ahead and enter `y` to deploy the changes. 

And that's it we have just updated our bucket.


## Getting output information

In order to see the resources that were created by stacker we have 2 options, we can either log into the AWS console or we can use the `stacker info` command. If you run:

```stacker info prod.env infra.yaml```

you should get output similar to this (your values will be different because AWS dynamically generates them)

```
[2017-04-24T17:08:58] Using Default AWS Provider
[2017-04-24T17:08:58] Outputs for stacks: prod-buckets
[2017-04-24T17:08:58] prod-buckets-myBucketStack:
[2017-04-24T17:08:58] 	sampleBucketBucketId: prod-buckets-mybucketstack-samplebucket-1pwgs8yplchmi
[2017-04-24T17:08:58] 	sampleBucketBucketArn: arn:aws:s3:::prod-buckets-mybucketstack-samplebucket-1pwgs8yplchmi
[2017-04-24T17:08:58] 	sampleBucketBucketDomainName: prod-buckets-mybucketstack-samplebucket-1pwgs8yplchmi.s3.amazonaws.com
```

we created a bucket that has an id represented by the value `sampleBucketBucketId`, an arn represented by `sampleBucketBucketArn` and lives at the URL at `sampleBucketBucketDomainName`. 

We still have not uploaded our files to the website so we upload them using the aws command line tool. Replace the value's with the ones that were in your output. 

```
aws s3 mv ./index.html s3://sampleBucketBucketId/
aws s3 mv ./error.html s3://sampleBucketBucketId/
```

Now, if we go to the `prod-buckets-mybucketstack-samplebucket-1pwgs8yplchmi.s3.amazonaws.com` url we see a...

```
<Error>
	<Code>AccessDenied</Code>
	<Message>Access Denied</Message>
	<RequestId>FA8DF3A5F1C4364A</RequestId>
	<HostId>
	k+cycsrtKMjGu0Q3hngW9j1X1dOrHur0mCWmk2Xna4ct9QHutoMStQilA2bFrwpxVNwnJFYl8cc=
	</HostId>
</Error>
```

This is because the bucket does not have the permissions (explanation of what permissions) to be viewed publically by anyone, this means that we have to edit and add a bucket policy to our template.

This brings us to our next part: [Modifying and Creating Templates](../part3)