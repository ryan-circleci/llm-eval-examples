from langchain import chat_models, prompts
from langchain.evaluation import StringEvaluator
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from langsmith import Client
from typing import Any
from dataset import dataset_name
from langchain.smith import RunEvalConfig
import os
import uuid

# a new trivial change

class ConstraintEvaluator(StringEvaluator):
    @property
    def requires_reference(self):
        return True

    def _evaluate_strings(self, prediction: str, reference: str, **kwargs: Any) -> dict:
        # Reference in this case is the letter that should not be present
        return {
            "score": 1 if reference not in prediction else 0,
            "reasoning": f"prediction contains the letter {reference}",
        }


def run_eval():
    client = Client()
    experiment_name = (
        os.environ.get("CCI_LANGCHAIN_EXPERIMENT_NAME") or uuid.uuid4().hex
    )

    chain = (
        prompts.PromptTemplate.from_template(
            "Write a poem about {input} without using the letter {constraint}. Respond directly with the poem with no explanation."
        )
        | ChatOpenAI(model="gpt-3.5-turbo")
        | StrOutputParser()
    )

    eval_config = RunEvalConfig(
        custom_evaluators=[ConstraintEvaluator()],
        input_key="input",
    )

    test_results = client.run_on_dataset(
        dataset_name=dataset_name,
        llm_or_chain_factory=chain,
        evaluation=eval_config,
        project_name=experiment_name,
    )

    runs = client.list_runs(project_name=experiment_name, execution_order=1)
    for r in runs:
        print("\n\n")
        print("Feedback Stats: {}".format(r.feedback_stats))
        print("\n\n=============================================\n\n")


if __name__ == "__main__":
    run_eval()
