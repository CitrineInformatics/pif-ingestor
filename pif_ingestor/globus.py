import os

interval_time = 10
default_collection = 35  # MDF Test collection

def push_to_globus(paths, metadata={}, collection=default_collection, src_ep=None, verbose=False):
    """Upload files in path to globus collection"""
    try:
        from globus_sdk import GlobusError, TransferData
        from mdf_forge import toolbox
    except ImportError:
        raise ImportError("Install 'globus_sdk' and 'mdf_forge' before uploading to globus")

    # Set up clients
    config = {
        "app_name": "PIF Ingestor",
        "services": ["transfer", "publish"]
        }
    clients = toolbox.login(config)
    transfer_client = clients["transfer"]
    publish_client = clients["publish"]
    src_endpoint = src_ep or toolbox.get_local_ep(transfer_client)

    # Process metadata
    if not metadata.get("accept_license"):
        usr_res = input("Do you accept the license for collection " + str(collection) + "? y/n: ").strip().lower()
        if usr_res == 'y' or usr_res == "yes":
            metadata["accept_license"] = True

    # Upload the metadata
    result = publish_client.push_metadata(collection, metadata)
    dest_endpoint = result['globus.shared_endpoint.name']
    dest_path = os.path.join(result['globus.shared_endpoint.path'], "data")
    submission_id = result['id']
    if verbose:
        print("Metadata uploaded")

    # Transfer the file(s)
    tdata = TransferData(transfer_client, src_endpoint, dest_endpoint, notify_on_succeeded=False, notify_on_inactive=False, notify_on_failed=False)
    for src_path in paths:

        #TODO: Optimize this loop
        # Add each dir from the source path to the dest path, creating if needed on the dest ep
        full_dest_path = dest_path
        for dirc in os.path.dirname(src_path).strip("/").split("/"):
            full_dest_path = os.path.join(full_dest_path, dirc)
            try:
                transfer_client.operation_mkdir(dest_endpoint, full_dest_path)
            except GlobusAPIError as e:
                # If path already created, continue
                if e.status_code == 502:
                    pass
                else:
                    raise
        full_dest_path = os.path.join(full_dest_path, os.path.basename(src_path))

        tdata.add_item(os.path.abspath(src_path), full_dest_path, recursive=False)
    transfer_res = transfer_client.submit_transfer(tdata)

    # Wait for transfer to complete
    if transfer_res["code"] != "Accepted":
        raise GlobusError("Failed to transfer files: Transfer " + res["code"])
    else:
        if verbose:
            print("Data transfer submitted")
        while not transfer_client.task_wait(transfer_res["task_id"], timeout=interval_time, polling_interval=interval_time):
            for event in transfer_client.task_event_list(transfer_res["task_id"]):
                if event["is_error"]:
                    transfer_client.cancel_task(transfer_res["task_id"])
                    raise GlobusError("Error: " + event["description"])
                if config_data["timeout"] and intervals >= timeout_intervals:
                    transfer_client.cancel_task(transfer_res["task_id"])
                    raise GlobusError("Transfer timed out.")
        if verbose:
            print("Transfer complete")

    # Complete publication
    fin_res = publish_client.complete_submission(submission_id)
    if verbose:
        print("Submission complete")
        print("Result:", result.data)

    return {
        "local_path": src_path,
        "globus_path": full_dest_path,
        "globus_info": result.data
        }

