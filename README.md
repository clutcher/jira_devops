# Jira DevOps
Django application designed to simplify day to day work of release management for Operations team. It is designed to be used in private network without public access.

Main futures:
+ Generate release note page from Jira tickets (could be injected via iframe in Confluence)

## Implementation notes
It is Django application with modules:
+ **jira** service layer module, which provides service to get information from Jira.
+ **repo** service layer module, which provides service to get information from Git.
+ **release_notes** service layer module, which provides services to generate release notes from Jira tickets
+ **xenon_theme** set of static files and templates used by other modules to generate HTML
+ **frontend** views module, which defines URL's and view/controllers for them

There is 2 Django settings module:

+ settings.development (default)
+ settings.production

Main difference - production settings enables compression for static file.

## Execution notes

Application requires 3 mandatory settings, which must be passed as environment variables:

+ JIRA_SERVER - URL to Jira server, usually looks like `https://company_name.atlassian.net`
+ JIRA_USERNAME - username used for login, usually looks like `automation.devops@companyname.com`
+ JIRA_PASSWORD - App password(API token) for login, usually looks like `qs1RWbyzramqqyNqqdnc3DC9`, could be generated
  following [instruction](https://support.atlassian.com/bitbucket-cloud/docs/app-passwords/)

Optional settings for Git integration:

+ GIT_REPO_URL - URL to Git, usually looks like `https://bitbucket.org/company/repo.git`
+ GIT_USERNAME - git username
+ GIT_PASSWORD - password for git user

After setting up environment variables application could be run as regular Django application(would be used default
development settings):

```shell
python manage.py runserver
```

Another option is build and run docker container(would be used production settings):

```shell
docker build -t jira_devops .
docker run -p 8000:8000 jira_devops
```

## Usage notes

+ URL to view generated release notes (could be injected as an iframe in Confluence)
  + /frames/releases/ - generate release notes for all unreleased releases
  + /frames/releases/?version=PRJ-V1.00.0 - generate release notes for specified release name

## Version history

### 0.1.1

+ **(Bug)** Allow injecting release notes via iframe on HTTPS page.

### 0.1

+ **(Feature)** Generate release note page from Jira tickets.
