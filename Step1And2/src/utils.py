def wait_for_confirmation(client, transaction_id, timeout):
    start_round = client.status()["last-round"] + 1
    current_round = start_round

    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(transaction_id)
        except Exception:
            return

        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception('pool error: {}'.format(pending_txn["pool-error"]))

        client.status_after_block(current_round)
        current_round += 1

    raise Exception('pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))


def get_default_params(client):
    params = client.suggested_params()
    params.flat_fee = True
    params.fee = 1000
    return params
