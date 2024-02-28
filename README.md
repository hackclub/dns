# Hack Club's DNS

[![test](https://github.com/hackclub/dns/workflows/test/badge.svg)](https://github.com/hackclub/dns/actions?query=workflow%3Atest)
[![deploy](https://github.com/hackclub/dns/workflows/deploy/badge.svg)](https://github.com/hackclub/dns/actions?query=workflow%3Adeploy)

This repository is used for managing Hack Club's DNS configuration through [OctoDNS](https://github.com/github/octodns). Please see its documentation for more information.

## Adding a subdomain

1. [Create a fork](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo) of this repository.
2. In your fork open the [hackclub.com.yaml](./hackclub.com.yaml) file and add the following alphabetically based off the subdomain name:

```yaml
SUBDOMAIN_NAME:
  - ttl: 600
    type: CNAME
    value: SOURCE_DOMAIN_OR_IP.
```

3. Replace `SUBDOMAIN_NAME` with the name of the sub-domain. So if the name was `hello` then the subdomain would be `hello.hackclub.com`.
4. Replace `SOURCE_DOMAIN_OR_IP` with the domain or IP address of the website you want the subdomain to go. If you are using an IP address change `type: CNAME` to `type: A`. Remember to leave that `.` at the end!
5. Commit your changes and [create the PR](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork)!

That's it! Someone with contributor access to the repo will then review your PR.

### Google Workspace / Vercel Combination

If you're looking to use both Google Workspace and Vercel, deploying your changes may break. To fix this, follow these steps (each in a seperate step, `irvine.hackclub.com` is an example of this process):

1. Delete all records associated to your subdomain.
2. Add the records needed for Google Workspace to your subdomain.
3. Add the remaining records you'd like for your subdomain. Instead of a `CNAME`, use `ALIAS`.

## Limitations

Subdomains, under domains following the format `hackclub.xxx`(or other domains reffering to hackclub), are only available for clubs and projects related to Hack Club, this does not include HCB projects. Everyone is welcome to use `dino.icu`!

When adding a site hosted on ▲ Vercel, you will need to verifiy the domain by adding a TXT record.

<img width="787" alt="image" src="https://user-images.githubusercontent.com/63619830/171483050-68d3123b-3b16-4293-b7f1-f5259f6d039b.png">

Add the value to the [hackclub.com.yaml](./hackclub.com.yaml) file as shown below:

```yaml
_vercel:
  ttl: 600
  type: TXT
  values:
    - vc-domain-verify=wackclub.hackclub.com,423c28e0fbdd51449cf1
 ```
