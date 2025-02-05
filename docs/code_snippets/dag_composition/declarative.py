from dagger import DAG, FromNodeOutput, FromParam, FromReturnValue, Task

DataSet = str


#
# DAG that processes and transforms a dataset
# ===========================================
#
def encode_field_a(dataset: DataSet) -> DataSet:
    return f"{dataset}, with field a encoded"


def aggregate_fields_b_and_c(dataset: DataSet) -> DataSet:
    return f"{dataset}, with fields b and c aggregated"


def calculate_moving_average_for_d(dataset: DataSet) -> DataSet:
    return f"{dataset}, with moving average for d calculated"


def dataset_transformation_dag(dataset_input: FromNodeOutput) -> DAG:
    return DAG(
        inputs={"dataset": dataset_input},
        nodes={
            "encode-field-a": Task(
                encode_field_a,
                inputs={"dataset": FromParam("dataset")},
                outputs={"dataset": FromReturnValue()},
            ),
            "aggregate-fields-b-and-c": Task(
                aggregate_fields_b_and_c,
                inputs={"dataset": FromNodeOutput("encode-field-a", "dataset")},
                outputs={"dataset": FromReturnValue()},
            ),
            "calculate-moving-average-for-d": Task(
                calculate_moving_average_for_d,
                inputs={
                    "dataset": FromNodeOutput("aggregate-fields-b-and-c", "dataset")
                },
                outputs={"dataset": FromReturnValue()},
            ),
        },
        outputs={
            "dataset": FromNodeOutput("calculate-moving-average-for-d", "dataset")
        },
    )


#
# DAG that retrieves the dataset and invokes the previous DAG for each chunk
# ==========================================================================
#
def retrieve_dataset() -> DataSet:
    return "original dataset"


dag = DAG(
    nodes={
        "retrieve-dataset": Task(
            retrieve_dataset,
            outputs={"dataset": FromReturnValue()},
        ),
        "transform-dataset": dataset_transformation_dag(
            FromNodeOutput("retrieve-dataset", "dataset"),
        ),
    },
    outputs={
        "dataset": FromNodeOutput("transform-dataset", "dataset"),
    },
)
