# Repository workflow

- After completing and validating any requested repository changes, create a focused branch and commit, push it to `origin`, open a pull request against the default branch, and merge the pull request without waiting for additional confirmation.
- After the pull request is merged, synchronize the local default branch and remove the merged local and remote feature branches when safe.
- Do not publish repository changes through this workflow when the user explicitly asks to keep the work local, leave it uncommitted, or leave the pull request open for review.
- If authentication, permissions, required checks, merge conflicts, or branch protection prevent completion, preserve the work and clearly report the blocker.

## Responsive design

- Apply stylistic changes to both desktop and mobile by default so the experiences mirror each other wherever practical.
- If a requested change would create conflicting requirements, behavior, or styling between desktop and mobile, stop and ask the user for direction before implementing it.

## Essay publishing

- Use the repository-local `$publish-essay` skill for essay drafting, publishing, updates, Writing archive changes, and post-specific artifacts.
- Treat `writing-inbox/essay.md` as the single Markdown input and `writing-inbox/assets/` as that draft's artifact directory.
