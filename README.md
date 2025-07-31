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

If you're asked to make any changes to your pull request, please amend it by commiting to your fork, instead of closing it and creating another.

### Replacing a `CNAME` record with another record type

The CNAME record cannot coexist with other record types, which may require you to change to an `ALIAS` or `A` record type if you need additional DNS records on your subdomain. Due to a bug in OctoDNS, removing a CNAME may result in deploying your changes breaking. You might encounter this when trying to use both Vercel and email/Google Workspace on the same subdomain. 

To fix this, follow these steps, each in a seperate PR:

1. Make a PR that deletes all records on your subdomain (ex: [#1642](https://github.com/hackclub/dns/pull/1642)).
2. Make another PR that adds the additional records needed, replacing the `CNAME` with the other record that you want (oftentimes `ALIAS`) (ex: [#1643](https://github.com/hackclub/dns/pull/1643)).
3. Make it clear to the person reviewing your PRs that the first PR must be merged before the second one. 

## Limitations

Subdomains, under domains following the format `hackclub.xxx`(or other domains reffering to hackclub), are only available for official Hack Club projects, not including HCB (fiscally sponsored) projects. Everyone is welcome to use `dino.icu`!

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
