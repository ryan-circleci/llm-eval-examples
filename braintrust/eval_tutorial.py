from braintrust import Eval
from autoevals import LevenshteinScorer
from datasets import load_dataset
import braintrust
import os
from openai import OpenAI
import uuid

# a trivial change

# Load dataset from Huggingface.
dataset = load_dataset("ag_news", split="train")

# Extract category names from the dataset and build a map from index to
# category name. We will use this to compare the expected categories to
# those produced by the model.
category_names = dataset.features["label"].names
category_map = dict([name for name in enumerate(category_names)])

# Shuffle and trim to 20 datapoints. Restructure our dataset
# slightly so that each item in the list contains an input
# being the title and the expected category index label.
trimmed_dataset = dataset.shuffle(seed=42)[:20]
articles = [
    {
        "input": trimmed_dataset["text"][i],
        "expected": category_map[trimmed_dataset["label"][i]],
    }
    for i in range(len(trimmed_dataset["text"]))
]

client = braintrust.wrap_openai(
    OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
)

MODEL = "gpt-3.5-turbo"
SEED = 123

@braintrust.traced
def classify_article(input):
    messages = [
        {
            "role": "system",
            "content": """You are an editor in a newspaper who helps writers identify the right category for their news articles,
by reading the article's title. The category should be one of the following: World, Sports, Business or Sci/Tech. Reply with one word corresponding to the category.""",
        },
        {
            "role": "user",
            "content": "Article title: {article_title} Category:".format(article_title=input),
        },
    ]
    result = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=10,
        seed=SEED,
    )
    category = result.choices[0].message.content
    return category


braintrust.login(api_key=os.environ.get("BRAINTRUST_API_KEY"))

def run_evaluation(dataset):
    experiment_name = os.environ.get("BRAINTRUST_EXPERIMENT_NAME") or uuid.uuid4().hex
    with braintrust.init(project="Classifying News Articles Cookbook", experiment=experiment_name) as experiment: 
        for data in dataset:
            input_data = data["input"]
            expected = data["expected"]
 
            output = classify_article(input_data)
 
            levenshtein = LevenshteinScorer()
            factualityScore = levenshtein(output, expected, input=input_data)

            span = experiment.start_span(name="Evaluation")
            span.log(
                input=input_data,
                output=output,
                expected=expected,
                scores={
                    factualityScore.name: factualityScore.score,
                }, # The scores dictionary
                # tags=[]("type": "Test")],# The metadata dictionary
            )
            span.close()
        summary = experiment.summarize(summarize_scores=True)

run_evaluation(articles)
