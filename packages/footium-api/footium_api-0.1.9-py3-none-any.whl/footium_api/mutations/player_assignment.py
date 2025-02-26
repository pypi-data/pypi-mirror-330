from typing import List, Tuple
import json
from datetime import datetime, timedelta
from footium_api import GqlConnection
from footium_api.queries import get_server_timestamp

def prepare_assign_players_to_sign(
        gql: GqlConnection, 
        club_id: int,
        player_ids: List[str]
) -> Tuple[dict, dict]:
    current_time = get_server_timestamp(gql)
    current_time_local = datetime.utcnow()
    current_time = current_time / 1000.0
    current_time = datetime.utcfromtimestamp(current_time)
    timeout = 120000
    expiration_time = current_time + timedelta(milliseconds=timeout)
    expiration_iso_string = expiration_time.isoformat(timespec='milliseconds') + 'Z'
    data = {
            "clubId": club_id,
            "playerIds": player_ids,
        }
    message_to_sign = {
        "type": "REGISTER_PLAYERS_TO_CLUB",
        "data": json.dumps(data, separators=(',', ':'), ensure_ascii=False),
        "expirationTime": expiration_iso_string,
    }
    message_to_send = {
        "type": "REGISTER_PLAYERS_TO_CLUB",
        "data": data,
        "expirationTime": expiration_iso_string,
    }
    message_to_send = json.dumps(message_to_send, separators=(',', ':'), ensure_ascii=False)
    return message_to_sign, message_to_send

def prepare_unassign_players_to_sign(
        gql: GqlConnection, 
        club_id: int,
        player_ids: List[str]
) -> Tuple[dict, dict]:
    current_time = get_server_timestamp(gql)
    current_time_local = datetime.utcnow()
    current_time = current_time / 1000.0
    current_time = datetime.utcfromtimestamp(current_time)
    timeout = 120000
    expiration_time = current_time + timedelta(milliseconds=timeout)
    expiration_iso_string = expiration_time.isoformat(timespec='milliseconds') + 'Z'
    data = {
            "clubId": club_id,
            "playerIds": player_ids,
        }
    message_to_sign = {
        "type": "UNREGISTER_PLAYERS_FROM_CLUB",
        "data": json.dumps(data, separators=(',', ':'), ensure_ascii=False),
        "expirationTime": expiration_iso_string,
    }
    message_to_send = {
        "type": "UNREGISTER_PLAYERS_FROM_CLUB",
        "data": data,
        "expirationTime": expiration_iso_string,
    }
    message_to_send = json.dumps(message_to_send, separators=(',', ':'), ensure_ascii=False)
    return message_to_sign, message_to_send

def submit_signed_message(gql: GqlConnection, message, signed_message, address):
    query = """
mutation SubmitAction($action: String!, $signature: String!, $address: String!) {
    submitAction(action: $action, signature: $signature, address: $address)
    {
        code
        error
        message
        __typename
    }
}
"""
    variables = {
        "signature": signed_message,
        "address": address,
        "action": message,
    }
    response = gql.send_mutation(query, variables, "SubmitAction")
    return response
