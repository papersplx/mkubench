# Git History Rewrite Documentation

## Summary

On 2026-09-07, the git history was rewritten to standardize all commit authors to `papersplx`. The remote was force-pushed to complete this change.

## Why This Was Necessary

Commit authors across the history were inconsistent and used a pseudonym that needed to be replaced with the actual identity `papersplx` for proper attribution and transparency.

## What Changed

- All commit authors standardized to `papersplx`
- All committer names standardized to `papersplx`
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

- Original history: commits by the previous author name
- Rewritten history: all commits by `papersplx`
- Remote updated: 2026-09-07