from kedro.pipeline import Pipeline, node, pipeline

base_data_extraction_pipe = pipeline(
    [
        node(
            lambda x: x,
            inputs="DB.storesStockSnapshot",
            outputs="01_raw.storesStockSnapshot",
            namespace="query_db_nodes",
            tags="estoque",
        ),
        node(
            lambda x: x,
            inputs="DB.produtos",
            outputs="01_raw.produtos",
            namespace="query_db_nodes",
            tags="produto",
        ),
        node(
            lambda x: x,
            inputs="DB.transactions",
            outputs="01_raw.transactions",
            namespace="query_db_nodes",
            tags="transacao",
        ),
    ],
)


def create_pipeline(**kwargs) -> Pipeline:
    ds_pipe = pipeline(
        base_data_extraction_pipe,
        namespace="ds",
    )

    averara_pipe = pipeline(
        base_data_extraction_pipe,
        namespace="averara",
    )

    botti_pipe = pipeline(
        base_data_extraction_pipe,
        namespace="botti",
    )

    casaprado_pipe = pipeline(
        base_data_extraction_pipe,
        namespace="casaprado",
    )

    capodarte_pipe = pipeline(
        base_data_extraction_pipe,
        namespace="capodarte",
    )

    return ds_pipe + averara_pipe + botti_pipe + casaprado_pipe + capodarte_pipe
