## Installing Stacker
You can install stacker via pip

```
pip install stacker stacker_blueprints
```
and you can verify that the installation worked by running the stacker command in your shell

```
$ stacker

usage: stacker [-h] [--version] {build,destroy,info,diff} ...
stacker: error: too few arguments
```

## Credentials

In order for Stacker to work we must give it AWS credentials in some way, there are several places where stacker checks for credentials. 

1. The `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables
2. Shared credential file (*~/.aws/credentials*)
3. AWS config file (*~/.aws/config*)
4. You can specify a role using `AWS_PROFILE`

The easiest way to get your environment configured is to just use:
`aws configure` to get it working. 

## Setting Up

When running a build with stacker we will need to create 2 files, an environment file and an configuration file.

``` 
touch infra.yaml prod.env
```

### The Configuration file

The configuration file contains all the information about what infrastructure your application needs to build. We are going to write a sample configuration file that is going to create a single S3 bucket. 

Configuration files are written in the yaml file format and end with a .yaml file extension. 

Your first stacker config file: **infra.yaml**

```
stacks:
  - name: myBucketStack
    class_path: stacker_blueprints.s3.Buckets
    variables:
      Buckets:
        sampleBucket: {}
```

Let's dissect this file:

The `stacks` block is where the configuration for each stack is stored, `stacks` is a list with each list item being a seperate stack.

Every stack (collection of aws resources) has 3 mandatory parameters. The `name` is used along with the `namespace` to create a unique identifier for each stack. The `class_path` is the location of the blueprint (a blueprint is a python class which defines which AWS resources will be created for a stack, we will talk about this in more detail later). We have created a stacker_blueprints repo which contains templates for many commonly created resources but you can easily create your own. The `variables` is used indicate configuration options for the template, you can see variables a stack accepts by looking at the template that the stack is using. For now, we won't have any custom configuration for our bucket and just leave it empty.

### The Environment File

Imagine you have a production environment and a staging environment, and environment file is the place you store every thing that is different about them. This includes API Keys, ARNs for different roles and environment specific variables. For this super simple example we will create the most basic environment file possible, the only mandatory variable for an environment file is the `namespace`. 


Your first stacker config file: **prod.env**

```
namespace: prod-buckets
```     

### Launching our Stack

In order to deploy our stack to cloudformation we just have to call:

```
stacker build prod.env infra.yaml
``` 

if everything was set up correctly you should now see output similar to this

```
[2017-04-13T17:26:42] Using Default AWS Provider
[2017-04-13T17:26:42] Plan Status:
[2017-04-13T17:26:42] 	prod-buckets-myBucketStack: pending
```

after the build has completed you should go into your AWS cloudformation console and verify that a stack was created which builds the correct bucket. 

If there is an error, stacker will print out what the error is, this could be an error related to either the syntax of your configuration file or a problem trying to deploy the stack to cloudformation. 


### Next Steps

Congratulations, you have built your first of many stacks! 

>This brings us to our next part: [Configuring this S3 Bucket to be a Website](../part2)




