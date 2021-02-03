#
# GH file search client
# https://docs.github.com/en/free-pro-team@latest/rest/reference/search
#
import logging
from config import PROJECT_ROOT
from datetime import datetime
from time import sleep
from .search import *

REPO_DOC_PATH = PROJECT_ROOT + '/logs/repos'
log = logging.getLogger().info

CLIENT = GitHubFileSearchClient()
CONTENT = GitHubContent()
PAGE_MAX = 100
SUPPORTED_DOCS = ('md',) # , 'rst')
TAB = "\t"


def find_dot_repos(user=None):
    repo_count = 0
    target_repos = []
    page = 0
    while page < PAGE_MAX:
        args = {}
        if user is not None:
            args['user'] = user
        resp = CLIENT.search(DOT_FILE_SEARCH, page, **args)
        logging.info(resp)
        if not resp.repos():
            break

        dot_names = [item.filename() for item in resp.items]

        for repo in resp.repos():
            repo_count += 1
            owner, project = repo.split('/')
            fp = open(f'{REPO_DOC_PATH}/{owner}-{project}', 'w')
            record = lambda msg: fp.write(f"{msg}\n")

            record("=========================")
            dots = list(filter(lambda i: repo == i.repo, resp.items))
            target_docs = []
            unsupported = []
            dot_refs = CLIENT.search("*.png", repo=repo)
            author = ":".join(list(CONTENT.last_author(repo).values()))
            # + CLIENT.search("*.svg", repo=repo)

            log(f"PROCESSING REPO: {repo} dots: {len(dots)} refs: {len(dot_refs.items)} {author}")
            record(f"PROCESSING REPO: {repo} dots: {len(dots)} refs: {len(dot_refs.items)} {author}")
            record("========= dots ==========")
            for dot in dots:
                record(str(dot))
            record("== dot file references ==")

            if not dot_refs:
                target_repos.append([repo, None
                                     ] + dots)
            for ref in dot_refs.items:
                if ref.filetype() in SUPPORTED_DOCS:
                    target_docs.append(ref)
                    target_repos.append([repo,
                                         ref
                                         ] + dots)
                else:
                    unsupported.append(ref)
            for ref in target_docs + unsupported:
                record(str(ref))
            fp.close()

        log("======= discovered ======")
        for target in target_repos:
            if target[1] is None:
                log(TAB.join(map(str, ["DISCOVERED",
                                       target[0],
                                       "",
                                       "",
                                       *map(lambda i: i.content_url(), target[2:])
                                       ]
                                 )))
            else:
                log(TAB.join(map(str, ["DISCOVERED",
                                       target[0],
                                       target[1].content_url(),
                                       target[1].url,
                                       *map(lambda i: i.content_url(), target[2:])
                                       ]
                )))

        page += 1
        sleep(1)

    with open('{REPO_DOC_PATH}/repo.counts', 'a+') as fp:
        fp.write(datetime.strftime(datetime.now(), "%Y-%m-%d"))
        fp.write("\t")
        fp.write(str(repo_count))
        fp.write("\n")
