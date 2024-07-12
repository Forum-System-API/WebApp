from services.user_service import find_name_by_id
from data.database import read_query, update_query, insert_query
from data.models.messages import Message
from routers.user import User


def view_all(logged_user: User):
    data = read_query('''SELECT message_id, text, timestamp, sender_id, recipient_id FROM messages
    WHERE recipient_id = ? OR sender_id = ?''', (logged_user.id, logged_user.id))
    formatted_data = [
        {"message_id": row[0], "text": row[1], "timestamp": row[2], "sender_username": find_name_by_id(row[3]),
         "recipient_username": find_name_by_id(row[4])}
        for row in data
    ]
    return formatted_data


def view_conversation(recipient, logged_user: User):
    data = read_query('''SELECT message_id, text, timestamp, sender_id, recipient_id FROM messages
    WHERE recipient_id = ? AND sender_id = ?''', (recipient.id, logged_user.id))
    formatted_data = [
        {"message_id": row[0], "text": row[1], "timestamp": row[2], "sender_id": row[3], "recipient_id": row[4]}
        for row in data
    ]
    return formatted_data


def write_message(message: Message) -> Message | None:
    generated_id = insert_query('''INSERT INTO messages(message_id, text, timestamp, sender_id, recipient_id)
    VALUES(?, ?, ?, ?, ?)''', (
        message.message_id, message.text, message.timestamp, message.sender_id, message.recipient_id))

    message.message_id = generated_id

    return message


def delete_all(user_id: int):
    update_query(f'DELETE FROM messages WHERE messages.sender_id = {user_id}')
