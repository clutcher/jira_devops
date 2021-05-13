from multiprocessing import Pool

from jira_devops.repo.RepoService import RepoService

shared_update_repo_pool = Pool(processes=1)


def async_fetch_repo():
    if len(shared_update_repo_pool._cache) == 0:
        shared_update_repo_pool.apply_async(RepoService.fetch_latest_data_from_remote_repository, ())
