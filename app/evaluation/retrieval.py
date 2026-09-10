
# Essa função compara: IDs recuperados X IDs esperados
def calculate_recall_at_k(
        retrieved_ids,
        expected_ids,
):
    retrieved_ids = set(retrieved_ids)
    expected_ids = set(expected_ids)

    if not expected_ids:
        return 0.0

    relevant_retrieved = retrieved_ids.intersection(
        expected_ids
    )

    return len(relevant_retrieved) / len(expected_ids)