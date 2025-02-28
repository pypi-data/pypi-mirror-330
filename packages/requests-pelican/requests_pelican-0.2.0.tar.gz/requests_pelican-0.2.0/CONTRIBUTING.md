# Contributing to the requests-pelican

This page outlines the recommended procedure for reporting issues / giving
feedback on this project, or proposed new or modified content.

All interactions related to this project must follow the
[LIGO-Virgo-KAGRA Code of Conduct](https://dcc.ligo.org/LIGO-M1900037).

## Reporting issues / feedback

To report issues, or post feedback, please open a ticket by navigating to

<https://git.ligo.org/computing/software/requests-pelican/-/issues/new>

## Making contributions

To make a contribution, please follow the fork and
[merge request](https://git.ligo.org/help/user/project/merge_requests/index.md)
[workflow](https://git.ligo.org/help/workflow/forking_workflow.md).
This will ensure that your changes are tested and reviewed before
being deployed.

### 0. Make a fork (copy) of the project

__You only need to do this once__:

1.  Go to the [repository home page](https://git.ligo.org/computing/software/requests-pelican),
1.  click on the _Fork_ button, that should lead you
    [here](https://git.ligo.org/computing/software/requests-pelican/-/forks/new),
1.  select the namespace that you want to create the fork in, this should
    usually be your personal namespace.

If you can't see the _Fork_ button, make sure that you are logged in by
checking for your account profile avatar in the top right-hand corner of
the screen.

### 1. Clone the project

[Clone](https://git-scm.com/docs/git-clone) **the upstream project** with

```shell
git clone git@git.ligo.org:computing/software/requests-pelican.git --origin upstream
```

and then add your **fork** as a [remote](https://git-scm.com/docs/git-remote):

```shell
cd requests-pelican
git remote add origin git@git.ligo.org:<namespace>/requests-pelican.git
```

replacing `<namespace>` with your GitLab username.

### 2. Make changes

All changes should be developed on a feature branch in order to keep them
separate from other work, thus simplifying the review and merge once the
work is complete.
The workflow is:

1.  Create a new feature branch configured to track the `main` branch of the
    `upstream` repository:

    ```shell
    git fetch upstream
    git checkout -b my-new-feature upstream/main
    ```

    These commands fetch the latest changes from the `upstream` remote, then
    create the new branch `my-new-feature` based off `upstream/main`,
    and checks out the new branch.
    There are other ways to do these steps, but this is a good habit since it
    will allow you to `fetch` and `merge` changes from `upstream/main`
    directly onto the branch.

1.  Develop the changes you would like to introduce, using `git commit` to
    finalise a specific change.
    Ideally commit small units of change often, rather than creating one large
    commit at the end, this will simplify review and make modifying any changes
    easier.

    Commit messages should be clear, identifying which code was changed, and why.
    Common practice is to use a short summary line (<50 characters), followed
    by a blank line, then more information in longer lines.

1.  Push your changes to the remote copy of your fork on <https://git.ligo.org>.
    The first `push` of any new feature branch will require the
    `-u/--set-upstream` option to `push` to create a link between your new
    branch and the `origin` remote:

    ```shell
    git push --set-upstream origin my-new-feature
    ```

    Subsequent pushes can be made with

    ```shell
    git push origin my-new-feature
    ```

1.  Keep your feature branch up to date with the `upstream` repository by doing.

    ```shell
    git checkout my-new-feature
    git pull --rebase upstream main
    git push --force origin my-new-feature
    ```

    If there are conflicts between `upstream` changes and your changes, you
    will need to resolve them before pushing everything to your fork.

### 3. Open a merge request

When you feel that your work is finished, you should create a
[Merge Request](https://gitlab.com/help/user/project/merge_requests/index.html)
to propose that your changes be merged into the main (`upstream`) repository.

After you have pushed your new feature branch to `origin`, you should find a
new button on the
[repository home page](https://git.ligo.org/computing/software/requests-pelican/)
inviting you to create a merge request out of your newly pushed branch.
(If the button does not exist, you can initiate a merge request by going to
the _Merge Requests_ tab on your fork website on git.ligo.org and clicking
_New merge request_)

You should click the button, and proceed to fill in the title and description
boxes on the merge request page.

Once the request has been opened, one of the maintainers will assign someone
to review the change.
There may be suggestions and/or discussion with the reviewer.
These interactions are intended to make the resulting changes better.
The reviewer will merge your request.

Once the changes are merged into the upstream repository, you should remove
the development branch from your clone using.

```shell
git branch -d my-new-feature
```

**A feature branch should _not_ be repurposed for further development as this
can result in problems merging upstream changes.**
