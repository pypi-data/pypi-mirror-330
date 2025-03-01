# Prospector profile utils

It contains some utility Prospector profiles.

## Usage

```bash
pip install prospector-profile-utils
```

Then, in your `.prospector.yaml` file, you can use the profiles like this:

```yaml
inherits:
  - utils:base
  - utils:c2cwsgiutils
  - utils:no-design-checks
```

It provide also an alternate base witch activate less strict checks:

```yaml
inherits:
  - utils:base-less-strict
```

Additional available profiles:

- `utils:fix`: Disables specific rules that are known to have reliability issues.
- `utils:autofix`: Enables automatic fixing capabilities for supported rules.
- `utils:tests`: Specifically designed for test files validation, recommended to use in combination with the `utils:fix` profile.

## Contributing

Install the pre-commit hooks:

```bash
pip install pre-commit
pre-commit install --allow-missing-config
```
