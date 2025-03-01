from google.cloud import dataform_v1beta1

dataform = dataform_v1beta1.DataformClient()

def create_compilation_result(project, location, repo, source_type, source):
    compilation_result = dataform_v1beta1.CompilationResult()
    if source_type in ['git_commit', 'git_tag', 'git_branch']:
        compilation_result.git_commitish = source
    elif source_type == 'workspace':
        compilation_result.workspace = f'projects/{project}/locations/{location}/repositories/{repo}/workspaces/{source}'
    elif source_type == 'release_config':
        compilation_result.release_config = f'projects/{project}/locations/{location}/repositories/{repo}/releaseConfigs/{source}'
    else:
        assert False, 'source_type should be among [git_commit, git_tag, git_branch, workspace, release_config]'

    return dataform.create_compilation_result(
        parent=f'projects/{project}/locations/{location}/repositories/{repo}',
        compilation_result=compilation_result
    )


def create_workflow_invocation(project, location, repo, compilation_result):

    # Initialize request argument(s)
    workflow_invocation = dataform_v1beta1.WorkflowInvocation()
    workflow_invocation.compilation_result = compilation_result.name

    # Make the request
    response = dataform.create_workflow_invocation(
        parent=f'projects/{project}/locations/{location}/repositories/{repo}',
        workflow_invocation=workflow_invocation,
    )

    # Handle the response
    print(response)