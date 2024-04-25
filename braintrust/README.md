# Braintrust

> Follow prerequisites in the main [README](../README.md) to set up Braintrust account and API key

This is a Braintrust eval example that demonstrates how to run evals with the [`circleci/ai-evals`](https://circleci.com/developer/orbs/orb/circleci/ai-evals) orb.

## Usage

- in [.circleci/run_evals_config.yaml](../.circleci/run_evals_config.yml) replace `ai-ai-evals-orb-examples` with context name from LLMOps integration.
- Commit and push changes to trigger workflow. Make a PR. Once pipeline completes, Braintrust eval results will be saved as follows...
    - as a comment in your PR if a `GITHUB_TOKEN` is provided in the context
    - as an eval `summary.html` [Artifact](https://circleci.com/docs/artifacts/) within your CircleCI pipeline

> :lightbulb: To trigger this workflow again make sure to do some simple changes in braintrust folder like adding a space and commiting.
