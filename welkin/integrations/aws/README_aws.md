# Configuring AWS Integration

## Table of Contents
+ [Create an AWS Account](#create-an-aws-account)
  + [Set a Budget!](#set-a-budget)
+ [Add a Framework User](#add-a-framework-user)
  + [Add a User Group and Inline Policy](#add-a-user-group-and-inline-policy)
  + [Add a User](#add-a-user)
+ [Set Up The System AWS CLI Configuration](#set-up-the-system-aws-cli-configuration)
  + [Installing AWS CLI Locally](#installing-aws-cli-locally)
  + [Configure the Local AWS CLI](#configure-the-local-aws-cli)
+ [Set your Passwords](#set-your-passwords)


Welkin can be configured to integrate with AWS, but be warned that this is a finicky and fiddly process involving a lot of non-intuitable steps. Some of these steps will have to be taken for every different system or platform that these integrations will run on. 

Currently Welkin supports using AWS for storing secrets, using the AWS Parameter Store service.

## Create an AWS Account
In order to integrate with AWS, you will need an AWS account. This documentation assumes that you don't have an existing company or organization account that you can gain access to, so it describes creating and setting up a *new* account. 

You get a range of free services with an account: [https://aws.amazon.com/free/](https://aws.amazon.com/free/). But be very, very cautious about what you build, because you can quickly move beyond the boundaries of the free offerings.

Note that the **AWS Secrets Manager** is *not* included in the free offerings. While it might be the smartest and safest solution for managing passwords, **AWS Parameter Store** will be good enough and is in the free tier.  

### Set a Budget! 
Even though you are working in the free tier, you can accidently fall out of that tier. Go to ```Dashboard --> Cost Management -->  Budgets``` and set a very low budget threshold and notification action.


## Add a Framework User
You actually need to add a **user**, a **user group**, and an inline **security policy**. This is kind of a circular process, where you have to update each of these until they are all complete.

### Add a User Group and Inline Policy
You need a **user group** that will be attached to the access permissions.

1. go to ```AWS --> Identity and Access Management (IAM) --> User groups```
2. create a group like "framework_users"
3. create an inline policy called something like "framework_access_policy"
4. Lookup the service **Systems Manager** and select that
5. Expand the **Access Level** for **Read**
6. Find and select the **Read** options **GetParameter** and **GetParameters**
7. Select the option **Specific** for **Resources** and fill in the ARN details:
   * **Region** should be the region for the framework account
   * **Account** should be the framework account
   * For the **Parameter name without leading slash**, you can either put in the specific parameter name -- and have to deal with adding each parameter separately, which improves security but is a pain -- or you can enter in **welkin/** (or other framework identifier) to allow access to all teh framework parameters. 

This gives exactly two access permissions for this group. If you add framework code that requires additional integration points, you must add the additional access actions to the policy. 


### Add a User
You need a user that represents the framework: this will provide credentials to the *framework as a user* to access the AWS parameters.

1. go to ```AWS --> Identity and Access Management (IAM) --> users```
2. create a user with a name like "framework_user"
3. add this user to the group "framework_users" (or whatever you called)

Note: You will come back to this user to generate and copy its access credentials. 
 

## Set Up The System AWS CLI Configuration
In order to interact with your framework's AWS account, you will need to set up the AWS Command Line Interface (CLI) for each system on which the framework will be run. So at the very least, you will set up your local development box. 


### Installing AWS CLI Locally
1. Get the OSX package from [https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html]()  
2. Follow the instructions on this page.

Verifying installation:
``` bash
(v3) MacBook-Pro:welkin derek$ which aws
/usr/local/bin/aws
(v3) MacBook-Pro:welkin derek$ aws --version
aws-cli/2.2.40 Python/3.8.8 Darwin/18.7.0 exe/x86_64 prompt/off
```


### Configure the Local AWS CLI
The configuration process creates a local settings files:
* ~/.aws/config
* ~/.aws/credentials

Obviously do NOT check these into project source code! 

At this point, you need to generate the access credentials for your user at ```AWS --> Identity and Access Management (IAM) --> users --> <<user>> --> access credentials```; paste those at the appropriate prompt below.

In order to create a local config file at ~/.aws, run:
``` bash
(v3) MacBook-Pro:welkin derek$ aws configure
AWS Access Key ID [None]: <<key from user record in AWS IAM>>
AWS Secret Access Key [None]: <<key from user record in AWS IAM>>
Default region name [None]: us-west-1
Default output format [None]: 
(v3) MacBook-Pro:welkin derek$ 
```


## Set your Passwords
The typical structure for application passwords looks like this:
```
tier
    |- application
        |- username
```

This yields a string path "tier/application/username". We will use this as the name for the *name* of the parameter that corresponds to the password *value*. However, we should prepend this with a node that identifies this as being a framework parameter distinct from what anybody else in our company might be doing. For example, we might prepend this with "welkin".

1. go to ```AWS --> Systems Manager --> Parameter Store```
2. create a parameter with a name that reflects the unique prepend + node path, for example "/welkin/prod/duckduckgo/user01"; that leading slash is required.
3. specific an appropriate value type
4. assign a tag that references the framework, for exmaple "ok_welkin"

You will have to repeat this for *every* password (parameter) you need to support.
