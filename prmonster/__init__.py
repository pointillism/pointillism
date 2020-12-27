import logging
from subprocess import CalledProcessError

from .models import Repo
from .pr.github import *
from .readme import update_readmes


def repos_reader(filename):
    """
    Iterates through lines of a .repos file.
    Expects git project format:

    `{owner}/{project}\n`
    """
    with open(filename, "r") as repos:
        for line in repos:
            yield Repo.parse(line)


def devour_repos(*repos, dry_run=False):
    """Run PRMonster on `repos` params.
    """
    for filename in repos:
        logging.info(filename)
        for repo in repos_reader(filename):
            repo = checkout(repo)  # adding checkout path
            if 'pointillism.io' in contents(repo, 'README.md'):
                logging.info(f"SKIPPING: {str(repo)}. found 'pointillism.io'")
                continue

            update_readmes(repo)
            try:
                commit(repo, '"Adding pointillism.io"')
            except CalledProcessError:
                logging.error(
                    f"Commit failure. Does {str(repo)} have DOT files?")
                continue
            try:
                if not dry_run:
                    pr(repo)
            except CalledProcessError:
                logging.error(
                    f"PR failure for: {str(repo)}")
