# Repository workflow

- After completing and validating any requested repository changes, create a focused branch and commit, push it to `origin`, open a pull request against the default branch, and merge the pull request without waiting for additional confirmation.
- After the pull request is merged, synchronize the local default branch and remove the merged local and remote feature branches when safe.
- Do not publish repository changes through this workflow when the user explicitly asks to keep the work local, leave it uncommitted, or leave the pull request open for review.
- If authentication, permissions, required checks, merge conflicts, or branch protection prevent completion, preserve the work and clearly report the blocker.
