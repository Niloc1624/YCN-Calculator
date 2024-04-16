import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore, firestore_async
import json
import asyncio
import os


def pull_dicts_from_firebase(local=False):
    """
    Retrieves dicts from a Firebase collection and returns them as a dictionary.

    Args:
        local (bool, optional): If True, saves the retrieved dicts to a local file named "final_dict.json". Defaults to False.

    Returns:
        dict: A dictionary containing the retrieved dicts.
    """
    db, _ = _firebase_auth()
    old_results_dict = {}
    docs = db.collection("results").stream()
    for doc in docs:
        doc_dict = doc.to_dict()
        old_results_dict.update(doc_dict)

    # save final_dict to json
    if local:
        with open("final_dict.json", "w") as f:
            json.dump(old_results_dict, f, indent=2)
    return old_results_dict


def upload_dict_to_firebase(new_results_dict, local=False, entries_per_dict=1000):
    """
    Uploads the new_results_dict to Firebase.

    Args:
        new_results_dict (dict): The dictionary containing the new results to be uploaded.
        local (bool, optional): Flag indicating whether to also download locally. Defaults to False.
        entries_per_dict (int, optional): The maximum number of entries per dictionary. Defaults to 1000.
    """
    asyncio.run(_upload_async(new_results_dict, local, entries_per_dict))
    # _upload(new_results_dict, local, entries_per_dict)


def delete_all_documents_from_firebase():
    """
    Deletes all documents in the 'results' collection in the Firebase Firestore database.
    """
    db, _ = _firebase_auth()
    docs = db.collection("results").stream()
    for doc in docs:
        doc.reference.delete()


def _firebase_auth():
    """
    Authenticate with Firebase and return the Firestore database instances.

    Returns:
        tuple: A tuple containing two Firestore database instances - `db` and `db_async`.
    """
    key_dict = json.loads(st.secrets["textkey"])
    cred = credentials.Certificate(key_dict)

    # Check if default app is already initialized
    try:
        app = firebase_admin.get_app()
    except ValueError:
        # If app is not initialized, initialize a new app
        app = firebase_admin.initialize_app(cred)

    db = firestore.client(app)
    db_async = firestore_async.client(app)
    return db, db_async


async def _upload_to_firebase_async(dict_name, dict_data, db_async):
    """
    Uploads a dictionary to Firebase Firestore.

    Args:
        dict_name (str): The name of the dictionary.
        dict_data (dict): The data to be uploaded.
        db_async: The Firebase Firestore database object.

    Returns:
        None
    """
    result_dict = db_async.collection("results").document(dict_name)
    await result_dict.set(dict_data)


def _split_dict_by_number(new_results_dict, entries_per_dict, local):
    """
    Splits a dictionary into multiple smaller dictionaries based on the specified number of entries per dictionary.

    Args:
        new_results_dict (dict): The dictionary to be split.
        entries_per_dict (int): The maximum number of entries per dictionary.
        local (bool): Indicates whether the split dictionaries should be saved locally.

    Returns:
        dict: A dictionary containing the split dictionaries, where the keys are the names of the split dictionaries
              and the values are the corresponding dictionaries.

    """
    keys = list(new_results_dict.keys())
    num_dicts = (
        len(keys) + entries_per_dict - 1
    ) // entries_per_dict  # Calculate the number of dicts needed

    split_dicts = {}

    for i in range(num_dicts):
        start_idx = i * entries_per_dict
        end_idx = min((i + 1) * entries_per_dict, len(keys))
        output_data = {key: new_results_dict[key] for key in keys[start_idx:end_idx]}

        dict_name = f"part_{i+1:02}"
        split_dicts[dict_name] = output_data

        if local:
            output_file = os.path.join("split_jsons", f"{dict_name}.json")
            with open(output_file, "w") as f:
                json.dump(output_data, f, indent=4)
    return split_dicts


def _count_keys_in_json_file(file_path):
    """
    Counts the number of keys in a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        int: The number of keys in the JSON file.
    """
    # Read the JSON file
    with open(file_path, "r") as file:
        # Parse the JSON content into a dictionary
        json_data = json.load(file)
        # Count the number of keys in the dictionary
        num_keys = len(json_data)
    return num_keys


async def _upload_async(new_results_dict, local, entries_per_dict):
    """
    Uploads the given results dictionary to Firebase.

    Args:
        new_results_dict (dict): The dictionary containing the results to be uploaded.
        local (bool): Flag indicating whether the results are stored locally or not.
        entries_per_dict (int): The maximum number of entries per dictionary.

    Returns:
        None
    """
    if local:
        with open("o2cm_results_cache.json", "r") as f:
            new_results_dict = json.load(f)

    split_dicts = _split_dict_by_number(
        new_results_dict, entries_per_dict=entries_per_dict, local=local
    )

    _, db_async = _firebase_auth()
    tasks = []

    for dict_name in split_dicts.keys():

        if local:
            file_path = f"split_jsons/{dict_name}.json"
            num_keys = _count_keys_in_json_file(file_path)
            print(f"Uploaded {dict_name} with {num_keys} keys to Firebase.")

        task = _upload_to_firebase_async(dict_name, split_dicts[dict_name], db_async)

        tasks.append(task)

    await asyncio.gather(*tasks)


def _upload(new_results_dict, local, entries_per_dict):
    """
    Uploads the results dictionary to Firebase.

    Args:
        new_results_dict (dict): The dictionary containing the results to be uploaded.
        local (bool): Flag indicating whether the results are being uploaded from a local file.
        entries_per_dict (int): The maximum number of entries per dictionary.

    Returns:
        None
    """
    if local:
        with open("o2cm_results_cache.json", "r") as f:
            new_results_dict = json.load(f)

    split_dicts = _split_dict_by_number(
        new_results_dict, entries_per_dict=entries_per_dict, local=local
    )

    db, _ = _firebase_auth()
    batch = db.batch()

    for dict_name in split_dicts.keys():

        if local:
            file_path = f"split_jsons/{dict_name}.json"
            num_keys = _count_keys_in_json_file(file_path)
            print(f"Uploaded {dict_name} with {num_keys} keys to Firebase.")

        batch.set(db.collection("results").document(dict_name), split_dicts[dict_name])

    batch.commit()
