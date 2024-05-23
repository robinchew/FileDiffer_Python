import json
from pygit2 import Repository

class RevisionStringError(Exception):
    pass

def get_diff(repo_path, target_revision_string, source_revision_string=None):
    """
    Returns the diff between two revision strings of the repo found at repo_path
    """

    # TODO: this raises GitError if repo not found at repo_path
    # handle on Erlang side?
    repo = Repository(repo_path)
    
    # When source is not provided, the diff is done between the head
    if source_revision_string is None:
        source_revision_string = repo.head.shorthand
    
    # parse the rev strings to get the desired commits for the diff
    try:
        source_commit = repo.revparse_single(source_revision_string)
        target_commit = repo.revparse_single(target_revision_string)
    except KeyError as e:
        raise RevisionStringError(f"Error in parsing revision string: {e}")

    # get the diff
    diff = repo.diff(target_commit, source_commit)
    
    diff_data = {
        "source_branch": source_revision_string,
        "target_branch": target_revision_string,
        "source_commit_id": str(source_commit.id),
        "target_commit_id": str(target_commit.id),
        "diff_summary": {
            "total_files_changed": diff.stats.files_changed,
            "total_insertions": diff.stats.insertions,
            "total_deletions": diff.stats.deletions
        },
        "changes": format_diff_changes(diff),
    }
    
    return diff_data

def format_diff_changes(diff):
    """
    Shape the diff information from the diff object returned by pygit2 for use with json.dumps()
    """
    return [
        {  
            "file_path": patch.delta.new_file.path,  
            "added_lines": patch.line_stats[1],  
            "deleted_lines": patch.line_stats[2],  
            "hunks": [  
                {  
                    "header": hunk.header,  
                    "lines": [  
                        {  
                            "content": line.content.strip(),  
                            "type": line.origin,  
                            "new_lineno": line.new_lineno,  
                            "old_lineno": line.old_lineno  
                        }  
                        for line in hunk.lines  
                    ]  
                }  
                for hunk in patch.hunks  
            ]  
        }  
        for patch in diff  
    ]

def get_diff_json_from_args(*args):
    """
    This function is called with a path to a directory containing a git repo,
        a target revision string, and optionally a source revision string to
        generate a diff and return it as a json
    """
    git_dir = args[0].decode()
    diff_target = args[1].decode()
    diff_source = args[2].decode() if len(args) > 2 else None

    diff_data = get_diff(git_dir, diff_target, diff_source)

    return json.dumps(diff_data, indent=4)
