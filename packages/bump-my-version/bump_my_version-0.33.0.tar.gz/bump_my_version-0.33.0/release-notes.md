[Compare the full difference.](https://github.com/callowayproject/bump-my-version/compare/0.32.2...0.33.0)

### Fixes

- Fixed warnings in documentation. [782077d](https://github.com/callowayproject/bump-my-version/commit/782077dc438007d4b585991788efe7c5a5c8c19f)
    
- Refactored PEP621 tests into a class. [2a4f12a](https://github.com/callowayproject/bump-my-version/commit/2a4f12a68067bacf81ec536b884e9ec3afb16751)
    
  The tests are pretty much the same but renamed for clarity.
- Fixed: allow omitting the current version in sample-config. [6b369fe](https://github.com/callowayproject/bump-my-version/commit/6b369fec76e9a45b919e32a85d0b894752f6374d)
    
  If the current version is explicitly left empty during the
  `sample-config` questionnaire, the resulting `tool.bumpversion` table
  now lacks a `current_version` key, and will fall back to PEP 621
  `project.version` (if not dynamic). The instruction text specifically
  hints at this new functionality.
### New

- Add test for moveable tags. [df787f1](https://github.com/callowayproject/bump-my-version/commit/df787f153f1dcde8268e83ef3f035d018735e7bb)
    
- New feature: retrieve and update the PEP 621 project version, if possible. [3032450](https://github.com/callowayproject/bump-my-version/commit/3032450098f14abeb0661c62442d1ca03b222e09)
    
  When determining the current version, and if
  `tool.bumpversion.current_version` is not set, attempt to retrieve the
  version from `project.version` à la PEP 621. If that setting is not
  set, or if the version is explicitly marked as dynamically set, then
  continue with querying SCM tags.

  When updating the configuration during bumping, if we previously
  successfully retrieved a PEP 621 version, then update the
  `project.version` field in `pyproject.toml` as well. We always update,
  even if the true current version was read from
  `tool.bumpversion.current_version` instead of `project.version`.

  The docs have been updated; specifically, the "multiple replacements in
  one file" howto and the reference for `current_version`.

  The tests have been adapted: the new `pep621_info` property would
  otherwise trip up the old test output, and the `None` default would trip
  up the TOML serializer. Additionally, new tests assert that
  `project.version` (and correspondingly, the `pep621_info` property) is
  correctly honored or ignored, depending on the other circumstances.
### Other

- [pre-commit.ci] pre-commit autoupdate. [59e8634](https://github.com/callowayproject/bump-my-version/commit/59e863415d9a9f7ef082978ccee7b27c36112ea1)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.9.6 → v0.9.7](https://github.com/astral-sh/ruff-pre-commit/compare/v0.9.6...v0.9.7)

### Updates

- Updated documentation. [8162dd8](https://github.com/callowayproject/bump-my-version/commit/8162dd852b874e36626ad01ad72ea892499a9817)
    
