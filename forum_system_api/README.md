# Forum System API


## 1. Project description
- Desinged and implemented a Forum System.
- Provided a RESTful API that can be consumed by different clients.
- High-level description:
    - Users can read and create topics and message other users
    - Administrators manage users, topics and categories

## 2. Table of contents: describe what you will see during demonstration.


## 3. Database - relationships between tables
![database](./database.png)

- User to Category – Many-to-Many: Multiple users can have read access to multiple categories, and each category can be accessed by multiple Users. And only admins can create a Category.
- User to Topic – One-to-many: A User can create multiple Topics, but one Topic is created by one user.
- User to Message – One-to-Many: A User can send multiple messages, but a message can belong to a single User.
- Replies to Users – One-to-Many:  A User can have many replies, but a Reply can belong to only one User.
- Category to Topic – One-to-many: A Category can have many Topics, but a Topic can be part of only one Category.
- Topic to Reply – One-to-many: A Topic can have multiple replies, but a single reply can only belong to one Topic.


## 4. Models
### 4.1. `User`model has the following attributes:
- id &rarr; int
- username &rarr; str
- password &rarr; str
- role &rarr; str

### 4.2. `Message` model has the following attributes:
- message_id &rarr; int 
- text &rarr; str
- timestamp &rarr; datetime
- sender_id &rarr; int
- recipient_id &rarr; int

### 4.3. `Category` model has the following attributes:
- category_id &rarr; int 
- category_name &rarr; str
- is_private &rarr;  to follow
- is_locked &rarr; to follow

### 4.4.`Topic` model has the following attributes:
- topic_id &rarr; int 
- title &rarr; str
- category_id &rarr; int
- user_id &rarr; int
- date_time &rarr; datetime
- best_reply_id &rarr; to follow
- is_locked &rarr; to follow
- is_private &rarr; to follow

### 4.5.`Reply` model has the following attributes:
- reply_id &rarr; int 
- text &rarr; str
- topic_id &rarr; int
- user_id &rarr; int
- date_time &rarr; datetime

## 5. Endpoints
### 5.1. User 

### 5.2. Category

### 5.3. Message 

### 5.4. Topic
- ✔ GET /topics:
    - DESCRIPTION: Responds with a list of Topic resources.
    - REQUEST: 

        - `GET http://127.0.0.1:8000/topics`

        - `GET http://127.0.0.1:8000/topics?search=sprint`

        - `GET http://127.0.0.1:8000/topics?sort=asc&sort_by=title`

        - `GET http://127.0.0.1:8000/topics?search=sprint&sort=asc&sort_by=title`

    - RESPONSE:
        ```json
        [
            Go to Postman.
        ]
        ```
- ✔ GET /topics/topic_{id}:
    - DESCRIPTION: Responds with a single Topic resource and s list of Reply resources.
    - REQUEST: `GET http://127.0.0.1:8000/topics/1` 
    - RESPONSE:
        ```json
        [
            to follow: example code
        ]
        ```
- ✔ POST /topics:
    - DESCRIPTION: Creates a new Topic.
    - REQUEST: `POST http://127.0.0.1:8000/topics` 
        ```json
        [
            "topic_id": 6,
            "title": "F1 Miami GP Highlights",
            "category_id": 2,
            "user_id": 1,
            "date_time": "2024-05-06T12:50:00"
        ]
        ```
    - RESPONSE:
        ```json
        [
            Go to Postman.
        ]
        ```
- ✔ PUT /{topic_id}/replies:
    - DESCRIPTION: Adds Replies to a specific Topic.
    - REQUEST: `PUT http://127.0.0.1:8000/5/replies` 
        ```json
        [
            to follow
        ]
        ```
    - RESPONSE:
        ```json
        [
            to follow
        ]
        ```
- ✔ DELETE /{topic_id}/replies:
    - DESCRIPTION: Removes Replies from a specific Topic.
    - REQUEST: `DELETE http://127.0.0.1:8000/5/replies` 
        ```json
        [
            to follow
        ]
        ```
    - RESPONSE:
        ```json
        [
            to follow
        ]
        ```
- ✔ DELETE /topics:
    - DESCRIPTION: Deletes a Topic resource and all of its Replies.
    - REQUEST: `DELETE http://127.0.0.1:8000/topics/6` 
    - RESPONSE:
        ```json
        [
            Go to Postman.
        ]
        ```

### 5.5. Reply  
- ✔ POST /replies:
    - DESCRIPTION: Creates a Reply data which is associated with a specific Topic.
    - REQUEST: `POST http://127.0.0.1:8000/replies` 
    - RESPONSE:
        ```json
        [
            "reply_id": 5,
            "text": "Lando Norris won by a dominant 7.6-second margin.",
            "date_time": "2024-05-06T12:50:00",
            "topic_id": 5,
            "user_id": 1
        ]
        ```
- ✔ PUT /replies/{id}:
    - DESCRIPTION: Updates a Reply's text.
    - REQUEST: `POST http://127.0.0.1:8000/replies/5` 
    - RESPONSE:
        ```json
        [
            "reply_id": 5,
            "text": "Lando Norris won by a dominant 7.6-second margin over Max Verstappen's Redbull.",
            "date_time": "2024-05-06T12:52:00",
            "topic_id": 5,
            "user_id": 1
        ]
        ```
- ✔ DELETE /replies/{id}:
    - Description: to follow
    - REQUEST: 
    - RESPONSE:
        ```json
        [
            Go to Postman.
        ]
        ```

## 6. How to Install and Run the Project
- Navigate to /server and open a terminal
- Run `uvicorn main:app`
- Open a browser and type `http://127.0.0.1:8000/docs`. There should be documentation of the available endpoints.


### What to Include in the README:
- Project's Title: ✔ 
- Project Description: **IN PROGRESS**
- Table of Contents (Optional): **IN PROGRESS**
- How to Install and Run the Project: ✔ 
