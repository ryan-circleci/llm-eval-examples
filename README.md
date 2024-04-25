# LLM Eval Examples

Collection of LLM eval examples using [ai-evals orb](https://circleci.com/developer/orbs/orb/circleci/ai-evals) on CircleCI.

## Prerequisites

Before runnning any of the examples, you'll need:

- **OpenAI account** - Sign up for an OpenAI account at [openai.com](https://openai.com) to access their platform and API. Once logged into your OpenAI account, genreate your API key. Make note of the `API Key` and `Organization ID`.
- **Braintrust account** - Sign up for a Braintrust account at [www.braintrust.com](https://www.braintrust.com) to access their platform and API. Once logged into your Braintrust account, generate an `API Key` and make note of it.
- **LangSmith account** -  Sign up for a LangSmith account at [langsmith.com](https://langsmith.com) to use their language models API. AOnce logged into your LangSmith account, go to the API Keys page in your account settings to generate an API key. Copy this key to authenticate when using the LangSmith API.
- **CircleCI**
  1. **Project Setup** - Make sure your project is setup on CircleCI.
  2. **LLMOps integration** - Setup a CircleCI LLMOps integration to help run evaluations. Go to `Project Settings` > `LLMOps`. Fill out the form by Clicking `Setup Integration`. This will create a context with environment variables with the credentials you've setup above. Also _optionally_, this integration has the ability to save eval summary [Artifacts](https://circleci.com/docs/artifacts/)  and write comments on your PR's with eval results, once the context is created add a `GITHUB_TOKEN` with appropriate permissions. Make a note of the generated context name.

This will allow you to authenticate and interact with their APIs to leverage their services. See their documentation for more details on capabilities and usage.

## Orb Parameters

The [ai-evals orb](https://github.com/circleci-public/ai-evals-orb) accepts the following parameters:

_Some of the parameters are optional based on the eval platform being used._

#### Common parameters

- `circle_pipeline_id` - CircleCI Pipeline ID

- `cmd` - Command to run the evaluation

- `eval_platform` - Evaluation platform (e.g. `braintrust`, `langsmith` etc. - default: `braintrust`)

- `evals_result_location` - Location to save evaluation results (default: `./results`)

#### Braintrust specific parameters

- `braintrust_experiment_name` (optional) - Braintrust experiment name. An experiment name is generated if not set. (default: `''`)

#### Langsmith specific parameters

- `langsmith_endpoint` - Langsmith API endpoint (default: `''`)

- `langsmith_experiment_name` (optional) - Langsmith experiment name. An experiment name is generated if not set. (default: `''`)


## Examples

Fork this repo and try out the examples to evaluate language models on different platforms using the [ai-evals orb](https://circleci.com/developer/orbs/orb/circleci/ai-evals). Each example folder contains instructions and sample code to run evaluations.

These examples use CircleCI dynamic workflow that runs a specific eval based on the changes in respective folders for your chosen `eval_platform`.

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

Happy Evaluating! Let us know if you have any feedback trying these out. Jut submit an [issue](https://github.com/CircleCI-Public/llm-eval-examples/issues) on GitHub.
