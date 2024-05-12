from data.database import insert_query, read_query, update_query
from data.models import Reply, User, ReplyUpdate, Vote, VoteTypes
from common.responses import BadRequest
from datetime import datetime


def create(reply: Reply, user: User):
    generated_id = insert_query(
        '''INSERT INTO replies(reply_id, text, date_time, topic_id, user_id) 
               VALUES(?,?,?,?,?)''',
        (reply.reply_id, reply.text, reply.date_time, reply.topic_id, user.id))

    reply.reply_id = generated_id

    return reply


def get_by_id(reply_id: int):
    data = read_query(
        '''SELECT reply_id, text, date_time, topic_id, user_id 
            FROM replies WHERE reply_id = ?''', 
        (reply_id,))

    return next((Reply.from_query_result(*row) for row in data), None)


def reply_id_exists(reply_id: int):
    return any(
        read_query(
                '''SELECT reply_id, text, date_time, topic_id, user_id 
                       FROM replies WHERE reply_id = ?''',
                (reply_id,)))


def create_vote(reply_id: int, vote: Vote):
    new_vote = insert_query(
        ''' INSERT INTO votes (user_id, reply_id, type_of_vote) 
                VALUES (?, ?, ?)''',
        (vote.user_id, reply_id, vote.type_of_vote))
    
    values = (vote.user_id, reply_id, vote.type_of_vote)

    return vote
 

def get_by_id_with_votes(reply_id: int):
    reply_data = read_query(
        '''SELECT reply_id, text, date_time, topic_id, user_id 
               FROM replies WHERE reply_id = ?''',
        (reply_id,))

    votes_data = read_query(
        '''SELECT type_of_vote, COUNT(*) 
               FROM votes WHERE reply_id = ? GROUP BY type_of_vote''',
        (reply_id,))

    reply_result = next((Reply.from_query_result(*row) for row in reply_data), None)

    if reply_result is None:
        return f'No reply found with id {reply_id}'

    if not votes_data:
        return {
            'reply': reply_result,
            'votes': {
                'upvote': 0,
                'downvote': 0
            }
        }

    vote_count = {VoteTypes.INT_TO_STR[vote_type]: count for vote_type, count in votes_data}

    return {
        'reply': reply_result,
        'votes': vote_count
    }


def update(reply_update: ReplyUpdate, reply: Reply):
    result = update_query('''UPDATE replies SET text = ? 
                                 WHERE reply_id = ?''',
        (reply_update.text, reply.reply_id))

    if result:
        reply.text= reply_update.text
        return reply
    else:
        return None


def get_by_topic(topic_id: int):
    data = read_query(
        '''SELECT reply_id, text, date_time, topic_id, user_id 
               FROM replies WHERE topic_id = ?''',
        (topic_id,))
    
    replies_data = []
    for row in data:
        reply = Reply.from_query_result(*row)
        reply.date_time = reply.date_time.strftime('%Y/%m/%d %H:%M')
        replies_data.append(reply)

    return replies_data


def delete(reply: Reply):
    update_query('''DELETE 
                        FROM replies WHERE reply_id = ?''', 
                 (reply.reply_id,))
    
    
def get_vote(vote: Vote):
    vote.type_of_vote = VoteTypes.STR_TO_INT[vote.type_of_vote]
    result = read_query(
        '''SELECT type_of_vote 
               FROM votes WHERE reply_id = ?''',
        (vote.reply_id,))
    
    return result


def update_reply_vote(existing_vote: int, reply_id: int, vote: Vote):
    existing_vote_str = VoteTypes.INT_TO_STR[existing_vote]
    existing_vote_result = read_query(
        '''SELECT type_of_vote 
               FROM votes WHERE reply_id = ?''',
        (reply_id,))
    
    if existing_vote_result:
        existing_vote_str_fordb = VoteTypes.INT_TO_STR[existing_vote_result[0][0]]
        if existing_vote_str_fordb == existing_vote_str:
            return BadRequest(content='You have already voted.') 
        update_query(
            '''UPDATE votes 
                   SET type_of_vote = ? WHERE reply_id = ?''',
            (vote.type_of_vote, vote.reply_id))
        
        return vote.type_of_vote
    else:
        insert_query(
            '''INSERT INTO votes (reply_id, type_of_vote, user_id) 
                   VALUES (?,?,?)''',
            (vote.reply_id, vote.type_of_vote, vote.user_id))
        
        return vote.type_of_vote


def is_locked(topic_id: int):
    data = read_query(f'''SELECT topic_id, title
                            FROM topics
                            WHERE is_locked = 1 AND topic_id = {topic_id}''')
    
    return len(data) > 0


def has_access(category_id: int, user: User):
    data = read_query(f'''SELECT DISTINCT c.category_id
                    FROM categories c
                    JOIN categories_access ca ON  c.category_id = ca.category_id
                    JOIN users u ON u.user_id = ca.user_id
                    WHERE c.is_private = 1 AND ca.can_write = 1 AND u.user_id = {user.id} AND c.category_id = {category_id}
                    UNION ALL 
                    SELECT DISTINCT c.category_id
                    FROM categories c
                    WHERE c.is_private = 0 AND c.is_locked = 0 AND c.category_id = {category_id}''')
    
    return len(data) > 0