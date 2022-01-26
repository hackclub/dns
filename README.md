# Hack Club's DNS

[![test](https://github.com/hackclub/dns/workflows/test/badge.svg)](https://github.com/hackclub/dns/actions?query=workflow%3Atest)
[![deploy](https://github.com/hackclub/dns/workflows/deploy/badge.svg)](https://github.com/hackclub/dns/actions?query=workflow%3Adeploy)

This repository is used for managing Hack Club's DNS configuration through [OctoDNS](https://github.com/github/octodns). Please see its documentation for more information.

Domains are available for all clubs and projects related to Hack Club.

Non-HQ sites using Vercel can not use Hack Club's DNS due to Vercel limitations. Please consider alternatives such as Netlify or GitHub Pages.

## Adding a subdomain

1. [Create a fork](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo) of this repository.
2. In your fork open the [hackclub.com.yaml](./hackclub.com.yaml) file and add the following alphabetically based off the subdomain name:

```yaml
SUBDOMAIN_NAME:
  - ttl: 1
    type: CNAME
    value: SOURCE_DOMAIN_OR_IP.
```

3. Replace `SUBDOMAIN_NAME` with the name of the sub-domain. So if the name was `hello` then the subdomain would be `hello.hackclub.com`.
4. Replace `SOURCE_DOMAIN_OR_IP` with the domain or IP address of the website you want the subdomain to go. If you are using an IP address change `type: CNAME` to `type: A`. Remember to leave that `.` at the end!
5. Commit your changes and [create the PR](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork)!

That's it! Someone with contributor access to the repo will then review your PR.
