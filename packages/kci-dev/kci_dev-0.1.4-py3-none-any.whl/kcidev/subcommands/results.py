#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import gzip
import json
import os
import re
import subprocess
import urllib
from functools import wraps

import click
import requests
import yaml

from kcidev.libs.common import *

DASHBOARD_API = "https://dashboard.kernelci.org/api/"


def dashboard_api_fetch(endpoint, params):
    base_url = urllib.parse.urljoin(DASHBOARD_API, endpoint)
    try:
        url = "{}?{}".format(base_url, urllib.parse.urlencode(params))
        r = requests.get(url)
    except:
        click.secho(f"Failed to fetch from {DASHBOARD_API}.")
        raise click.Abort()
    data = r.json()

    # check for errors in json data
    if "error" in data:
        kci_msg("json error: " + str(data["error"]))
        raise click.Abort()

    return data


def dashboard_fetch_summary(origin, giturl, branch, commit):
    endpoint = f"tree/{commit}/summary"
    params = {
        "origin": origin,
        "git_url": giturl,
        "git_branch": branch,
    }

    return dashboard_api_fetch(endpoint, params)


def dashboard_fetch_builds(origin, giturl, branch, commit):
    endpoint = f"tree/{commit}/builds"
    params = {
        "origin": origin,
        "git_url": giturl,
        "git_branch": branch,
    }

    return dashboard_api_fetch(endpoint, params)


def dashboard_fetch_boots(origin, giturl, branch, commit):
    endpoint = f"tree/{commit}/boots"
    params = {
        "origin": origin,
        "git_url": giturl,
        "git_branch": branch,
    }

    return dashboard_api_fetch(endpoint, params)


def dashboard_fetch_tests(origin, giturl, branch, commit):
    endpoint = f"tree/{commit}/tests"
    params = {
        "origin": origin,
        "git_url": giturl,
        "git_branch": branch,
    }

    return dashboard_api_fetch(endpoint, params)


def repository_url_cleaner(url):
    # standardize protocol to https
    parsed = urllib.parse.urlsplit(url)
    scheme = "https"

    # remove auth from url
    authority = parsed.hostname
    if parsed.port:
        authority += f":{parsed.port}"

    url_cleaned = urllib.parse.urlunsplit((scheme, authority, *parsed[2:]))
    return url_cleaned


def dashboard_fetch_tree_list(origin):
    params = {
        "origin": origin,
    }
    return dashboard_api_fetch("tree-fast", params)


def is_inside_work_tree(git_folder):
    process = subprocess.Popen(
        ["git", "rev-parse", "--is-inside-work-tree"], stdout=subprocess.PIPE, text=True
    )
    std_out, std_error = process.communicate()
    is_inside_work_tree = std_out.strip()
    if is_inside_work_tree:
        return True
    return False


def get_folder_repository(git_folder, branch):
    kci_msg("git folder: " + str(git_folder))
    if git_folder:
        current_folder = git_folder
    else:
        current_folder = os.getcwd()

    previous_folder = os.getcwd()
    if os.path.isdir(current_folder):
        os.chdir(current_folder)
    else:
        os.chdir(previous_folder)
        kci_err("Not a folder")
        raise click.Abort()
    dot_git_folder = os.path.join(current_folder, ".git")
    if is_inside_work_tree(current_folder):
        while not os.path.exists(dot_git_folder):
            current_folder = os.path.join(current_folder, "..")
            dot_git_folder = os.path.join(current_folder, ".git")

    # Check if we are in a git repository
    if os.path.exists(dot_git_folder):
        # Get remote origin url
        git_config_path = os.path.join(dot_git_folder, "config")
        git_config = configparser.ConfigParser(strict=False)
        git_config.read(git_config_path)
        git_url = git_config.get('remote "origin"', "url")
        # A way of standardize git url for API call
        git_url = repository_url_cleaner(git_url)
        # Get current branch name
        process = subprocess.Popen(
            ["git", "branch", "--show-current"], stdout=subprocess.PIPE, text=True
        )
        branch_name, branch_error = process.communicate()
        branch_name = branch_name.strip()
        if branch:
            branch_name = branch

        # Get last commit hash
        process = subprocess.Popen(
            ["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, text=True
        )
        last_commit_hash, last_commit_hash_error = process.communicate()
        last_commit_hash = last_commit_hash.strip()

        os.chdir(previous_folder)
        kci_msg("tree: " + git_url)
        kci_msg("branch: " + branch_name)
        kci_msg("commit: " + last_commit_hash)
        return git_url, branch_name, last_commit_hash
    else:
        os.chdir(previous_folder)
        kci_err("Not a GIT folder")
        raise click.Abort()


def get_latest_commit(origin, giturl, branch):
    trees = dashboard_fetch_tree_list(origin)
    for t in trees:
        if t["git_repository_url"] == giturl and t["git_repository_branch"] == branch:
            return t["git_commit_hash"]

    kci_err("Tree and branch not found.")
    raise click.Abort()


def print_summary(type, n_pass, n_fail, n_inconclusive):
    kci_msg_nonl(f"{type}:\t")
    kci_msg_green_nonl(f"{n_pass}") if n_pass else kci_msg_nonl(f"{n_pass}")
    kci_msg_nonl("/")
    kci_msg_red_nonl(f"{n_fail}") if n_fail else kci_msg_nonl(f"{n_fail}")
    kci_msg_nonl("/")
    (
        kci_msg_yellow_nonl(f"{n_inconclusive}")
        if n_inconclusive
        else kci_msg_nonl(f"{n_inconclusive}")
    )
    kci_msg_nonl(f"\n")


def sum_inconclusive_results(results):
    count = 0
    for status in ["ERROR", "SKIP", "MISS", "DONE", "NULL"]:
        if status in results.keys():
            count += results[status]

    return count


def cmd_summary(data):
    kci_msg("pass/fail/inconclusive")
    summary = data["summary"]
    builds = summary["builds"]["status"]
    print_summary("builds", builds["valid"], builds["invalid"], builds["null"])

    boots = summary["boots"]["status"]
    inconclusive_boots = sum_inconclusive_results(boots)
    pass_boots = boots["PASS"] if "PASS" in boots.keys() else 0
    fail_boots = boots["FAIL"] if "FAIL" in boots.keys() else 0
    print_summary("boots", pass_boots, fail_boots, inconclusive_boots)

    tests = summary["tests"]["status"]
    pass_tests = tests["PASS"] if "PASS" in tests.keys() else 0
    fail_tests = tests["FAIL"] if "FAIL" in tests.keys() else 0
    inconclusive_tests = sum_inconclusive_results(tests)
    print_summary("tests", pass_tests, fail_tests, inconclusive_tests)


def cmd_list_trees(origin):
    trees = dashboard_fetch_tree_list(origin)
    for t in trees:
        kci_msg_green_nonl(f"- {t['tree_name']}/{t['git_repository_branch']}:\n")
        kci_msg(f"  giturl: {t['git_repository_url']}")
        kci_msg(f"  latest: {t['git_commit_hash']} ({t['git_commit_name']})")
        kci_msg(f"  latest: {t['start_time']}")


def cmd_builds(data, commit, download_logs, status):
    if status == "inconclusive":
        kci_msg("No information about inconclusive builds.")
        return

    for build in data["builds"]:
        if build["valid"] == None:
            continue

        if not status == "all":
            if build["valid"] == (status == "fail"):
                continue

            if not build["valid"] == (status == "pass"):
                continue

        log_path = build["log_url"]
        if download_logs:
            try:
                log_gz = requests.get(build["log_url"])
                log = gzip.decompress(log_gz.content)
                log_file = f"{build['config_name']}-{build['architecture']}-{build['compiler']}-{commit}.log"
                with open(log_file, mode="wb") as file:
                    file.write(log)
                log_path = "file://" + os.path.join(os.getcwd(), log_file)
            except:
                kci_err(f"Failed to fetch log {build['log_url']}.")
                pass

        kci_msg_nonl("- config:")
        kci_msg_cyan_nonl(build["config_name"])
        kci_msg_nonl(" arch: ")
        kci_msg_cyan_nonl(build["architecture"])
        kci_msg_nonl(" compiler: ")
        kci_msg_cyan_nonl(build["compiler"])
        kci_msg("")

        kci_msg_nonl("  status:")
        if build["valid"]:
            kci_msg_green_nonl("PASS")
        else:
            kci_msg_red_nonl("FAIL")
        kci_msg("")

        kci_msg(f"  config_url: {build['config_url']}")
        kci_msg(f"  log: {log_path}")
        kci_msg(f"  id: {build['id']}")
        kci_msg(f"  dashboard: https://dashboard.kernelci.org/build/{build['id']}")
        kci_msg("")


def filter_out_by_status(status, filter):
    if filter == "all":
        return False

    if filter == status.lower():
        return False

    elif filter == "inconclusive" and status in [
        "ERROR",
        "SKIP",
        "MISS",
        "DONE",
        "NULL",
    ]:
        return False

    return True


def filter_out_by_hardware(test, filter_data):
    # Check if the hardware name is in the list
    hardware_list = filter_data["hardware"]
    if test["misc"]["platform"] in hardware_list:
        return False

    if test["environment_compatible"]:
        for compatible in test["environment_compatible"]:
            if compatible in hardware_list:
                return False

    return True


def filter_out_by_test(test, filter_data):
    # Check if the test name is in the list
    test_list = filter_data["test"]
    if test["path"] in test_list:
        return False

    return True


def cmd_tests(data, commit, download_logs, status_filter, filter):
    filter_data = yaml.safe_load(filter) if filter else None

    for test in data:
        if filter_out_by_status(test["status"], status_filter):
            continue

        if filter_data and filter_out_by_hardware(test, filter_data):
            continue

        if filter_data and filter_out_by_test(test, filter_data):
            continue

        log_path = test["log_url"]
        if download_logs:
            try:
                log_gz = requests.get(test["log_url"])
                log = gzip.decompress(log_gz.content)
                log_file = f"{test['misc']['platform']}__{test['path']}__{test['config']}-{test['architecture']}-{test['compiler']}-{commit}.log"
                with open(log_file, mode="wb") as file:
                    file.write(log)
                log_path = "file://" + os.path.join(os.getcwd(), log_file)
            except:
                kci_err(f"Failed to fetch log {test['log_url']}.")
                pass

        kci_msg_nonl("- test path: ")
        kci_msg_cyan_nonl(test["path"])
        kci_msg("")

        kci_msg_nonl("  hardware: ")
        kci_msg_cyan_nonl(test["misc"]["platform"])
        kci_msg("")

        if test["environment_compatible"]:
            kci_msg_nonl("  compatibles: ")
            kci_msg_cyan_nonl(" | ".join(test["environment_compatible"]))
            kci_msg("")

        kci_msg_nonl("  config: ")
        kci_msg_cyan_nonl(test["config"])
        kci_msg_nonl(" arch: ")
        kci_msg_cyan_nonl(test["architecture"])
        kci_msg_nonl(" compiler: ")
        kci_msg_cyan_nonl(test["compiler"])
        kci_msg("")

        kci_msg_nonl("  status:")
        if test["status"] == "PASS":
            kci_msg_green_nonl("PASS")
        elif test["status"] == "FAIL":
            kci_msg_red_nonl("FAIL")
        else:
            kci_msg_yellow_nonl(f"INCONCLUSIVE (status: {test['status']})")
        kci_msg("")

        kci_msg(f"  log: {log_path}")
        kci_msg(f"  start time: {test['start_time']}")
        kci_msg(f"  id: {test['id']}")
        kci_msg(f"  dashboard: https://dashboard.kernelci.org/test/{test['id']}")
        kci_msg("")


def set_giturl_branch_commit(origin, giturl, branch, commit, latest, git_folder):
    if not giturl or not branch or not ((commit != None) ^ latest):
        giturl, branch, commit = get_folder_repository(git_folder, branch)
    if latest:
        commit = get_latest_commit(origin, giturl, branch)
    return giturl, branch, commit


def common_options(func):
    @click.option(
        "--origin",
        help="Select KCIDB origin",
        default="maestro",
    )
    @click.option(
        "--giturl",
        help="Git URL of kernel tree ",
    )
    @click.option(
        "--branch",
        help="Branch to get results for",
    )
    @click.option(
        "--git-folder",
        help="Path of git repository folder",
    )
    @click.option(
        "--commit",
        help="Commit or tag to get results for",
    )
    @click.option(
        "--latest",
        is_flag=True,
        help="Select latest results available",
    )
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def build_and_test_options(func):
    @click.option(
        "--download-logs",
        is_flag=True,
        help="Select desired results action",
    )
    @click.option(
        "--status",
        type=click.Choice(["all", "pass", "fail", "inconclusive"], case_sensitive=True),
        help="Status of test result",
        default="all",
    )
    @click.option(
        "--filter",
        type=click.File("r"),
        help="Pass filter file for builds, boot and tests results.",
    )
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@click.group(help="[Experimental] Get results from the dashboard")
@click.pass_context
def results(ctx):
    """Commands related to results."""
    pass


@results.command()
@common_options
@click.pass_context
def summary(
    ctx,
    origin,
    git_folder,
    giturl,
    branch,
    commit,
    latest,
):
    """Display a summary of results."""
    giturl, branch, commit = set_giturl_branch_commit(
        origin, giturl, branch, commit, latest, git_folder
    )
    data = dashboard_fetch_summary(origin, giturl, branch, commit)
    cmd_summary(data)


@results.command()
@click.option(
    "--origin",
    help="Select KCIDB origin",
    default="maestro",
)
@click.pass_context
def trees(ctx, origin):
    """List trees from a give origin."""
    cmd_list_trees(origin)


@results.command()
@common_options
@build_and_test_options
@click.pass_context
def builds(
    ctx,
    origin,
    git_folder,
    giturl,
    branch,
    commit,
    latest,
    download_logs,
    status,
    filter,
):
    """Display build results."""
    giturl, branch, commit = set_giturl_branch_commit(
        origin, giturl, branch, commit, latest, git_folder
    )
    data = dashboard_fetch_builds(origin, giturl, branch, commit)
    cmd_builds(data, commit, download_logs, status)


@results.command()
@common_options
@build_and_test_options
@click.pass_context
def boots(
    ctx,
    origin,
    git_folder,
    giturl,
    branch,
    commit,
    latest,
    download_logs,
    status,
    filter,
):
    """Display boot results."""
    giturl, branch, commit = set_giturl_branch_commit(
        origin, giturl, branch, commit, latest, git_folder
    )
    data = dashboard_fetch_boots(origin, giturl, branch, commit)
    cmd_tests(data["boots"], commit, download_logs, status, filter)


@results.command()
@common_options
@build_and_test_options
@click.pass_context
def tests(
    ctx,
    origin,
    git_folder,
    giturl,
    branch,
    commit,
    latest,
    download_logs,
    status,
    filter,
):
    """Display test results."""
    giturl, branch, commit = set_giturl_branch_commit(
        origin, giturl, branch, commit, latest, git_folder
    )
    data = dashboard_fetch_tests(origin, giturl, branch, commit)
    cmd_tests(data["tests"], commit, download_logs, status, filter)


if __name__ == "__main__":
    main_kcidev()
