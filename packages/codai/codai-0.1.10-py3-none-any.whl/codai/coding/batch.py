def batch_apply(change: str, files_glob: str, dry_run: bool = True):
    """In this function, we take the `changes` string and apply it (using an AI model) to all the files that match the `files_glob` pattern."""
    # imports
    import os
    import glob

    from codai.repl import print
    from codai.bots.code import bot as code_bot

    # get the list of files
    files = glob.glob(files_glob)

    # apply the change to each file
    for file in files:
        if not os.path.isfile(file):
            print(f"Skipping {file} as it is not a file.")
            continue
        print(f"file: {file}")
        with open(file, "r") as f:
            code = f.read()
        prompt = f"Apply the following change to the code in {file}:\n\n{change}\n\nCurrent code:\n\n```\n{code}\n```"
        print(f"current code:\n\n```\n{code}\n```")
        new_code = code_bot(prompt).data.code
        print(f"new code:\n\n```\n{new_code}\n```")
        if not dry_run:
            with open(file, "w") as f:
                f.write(new_code)
