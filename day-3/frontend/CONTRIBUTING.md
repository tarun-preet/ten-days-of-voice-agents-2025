# Contributing

Thanks for contributing! A few guidelines to help keep things consistent and to avoid dependency issues:

- Package manager: pnpm is used for this repository and ensures consistent node_modules linking. Please use pnpm for installing dependencies and running scripts:

```bash
pnpm install
pnpm dev
```

- Formatting: This repo uses Prettier and a formatting pre-commit hook. Run the formatter locally before committing:

```bash
pnpm format
```

- Linting: We rely on ESLint and TypeScript for code quality. Run the linter and fix issues before creating a PR:

```bash
pnpm lint
```

- Branching: Use feature branches and submit PRs against `main`. Include a descriptive PR title and reference any related issues.

If you have questions or need help setting up your environment, open an issue and we’ll help you get started.
