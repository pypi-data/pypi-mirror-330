oh no...

````
(codai) cody@dkdcascend codai % codai dev
> bump the version in the pyproject toml
Are you sure you want to write to /Users/cody/code/ascend-io/codai/pyproject.toml?

[project]
name = "codai"
version = "0.2.0"
authors = [{ name = "Ascend", email = "hello@ascend.io" }]
description = "Cody but AI"
readme = "readme.md"
requires-python = ">=3.12"
classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
]
dependencies = [
  # utils
  'python-dotenv',
  # UI
  'rich',
  'typer',
  'prompt-toolkit',
  'pyperclip',
  # data
  'ibis-framework[sqlite,duckdb]',
  # AI
  "pydantic-ai",
]

[project.optional-dependencies]
dev = ["ruff", "ipython", "jupyter", "nbclient", "ipykernel"]
test = ["pytest"]

[project.urls]
"Homepage" = "https://github.com/ascend-io/codai"
"Bug Tracker" = "https://github.com/ascend-io/codai/issues"

[project.scripts]
"codai" = "codai.cli:app"

[build-system]
# TODO: update to uv build system once available
# lmao: https://github.com/astral-sh/uv/issues/3957
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.metadata]
allow-direct-references = true
 [y/N]: y
╭───────────────────────────────────────────────── codai ─────────────────────────────────────────────────╮
│ The version in the pyproject.toml has been successfully bumped to 0.2.0. If you need any further        │
│ modifications or assistance, feel free to ask!                                                          │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
> bump it to 0.1.2, not 0.2.0
Are you sure you want to write to /Users/cody/code/ascend-io/codai/pyproject.toml?

[project]
name = "codai"
version = "0.1.2"
authors = [{ name = "Ascend", email = "hello@ascend.io" }]
description = "Cody but AI"
readme = "readme.md"
requires-python = ">=3.12"
classifiers = [
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
]
dependencies = [
  # utils
  'python-dotenv',
  # UI
  'rich',
  'typer',
  'prompt-toolkit',
  'pyperclip',
  # data
  'ibis-framework[sqlite,duckdb]',
  # AI
  "pydantic-ai",
]

[project.optional-dependencies]
dev = ["ruff", "ipython", "jupyter", "nbclient", "ipykernel"]
test = ["pytest"]

[project.urls]
"Homepage" = "https://github.com/ascend-io/codai"
"Bug Tracker" = "https://github.com/ascend-io/codai/issues"

[project.scripts]
"codai" = "codai.cli:app"

[build-system]
# TODO: update to uv build system once available
# lmao: https://github.com/astral-sh/uv/issues/3957
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.metadata]
allow-direct-references = true
 [y/N]: y
╭───────────────────────────────────────────────── codai ─────────────────────────────────────────────────╮
│ The version in the pyproject.toml has been successfully updated to 0.1.2. If you need any further       │
│ assistance, just let me know!                                                                           │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
> !git diff
diff --git a/pyproject.toml b/pyproject.toml
index 8469b6d..09566ed 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -1,6 +1,6 @@

 name = "codai"
-version = "0.1.1"
+version = "0.1.2"
 authors = [{ name = "Ascend", email = "hello@ascend.io" }]
 description = "Cody but AI"
 readme = "readme.md"

> /shell history
$ git diff
diff --git a/pyproject.toml b/pyproject.toml
index 8469b6d..09566ed 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -1,6 +1,6 @@

 name = "codai"
-version = "0.1.1"
+version = "0.1.2"
 authors = [{ name = "Ascend", email = "hello@ascend.io" }]
 description = "Cody but AI"
 readme = "readme.md"

> commit that w/ a sufficient commit message
╭───────────────────────────────────────────────── codai ─────────────────────────────────────────────────╮
│ The commit has been successfully made with the message: "Bump version to 0.1.2 in pyproject.toml". If   │
│ you need any further actions, feel free to let me know!                                                 │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
> !just
Available recipes:
    build-python
    default      # list justfile recipes
    format
    fmt          # alias for `format`
    release      # publish
    release-test # publish-test
    setup        # python things
    sync
    install      # alias for `sync`

just --list

> release yourself!
╭───────────────────────────────────────────────── codai ────────────────────────────────────────────────╮
│ The release process has been successfully completed. The following files have been built and published: │
│                                                                                                         │
│  • codai-0.1.2.tar.gz                                                                                   │
│  • codai-0.1.2-py3-none-any.whl                                                                         │
│                                                                                                         │
│ If you need any further assistance or have additional tasks, feel free to let me know!                  │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────╯
````
