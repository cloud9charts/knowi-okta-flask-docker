### Knowi-Okta-Flask-Docker
A simple Flask app to access Knowi Single-Sign-On using Okta for user registration and login.

In this tutorial, you’ll use Okta to store the user accounts for your web app, and you’ll use 
OpenID Connect to talk to Okta to handle the authentication and authorization to 
[Knowi](https://www.knowi.com) as the Service Provider.

#### Requirements
* A Knowi [account](https://knowi.com/signup) with an SSO Customer Token
  * How to generate a [Knowi Customer Token](https://docs.knowi.com/hc/en-us/articles/360047948393-Embedding-with-Single-Sign-On)     
* An Okta [developer account](https://developer.okta.com/signup/)
  * How to create an [Okta app](https://developer.okta.com/docs/guides/sign-into-web-app/aspnet/create-okta-application/)


#### Running the App
This app requires Knowi and Okta to run. After creating a free account or using an existing account, next
will be a `client_secrets.json` file which holds our OpenID Connect information. Update the `clients_secrets.json.template`
file in the project folder root with the appropriate Okta variables. 

```
{
  "web": {
    "client_id": "{{ OKTA_CLIENT_ID }}",
    "client_secret": "{{ OKTA_CLIENT_SECRET }}",
    "auth_uri": "{{ OKTA_ORG_URL }}/oauth2/default/v1/authorize",
    "token_uri": "{{ OKTA_ORG_URL }}/oauth2/default/v1/token",
    "issuer": "{{ OKTA_ORG_URL }}/oauth2/default",
    "userinfo_uri": "{{ OKTA_ORG_URL }}/oauth2/default/userinfo",
    "redirect_uris": [
      "http://localhost:5000",
      "http://localhost:5000/oidc/callback"
    ]
  }
}
```

Next, define some necessary environment variables (or update [Dockerfile](Dockerfile) `ENV`)
```shell script
export KNOWI_CUSTOMER_TOKEN={{ KNOWI_CUSTOMER_TOKEN }}
export OKTA_AUTH_TOKEN={{ OKTA_AUTH_TOKEN }}
```

##### Build application
```
$ docker build -t knowi-okta .
```

##### Run application
```
$ docker run --name knowi-okta -d -p 5000:5000 knowi-okta
```

On a browser, visit [http://localhost:5000](http://localhost:5000) and explore the site!
