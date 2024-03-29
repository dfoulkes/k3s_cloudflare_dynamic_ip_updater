# Overview

Although my home IP is relatively static with my current ISP it is still consumer grade internet and
thus subject to change. I have a few services that I would like to access from outside my home network, the main one 
being the link between Cloudflare and my home network for my blog.

So to avoid possible outages on my blog I have created a script that will update the Cloudflare DNS record with my current
home IP address.

This works as follows:
1. Get the current public IP address of the home network
2. Get the current IP address of the DNS record in Cloudflare
3. If the IP addresses are different, update the DNS record with the new IP address

# Requirements

- Python 3.11+
- Cloudflare API Token
- Cloudflare Zone ID

# Installation

This intended for use with self hosted kubernetes clusters. The following steps will guide you through the installation.

Create Two Secrets in the namespace where you want to deploy the script. The secrets should be named 
`website-domain-secret` and `cf-secret` respectively.

```shell
# creates the secret for the Cloudflare hosted domain.
create secret generic website-domain-secret --from-literal=website-domain="MY_DOMAIN_NAME"

# creates the secret for the Cloudflare API Token
kubectl create secret generic cf-secret --from-literal=cf-token="MY_TOKEN"
```
> [!TIP]
> Apply namespace as required. 

Apply the `schedule.yaml` file to the cluster. This will create a cronjob that will run the script every 5 minutes.

```shell
kubectl apply schedule.yaml
```

