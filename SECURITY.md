# Security

## Reporting

Do not post credentials, personal information, or exploit details in public issues.
Report vulnerabilities privately to the maintainer at **manyalp12345@gmail.com**.
Include the affected commit, reproduction steps, expected impact, and a minimal
example with synthetic data. Do not test against deployments you do not own.
There is no guaranteed response time or paid support SLA.

## Maintenance scope

Security fixes target the current default branch. Older commits and container
images are not promised ongoing fixes. This project has not undergone a complete
independent security audit.

## Deployment responsibilities

- Create a unique administrator password. Container startup no longer creates
  or resets an `admin/admin` account. Existing installations must rotate that
  password explicitly with `python manage.py changepassword admin`.
- Set a private SECRET_KEY, DEBUG=False, explicit ALLOWED_HOSTS, HTTPS, secure
  cookies, and appropriate proxy settings. Address `check --deploy` warnings.
- Public display APIs are intended for public information. Authenticated API
  writes are not a complete role-based authorization policy. Review access
  requirements before giving accounts to untrusted users.
- Persist and back up data; protect uploads and never commit production databases.
- Review dependency advisories and validate upgrades before deployment.
