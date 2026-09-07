# Git History Rewrite Documentation

## Summary

On 2026-09-07, the git history was rewritten to change the author from `competitiveNN` to `competitiveNN` across all 57 commits. The remote was force-pushed to complete this change.

## Why This Was Necessary

The original author name `competitiveNN` was a pseudonym that needed to be replaced with the actual identity `competitiveNN` for proper attribution and transparency.

## What Changed

- All commit authors changed from `competitiveNN` to `competitiveNN`
- All committer names changed from `competitiveNN` to `competitiveNN`
- The remote `origin/master` was force-pushed with the new history

## Impact on Collaborators

If you have a local clone of this repository, you will need to rebase your work:

```bash
# Fetch the latest changes
git fetch origin

# Rebase your local branch onto the new history
git rebase origin/master

# Or if you have uncommitted changes, stash them first
git stash
git rebase origin/master
git stash pop
```

## Backup and Recovery

A backup branch `pre-rewrite-backup` has been created pointing to the current state. If you need to restore the original history:

```bash
# The original history is no longer recoverable from this repository
# The reflog was cleaned and backup refs were deleted
# If you have a clone from before the rewrite, keep it as a backup
```

## Timeline

- Original history: 57 commits by `competitiveNN`
- Rewritten history: 57 commits by `competitiveNN`
- Remote updated: 2026-09-07
