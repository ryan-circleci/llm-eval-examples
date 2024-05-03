# LLM Eval Examples

A collection of LLM eval examples using the [CircleCI Evals Orb](https://circleci.com/developer/orbs/orb/circleci/evals).

## Prerequisites

Before running any of the examples, you'll need:

- A **CircleCI account** connected to your code. You can [sign up for free](https://circleci.com/signup/).
- An **OpenAI account**. Sign up for an OpenAI account at [openai.com](https://openai.com) to access their platform and API. Once logged into your OpenAI account, generate your API key. Make note of the `API Key` and `Organization ID`.

Depending on your choice of evaluation provider, you will also need one of the following:

- A **Braintrust account**. Sign up for a Braintrust account at [braintrustdata.com](https://www.braintrustdata.com) to access their platform and API. Once logged into your Braintrust account, generate an `API Key` and make note of it.
- A **LangSmith account**. Sign up for a LangSmith account at [langsmith.com](https://langsmith.com) to use their language models API. Once logged into your LangSmith account, go to the API Keys page in your account settings to generate an API key. Copy this key to authenticate when using the LangSmith API.

The API keys will allow you to authenticate and interact with the APIs of your LLMOps tools to leverage their services.

See their documentation for more details on capabilities and usage.

## Getting started

Fork this repo to run evaluations on a LLM-based application using the [evals orb](https://circleci.com/developer/orbs/orb/circleci/evals).

This repository includes evaluations that can be run on two evaluation platforms: [Braintrust](https://www.braintrustdata.com/) and [LangSmith](https://smith.langchain.com/). Each example folder contains instructions and sample code to run evaluations.

### Here's the process...

1. Enter your credentials into CircleCI, which get stored as environment variables on a new context.
2. Update the CircleCI configuration file with your newly-created context.
3. Select the evaluation platform where you want to run evaluations.

### Step 1. Enter credentials into CircleCI

Entering your OpenAI, Braintrust, and LangSmith credentials into CircleCI is easy.

Just navigate to `Project Settings` > `LLMOps` and fill out the form by Clicking `Set up Integration`.

![Create Context](images/create-context.png)

This will create a context with environment variables for the credentials you've set up above.

:warning: _Please take note of the generated context name (e.g. `ai-llm-eval-examples`). This will be used in the next step to update `context` value in the CircleCI configuration file._

![LLMOps Integration Context](images/LLMOps-Integration-Context.png)

:bulb: You can also optionally [store a `GITHUB_TOKEN`](#to-enable-the-evals-orb-to-post-eval-job-summaries-on-github-pull-requests) as an environment variable on this context, if you'd like your pipelines to post summarized eval job results as comments on GitHub pull requests.

### Step 2. Update CircleCI config with your newly-created context

Once your credentials have been entered, make sure you update the evals `context` parameter in the `.circleci/run_evals_config.yml` file with the name of the context you just created in Step 1.

This will ensure that your credentials get used properly by the evaluation scripts in the following steps.

```yml
# WORKFLOWS
workflows:
  braintrust-evals:
    when: << pipeline.parameters.run-braintrust-evals >>
    jobs:
      - run-braintrust-evals:
          context:
            - ai-llm-evals-orb-examples # Replace this with your context name
  langsmith-evals:
    when: << pipeline.parameters.run-langsmith-evals >>
    jobs:
      - run-langsmith-evals:
          context:
            - ai-llm-evals-orb-examples # Replace this with your context name
```

### Step 3. Select your evaluation platform

#### Braintrust

The Braintrust example imports from HuggingFace an evaluation dataset of news articles, and uses ChatGPT to help classify them into category. The dataset contains both the news article and the expected category for each of them. As an evaluation metric, we use the Levenshtein distance, which tells us how distant the answer provided by ChatGPT is from the expected answer. Each individual test case is scored, and a summary score for the whole dataset is also available.

<img style="text-align:center" width="300" alt="CircleCI-llmops" src="https://github.com/CircleCI-Public/llm-eval-examples/assets/19594309/93595b21-abe2-4c74-8a15-1ed08e19dd0d">

#### LangSmith

In the LangSmith example, we instantiate the dataset ourselves. Ahead of triggering your evaluation via CircleCI, run the following commands:

```
cd ./experiments/ai-langsmith
pip install -r ./requirements.txt
python dataset.py
```

The dataset contains a list of topics which we want ChatGPT to write poems about. It also contains, for each topic, a letter or word which should not be included in the poem. In our evaluation, we use the LangSmith `ConstraintEvaluator` to verify whether our LLM has accurately avoided using the letter or word. By accessing the LangSmith platform we are able to access all scores by test case.

#### The Results

Whichever evaluation platform you choose, as evals are run through the [evals orb](https://circleci.com/developer/orbs/orb/circleci/evals), CircleCI stores the summary of eval results as a job [artifact](https://circleci.com/docs/artifacts/).

<img style="text-align:center" width="370" alt="Screenshot 2024-04-30 at 10 19 53" src="https://github.com/CircleCI-Public/llm-eval-examples/assets/19594309/9df64653-d1b7-41c5-8830-f8d8d497bdca">

If a [`GITHUB_TOKEN`](#to-enable-the-evals-orb-to-post-eval-job-summaries-on-github-pull-requests) has been set up, the orb will also post summarized eval results as a PR comment:

<img style="text-align:center" width="700" alt="Screenshot 2024-04-30 at 10 21 48" src="https://github.com/CircleCI-Public/llm-eval-examples/assets/19594309/73c628b0-de35-41f2-8f06-7e486691cea6">

### A few notes about CircleCI config...

The `.circleci/run_evals_config.yml` file uses the [evals orb](https://circleci.com/developer/orbs/orb/circleci/evals) to define jobs that run the evaluation code in each example folder. The orb handles setting up the evaluation environment, executing the evaluations, and collecting the results.

For example, the Braintrust job runs the Python script in `braintrust/eval_tutorial.py` by passing it as the `cmd` parameter. It saves the evaluation results to the location specified with `evals_result_location`.

Similarly, the LangSmith job runs the Python script in `langsmith/eval.py`.

To change where the results of the evaluation are being saved, go to the `evals/eval` step, and add the parameter `evals_result_location`:

_Note: the [evals orb](https://circleci.com/developer/orbs/orb/circleci/evals) will make the directory if it does not exist._

```yaml
- evals/eval:
    circle_pipeline_id: << pipeline.id >>
    eval_platform: ...
    evals_result_location: "./my-results-here"
    cmd: ...
```

### To enable the [evals orb](https://circleci.com/developer/orbs/orb/circleci/evals) to post eval job summaries on GitHub pull requests:

- Generate a [GitHub Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) with `repo` scope.
- Add this token as the environment variable [`GITHUB_TOKEN`](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) in CircleCI project settings. Alternatively, you could include this secret in the context that was created when [you entered your credentials](#step-1-enter-credentials-into-circleci) as part of LLMOps Integration.

### A note about dynamic configuration

The examples included in this repository use [dynamic configuration](https://circleci.com/docs/dynamic-config/) to selectively run only the evaluations defined in the folder that changed. So, for changes committed to the folder `braintrust`, only your Braintrust evaluations will be run; for changes committed to the folder `langsmith`, only your LangSmith evaluations will be run.

```shell
.
├── README.md
├── braintrust
│   ├── eval_tutorial.py
│   ├── README.md
│   └── requirements.txt
└── langsmith
    ├── dataset.py
    ├── eval.py
    ├── README.md
    └── requirements.txt
```

## The CircleCI Evals Orb

The [CircleCI Evals Orb](https://circleci.com/developer/orbs/orb/circleci/evals) simplifies the definition and execution of evaluation jobs using popular third-party tools, and generates reports of evaluation results.

Given the volatile nature of evaluations, evaluations orchestrated by the [evals orb](https://circleci.com/developer/orbs/orb/circleci/evals) do not halt the pipeline if an evaluation fails. This approach ensures that the inherent flakiness of evaluations does not disrupt the development cycle.

Instead, a summary of the evaluation results can _optionally_ be presented:

- as an [artifact](https://circleci.com/docs/artifacts/) within the CircleCI pipeline job
- as a comment on the corresponding GitHub pull request (requires a [GitHub Personal Access Token](#to-enable-the-evals-orb-to-post-eval-job-summaries-on-github-pull-requests))

### Orb Parameters

The [evals orb](https://circleci.com/developer/orbs/orb/circleci/evals) accepts the following parameters:

_Some of the parameters are optional based on the eval platform being used._

#### Common parameters

- **`circle_pipeline_id`**: CircleCI Pipeline ID

- **`cmd`**: Command to run the evaluation

- **`eval_platform`**: Evaluation platform (e.g. `braintrust`, `langsmith` etc.; default: `braintrust`)

- **`evals_result_location`**: Location to save evaluation results (default: `./results`)

#### Braintrust-specific parameters

- **`braintrust_experiment_name`** _(optional)_: Braintrust experiment name
  - If no value is provided, an experiment name will be auto-generated based on an MD5 hash of `<CIRCLE_PIPELINE_ID>_<CIRCLE_WORKFLOW_ID>`.

#### LangSmith-specific parameters

- **`langsmith_endpoint`** _(optional)_: LangSmith API endpoint (default: `https://api.smith.langchain.com`)

- **`langsmith_experiment_name`** _(optional)_: LangSmith experiment name
  - If no value is provided, an experiment name will be auto-generated based on an MD5 hash of `<CIRCLE_PIPELINE_ID>_<CIRCLE_WORKFLOW_ID>`.

## Happy Evaluating!

Let us know if you have any feedback trying these out.

Submit an [issue](https://github.com/CircleCI-Public/llm-eval-examples/issues) on GitHub, or reach out to us at [ai-feedback@circleci.com](mailto:ai-feedback@circleci.com).
