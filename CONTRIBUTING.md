# Contributing to Marathon Autoscaler

Thank you for considering making a contribution to this project!  We sincerely appreciate your time and energy invested in getting to know this project's code. We are also appreciative that you've taken time to read this guideline and cared enough to contriubute. 

The following is a set of guidelines for contributing to the Marathon Autoscaler project.
These are just guidelines, not rules, use your best judgment and feel free to propose changes to this document in a pull request.

#### Table Of Contents

[What should I know before I get started?](#what-should-i-know-before-i-get-started)
  * [Code of Conduct](#code-of-conduct)


[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Your First Code Contribution](#your-first-code-contribution)
  * [Pull Requests](#pull-requests)

[Styleguides](#styleguides)
  * [Git Commit Messages](#git-commit-messages)
  * [Documentation Styleguide](#documentation-styleguide)

[Additional Notes](#additional-notes)
  * [Issue and Pull Request Labels](#issue-and-pull-request-labels)

## What should I know before I get started?

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

Before creating bug reports, please perform a [cursory search](https://github.com/tendrilinc/marathon-autoscaler/issues?q=is%3Aissue)** to see if the problem has already been reported. If it has, add a comment to the existing issue instead of opening a new one. When you are creating a bug report, please [include as many details as possible](#how-do-i-submit-a-good-bug-report). If you'd like, you can use [this template](#template-for-submitting-bug-reports) to structure the information.


#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/).

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible. When listing steps, **don't just say what you did, but explain how you did it**.
* **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples. If you're providing snippets in the issue, use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**
* **Include the Autoscaler's logging output.** Copy the pertinent snippet of log information from the Autoscaler's standard out. **If the log output is too long, please open a public Gist** and include the link to this Gist with your report. 
Provide more context by answering these questions:

* **Did the problem start happening recently** (e.g. after updating to a new version) or was this always a problem?
* If the problem started happening recently, **can you reproduce the problem in an older version of Autoscaler?** What's the most recent version in which the problem doesn't happen?
* **Can you reliably reproduce the issue?** If not, provide details about how often the problem happens and under which conditions it normally happens.


Include details about your configuration and environment:

* **Which versions of Marathon and Mesos are you using?**
* **What's the name(s) and version(s) of the OS(es) you're running**?
* **Are you running the Autoscaler in Docker Machine locally or on Mesos/Marathon**?
* **Other configuration information that you believe to be relevant**


### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for Autoscaler, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion and find related suggestions.

Before creating enhancement suggestions, please check [this list](#before-submitting-an-enhancement-suggestion) as you might find out that you don't need to create one. When you are creating an enhancement suggestion, please [include as many details as possible](#how-do-i-submit-a-good-enhancement-suggestion). If you'd like, you can use [this template](#template-for-submitting-enhancement-suggestions) to structure the information.

#### Before Submitting An Enhancement Suggestion

* **Perform a [cursory search](https://github.com/tendrilinc/marathon-autoscaler/issues?q=is%3Aissue)** to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.

#### How Do I Submit A (Good) Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://guides.github.com/features/issues/). Provide the following information:

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include copy/pasteable snippets which you use in those examples, as [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Explain why this enhancement would be useful**.

#### Template For Submitting Enhancement Suggestions

    [Short description of suggestion]

    **Steps which explain the enhancement**

    1. [First Step]
    2. [Second Step]
    3. [Other Steps...]

    **Current and suggested behavior**

    [Describe current and suggested behavior here]

    **Why would the enhancement be useful to most users**

    [Explain why the enhancement would be useful to most users]

### Your First Code Contribution

Unsure where to begin contributing to Autoscaler? You can start by looking through these `beginner` and `help-wanted` issues:

* [Beginner issues][beginner] - issues which should only require a few lines of code, and a test or two.
* [Help wanted issues][help-wanted] - issues which should be a bit more involved than `beginner` issues.

Both issue lists are sorted by total number of comments. While not perfect, number of comments is a reasonable proxy for impact a given change will have.

### Pull Requests

* Reference the Github Issue 
* Document new code based on the
  [Documentation Styleguide](#documentation-styleguide)
* End files with a newline.

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally
* When only changing documentation, include `[ci skip]` in the commit description
* Consider starting the commit message with an applicable emoji:
    * :art: `:art:` when improving the format/structure of the code
    * :racehorse: `:racehorse:` when improving performance
    * :non-potable_water: `:non-potable_water:` when plugging memory leaks
    * :memo: `:memo:` when writing docs
    * :penguin: `:penguin:` when fixing something on Linux
    * :apple: `:apple:` when fixing something on Mac OS
    * :checkered_flag: `:checkered_flag:` when fixing something on Windows
    * :bug: `:bug:` when fixing a bug
    * :fire: `:fire:` when removing code or files
    * :green_heart: `:green_heart:` when fixing the CI build
    * :white_check_mark: `:white_check_mark:` when adding tests
    * :lock: `:lock:` when dealing with security
    * :arrow_up: `:arrow_up:` when upgrading dependencies
    * :arrow_down: `:arrow_down:` when downgrading dependencies
    * :shirt: `:shirt:` when removing linter warnings

### Documentation Styleguide

* Use [PyLint](https://www.pylint.org).
* Use [Markdown](https://daringfireball.net/projects/markdown).

## Additional Notes

### Issue and Pull Request Labels

This section lists the labels we use to help us track and manage issues and pull requests.

[GitHub search](https://help.github.com/articles/searching-issues/) makes it easy to use labels for finding groups of issues or pull requests you're interested in. To help you find issues and pull requests, each label is listed with search links for finding open items with that label. We  encourage you to read about [other search filters](https://help.github.com/articles/searching-issues/) which will help you write more focused queries.

The labels are loosely grouped by their purpose, but it's not required that every issue have a label from every group or that an issue can't have more than one label from the same group.

Please open an issue if you have suggestions for new labels, and if you notice some labels are missing on some repositories, then please open an issue on that repository.

#### Type of Issue and Issue State

| Label name | :mag_right: | Description |
| --- | --- | --- |
| `enhancement` | [search][search-label-enhancement] | Feature requests. |
| `bug` | [search][search-label-bug] | Confirmed bugs or reports that are very likely to be bugs. |
| `question` | [search][search-label-question] | Questions more than bug reports or feature requests (e.g. how do I do X). |
| `feedback` | [search][search-label-feedback] | General feedback more than bug reports or feature requests. |
| `help-wanted` | [search][search-label-help-wanted] | The core team would appreciate help from the community in resolving these issues. |
| `beginner` | [search][search-label-beginner] | Less complex issues which would be good first issues to work on for users who want to contribute to Marathon Autoscaler. |
| `more-information-needed` | [search][search-label-more-information-needed] | More information needs to be collected about these problems or feature requests (e.g. steps to reproduce). |
| `needs-reproduction` | [search][search-label-needs-reproduction] | Likely bugs, but haven't been reliably reproduced. |
| `blocked` | [search][search-label-blocked] | Issues blocked on other issues. |
| `duplicate` | [search][search-label-duplicate] | Issues which are duplicates of other issues, i.e. they have been reported before. |
| `wontfix` | [search][search-label-wontfix] | The core team has decided not to fix these issues for now, either because they're working as intended or for some other reason. |
| `invalid` | [search][search-label-invalid] | Issues which aren't valid (e.g. user errors). |


#### Topic Categories

| Label name | :mag_right: | Description |
| --- | --- | --- |
| `documentation` | [search][search-label-documentation] | Related to any type of documentation. |
| `performance` | [search][search-label-performance] | Related to performance. |
| `security` | [search][search-label-security] | Related to security. |
| `api` | [search][search-label-api] | Related to APIs. |
| `uncaught-exception` | [search][search-label-uncaught-exception] | Issues about uncaught exceptions. |
| `crash` | [search][search-label-crash] | Reports of crashing. |
| `network` | [search][search-label-network] | Related to network problems or working with remote files (e.g. on network drives). |
| `git` | [search][search-label-git] | Related to Git functionality (e.g. problems with gitignore files or with showing the correct file status). |
| `build-error` | [search][search-label-build-error] | Related to problems with building from source. |


#### Pull Request Labels

| Label name | :mag_right: | Description
| --- | --- | --- |
| `work-in-progress` | [search][search-label-work-in-progress] | Pull requests which are still being worked on, more changes will follow. |
| `needs-review` | [search][search-label-needs-review] | Pull requests which need code review, and approval from maintainers or core team. |
| `under-review` | [search][search-label-under-review] | Pull requests being reviewed by maintainers or core team. |
| `requires-changes` | [search][search-label-requires-changes] | Pull requests which need to be updated based on review comments and then reviewed again. |
| `needs-testing` | [search][search-label-needs-testing] | Pull requests which need manual testing. |

[search-label-enhancement]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Aenhancement
[search-label-bug]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Abug
[search-label-question]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Aquestion
[search-label-feedback]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Afeedback
[search-label-help-wanted]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Ahelp-wanted
[search-label-beginner]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Abeginner
[search-label-more-information-needed]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Amore-information-needed
[search-label-needs-reproduction]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Aneeds-reproduction
[search-label-triage-help-needed]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Atriage-help-needed
[search-label-documentation]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Adocumentation
[search-label-performance]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Aperformance
[search-label-security]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Asecurity
[search-label-api]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Aapi
[search-label-crash]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Acrash
[search-label-network]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Anetwork
[search-label-uncaught-exception]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Auncaught-exception
[search-label-git]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Agit
[search-label-blocked]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Ablocked
[search-label-duplicate]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Aduplicate
[search-label-wontfix]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Awontfix
[search-label-invalid]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Ainvalid
[search-label-build-error]: https://github.com/issues?q=is%3Aopen+is%3Aissue+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Abuild-error
[search-label-work-in-progress]: https://github.com/pulls?q=is%3Aopen+is%3Apr+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Awork-in-progress
[search-label-needs-review]: https://github.com/pulls?q=is%3Aopen+is%3Apr+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Aneeds-review
[search-label-under-review]: https://github.com/pulls?q=is%3Aopen+is%3Apr+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Aunder-review
[search-label-requires-changes]: https://github.com/pulls?q=is%3Aopen+is%3Apr+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Arequires-changes
[search-label-needs-testing]: https://github.com/pulls?q=is%3Aopen+is%3Apr+repo%3Atendrilinc%2Fmarathon-autoscaler+label%3Aneeds-testing

[beginner]:https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Abeginner+label%3Ahelp-wanted++repo%3Atendrilinc%2Fmarathon-autoscale+sort%3Acomments-desc
[help-wanted]:https://github.com/issues?q=is%3Aopen+is%3Aissue+label%3Ahelp-wanted+repo%3Atendrilinc%2Fmarathon-autoscale+sort%3Acomments-desc).
* Use [Markdown](https://daringfireball.net/projects/markdown).
