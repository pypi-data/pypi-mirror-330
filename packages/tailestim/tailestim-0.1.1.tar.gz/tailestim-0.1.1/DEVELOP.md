# Development notes

## Building package
```sh
hatch run test:all
hatch build
```

## GitHub Actions
- `test.yml`: Test functions
- `release.yml`: Automatically publish to PyPI when a release is made

## Release Process
To release a new version:

1. Set up PyPI trusted publisher (one-time setup):
   - Go to PyPI -> Account settings -> Add publisher
   - Set publisher to your GitHub repository (e.g., `mu373/tailestim`)
   - Set workflow name to `release`
   - Set environment to `None`

2. Create a new release on GitHub:
   - Go to GitHub -> Releases -> Draft a new release
   - Create a new tag with `v` prefix (e.g., `v0.1.0`)
   - Write release notes
   - Publish release

The GitHub Actions workflow will automatically:
1. Update version in `__about__.py`
2. Run tests
3. Build and publish to PyPI
4. Commit the version bump back to the repository
