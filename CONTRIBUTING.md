# Contributing

Contributions to DigitalSignage are welcome: reproducible bug reports, Nepali
language improvements, documentation, accessibility fixes, and tests.

## First contribution

Follow the README's local setup. Use synthetic notices and contacts when testing;
do not commit passwords, database files, real citizen data, or uploaded media.
Open an issue before substantial feature or architecture changes so scope can be
agreed with the maintainer. Small fixes can go directly to a pull request.

1. Fork the repository and create a focused branch.
2. Describe the problem and the expected behavior.
3. Add regression tests for behavioral fixes and update relevant documentation.
4. Run `python manage.py check`, `python manage.py makemigrations --check --dry-run`,
   and `python manage.py test`. For CSS changes run `npm ci && npm run build:css`.
5. Open a pull request describing the change and actual validation results.
   Include screenshots for visible changes, using synthetic content.

The maintainer reviews scope, compatibility, data migrations, and test results
before merging. No response-time guarantee is offered. Contributions are provided
under the repository's MIT license; retain attribution for third-party work.

Report vulnerabilities privately as described in SECURITY.md, not in public issues.
Follow CODE_OF_CONDUCT.md in all project spaces.
