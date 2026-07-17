# Hack Club's DNS

[![test](https://github.com/hackclub/dns/workflows/test/badge.svg)](https://github.com/hackclub/dns/actions?query=workflow%3Atest)
[![deploy](https://github.com/hackclub/dns/workflows/deploy/badge.svg)](https://github.com/hackclub/dns/actions?query=workflow%3Adeploy)

This repository is used to manage Hack Club's DNS configuration using [OctoDNS](https://github.com/github/octodns). Please see its documentation for more information.

## Adding a subdomain

## Using the website

We have a website that allows you to add a subdomain to Hack Club's DNS without needing to know how to use GitHub or OctoDNS. You can find it at [https://dns.hackclub.com](https://dns.hackclub.com). It can also be faster if you are just making a small change, like adding a subdomain or editing an existing one. If you are making a large change, like adding multiple subdomains or changing the DNS records for an existing subdomain, please use a pull request.

### Using a pull request

1. [Create a fork](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo) of this repository.
2. In your fork open the [hackclub.com.yaml](./hackclub.com.yaml) file and add the following alphabetically based off the subdomain name:

```yaml
SUBDOMAIN_NAME: # email@example.com U012AB345CD
  - type: CNAME
    value: SOURCE_DOMAIN_OR_IP.
```

3. Replace `SUBDOMAIN_NAME` with the name of the subdomain. So if the name was `hello` then the subdomain would be `hello.hackclub.com`.
4. Replace `SOURCE_DOMAIN_OR_IP` with the domain or IP address of the website you want the subdomain to go to. If you are using an IP address, change `type: CNAME` to `type: A`. Remember to leave that `.` at the end!
5. Add your contact information in a comment (see above). Include either an email address, Slack ID, or both.
6. Commit your changes and [create the PR](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork)!

That's it! Someone with contributor access to the repo will then review your PR.

If you're asked to make any changes to your pull request, please amend it by committing to your fork, instead of closing it and creating another.

### Replacing a `CNAME` record with another record type

The CNAME record cannot coexist with other record types, which may require you to change to an `ALIAS` or `A` record type if you need additional DNS records on your subdomain. Due to a bug in OctoDNS, removing a CNAME may cause your changes to break. You might encounter this when trying to use both Vercel and email/Google Workspace on the same subdomain.

To fix this, follow these steps, each in a separate PR:

1. Make a PR that deletes all records on your subdomain (ex: [#1642](https://github.com/hackclub/dns/pull/1642)).
2. Make another PR that adds the additional records needed, replacing the `CNAME` with the other record that you want (oftentimes `ALIAS`) (ex: [#1643](https://github.com/hackclub/dns/pull/1643)).
3. Make it clear to the person reviewing your PRs that the first PR must be merged before the second one.

## Limitations

Subdomains, under domains following the format `hackclub.xxx`(or other domains referring to hackclub), are only available for official Hack Club projects, not including HCB (fiscally sponsored) projects. Everyone is welcome to use `dino.icu`!

When adding a site hosted on ▲ Vercel, you will need to verify the domain by adding a TXT record.

<img width="1362" height="444" alt="image@2x" src="https://github.com/user-attachments/assets/095174f9-3f1b-4ad6-8130-aee78bd6794b" />

Add the value to the [hackclub.com.yaml](./hackclub.com.yaml) file as shown below:

```yaml
_vercel:
  type: TXT
  values:
    - vc-domain-verify=wackclub.hackclub.com,423c28e0fbdd51449cf1
 ```
