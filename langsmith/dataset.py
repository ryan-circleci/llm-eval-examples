from langsmith import Client

dataset_name = f"Download Feedback and Examples - AI Eval Example"

def create_dataset():
    client = Client()

    examples = [
        ("roses", "o"),
        ("vikings", "v"),
        ("planet earth", "e"),
        ("Sirens of Titan", "t"),
        ("Tears of valhala", "marvel")
    ]

    dataset = client.create_dataset(dataset_name)

    for prompt, constraint in examples:
        client.create_example(
            {"input": prompt, "constraint": constraint},
            dataset_id=dataset.id,
            outputs={"constraint": constraint},
        )
    
    print("Created dataset \"{}\"".format(dataset_name))

if __name__ == "__main__":
    create_dataset()
