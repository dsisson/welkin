# Configuring AWS Integration

## Table of Contents
+ [Setting Up the AWS Integration](#setting-up-the-aws-integration)
  + [Create an AWS Account](#create-an-aws-account)
    + [Set a Budget!](#set-a-budget)
  + [Add a Framework User](#add-a-framework-user)
    + [Add a User Group and Inline Policy](#add-a-user-group-and-inline-policy)
    + [Add a User](#add-a-user)
  + [Set Up The System AWS CLI Configuration](#set-up-the-system-aws-cli-configuration)
    + [Installing AWS CLI Locally](#installing-aws-cli-locally)
    + [Configure the Local AWS CLI](#configure-the-local-aws-cli)
  + [Set your Passwords](#set-your-passwords)
+ [Using Passwords in Tests](#using-passwords-in-tests)
  + [User Data Setup](#user-data-setup)
  + [The Authentication-Triggering Fixture](#the-authentication-triggering-fixture)
  + [Create the AWS Client Instance](#create-the-aws-client-instance)
  + [Get the User Data](#get-the-user-data)

Welkin can be configured to integrate with AWS, but be warned that this is a finicky and fiddly process involving a lot of non-intuitable steps. Some of these steps will have to be taken for every different system or platform that these integrations will run on. 

Currently Welkin supports using AWS for storing secrets, using the AWS Parameter Store service.

## Setting Up the AWS Integration

### Create an AWS Account
In order to integrate with AWS, you will need an AWS account. This documentation assumes that you don't have an existing company or organization account that you can gain access to, so it describes creating and setting up a *new* account. 

You get a range of free services with an account: [https://aws.amazon.com/free/](https://aws.amazon.com/free/). But be very, very cautious about what you build, because you can quickly move beyond the boundaries of the free offerings.

Note that the **AWS Secrets Manager** is *not* included in the free offerings. While it might be the smartest and safest solution for managing passwords, **AWS Parameter Store** will be good enough and is in the free tier.  

#### Set a Budget! 
Even though you are working in the free tier, you can accidently fall out of that tier. Go to ```Dashboard --> Cost Management -->  Budgets``` and set a very low budget threshold and notification action.


### Add a Framework User
You actually need to add a **user**, a **user group**, and an inline **security policy**. This is kind of a circular process, where you have to update each of these until they are all complete.

#### Add a User Group and Inline Policy
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


#### Add a User
You need a user that represents the framework: this will provide credentials to the *framework as a user* to access the AWS parameters.

1. go to ```AWS --> Identity and Access Management (IAM) --> users```
2. create a user with a name like "framework_user"
3. add this user to the group "framework_users" (or whatever you called)

Note: You will come back to this user to generate and copy its access credentials. 
 

### Set Up The System AWS CLI Configuration
In order to interact with your framework's AWS account, you will need to set up the AWS Command Line Interface (CLI) for each system on which the framework will be run. So at the very least, you will set up your local development box. 


#### Installing AWS CLI Locally
1. Get the OSX package from [https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-mac.html]()  
2. Follow the instructions on this page.

Verifying installation:
``` bash
(v3) MacBook-Pro:welkin derek$ which aws
/usr/local/bin/aws
(v3) MacBook-Pro:welkin derek$ aws --version
aws-cli/2.2.40 Python/3.8.8 Darwin/18.7.0 exe/x86_64 prompt/off
```


#### Configure the Local AWS CLI
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


### Set your Passwords
The typical structure for application passwords looks like this:
```
tier
    |- application
        |- username
```

This yields a string path "tier/application/username". We will use this as the name for the *name* of the parameter that corresponds to the password *value*. However, we should prepend this with a node that identifies this as being a framework parameter distinct from what anybody else in our company might be doing. For example, we might prepend this with "welkin".

1. go to ```AWS --> Systems Manager --> Parameter Store```
2. create a parameter with a name that reflects the unique prepend + node path, for example "/welkin/prod/my_app/user01"; that leading slash is required.
3. specific an appropriate value type
4. assign a tag that references the framework, for example "ok_welkin"

You will have to repeat this for *every* password (parameter) you need to support.

Note: it may take a few minutes for the new parameters to get associated with the user. Until that happens, you may get a ```botocore.exceptions.ClientError```.


## Using Passwords in Tests
The most common use case for passwords is that applications require login credentials for authenticating a user; these credentials are usually in the form of emails and passwords. However you create these test accounts, you will have at least these email address and password couplets that you have to manage for your tests.

### User Data Setup
The file ```data/users.py``` is where you create the data model for user accounts across tiers, but note that **passwords do not get saved anywhere in the framework code**. This data model will look this:
```python
app_user_map = {
    'int': {
        'my_app': {
            'user01': {
                'app': 'my_app',
                'email': 'int_user@example.com',
                'fuid': 'user01'
            }
        }
    },
    'stage': {
        'my_app': {
            'user01': {
                'app': 'my_app',
                'email': 'test_user@example.com',
                'fuid': 'user01'
            }
        }
    },
    'prod': {
        'my_app': {
            'user01': {
                'app': 'my_app',
                'email': 'prod_user@example.com',
                'fuid': 'user01'
            },
        }
    }
}
```

For every tier in your system -- and you should edit this to reflect your system -- you include the information for the app test user accounts on that tier. The path of keys to the user is what you use to name the parameter in the AWS Parameter Store, prepended with a framework identifier string. So from this example, we have three parameter paths: 

1. ```/welkin/int/my_app/user01```
2. ```/welkin/stage/my_app/user01```
3. ```/welkin/prod/my_app/user01```

These are what you are using in the **Set your Passwords** section above.

### The Authentication-Triggering Fixture
In every test method that needs to use a user password, add the fixture **auth** as an argument. For example:
```python
class MyTests:

    def test_foo(self, auth):
        session = auth
```

That fixture triggers the creation of an AWS Session object. 


### Create the AWS Client Instance
In order to access a password, which is just a SecureString AWS Parameter Store parameter value, you need to create an AWS Client object. Then you directly request that parameter with the client:
```python
from welkin.integrations.aws.aws import AWSClient

class MyTests:

    def test_foo(self, auth):
        tier = 'prod'
        user_id = 'user01'
        app_id = 'my_app'
        param_key = f"/welkin/{tier}/{app_id}/{user_id}"
        
        # disambiguate the session for clarity
        session = auth

        # create a client tied to this session
        client = AWSClient(session, resource_name='ssm')

        # make the AWS get parameter call
        res = client.get_parameter_data(
            aws_key_name=param_key, decrypt=True)

        password = res['Parameter']['Value']
```

### Get the User Data 
Use the AWS Client object to get the password, and pull in the user data to get the email; now you have the credentials for further test case actions. 

```python
from welkin.data import users
from welkin.integrations.aws.aws import AWSClient

class MyTests:

    def test_foo(self, auth):
        tier = 'prod'
        user_id = 'user01'
        app_id = 'my_app'
        param_key = f"/welkin/{tier}/{app_id}/{user_id}"
        
        # get user data
        user = users.get_specific_user(tier, app_id, user_id)
        email = user.get('email')
        
        # disambiguate the session for clarity
        session = auth

        # create a client tied to this session
        client = AWSClient(session, resource_name='ssm')

        # make the AWS get parameter call
        res = client.get_parameter_data(
            aws_key_name=param_key, decrypt=True)

        password = res['Parameter']['Value']
        
        # do something with user email and password
```

If you use the user model, you can streamline this a little bit:
```python
from welkin.models.user import ApplicationUser
from welkin.integrations.aws.aws import AWSClient

class MyTests:

    def test_foo(self, auth):
        tier = 'prod'
        user_id = 'user01'
        app_id = 'my_app'
        
        # disambiguate the session for clarity
        session = auth

        # set up user object
        user = ApplicationUser(tier, app_id, user_id)
        email = user.properties.get('email')

        # get the password
        user.get_password_from_aws(session, verbose=True, decrypt=True)
        password = user.password
        
        # do something with user email and password
```


