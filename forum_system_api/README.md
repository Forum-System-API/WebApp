# Forum System API


## 1. Project description
- Desinged and implemented a Forum System.
- Provided a RESTful API that can be consumed by different clients.
- High-level description:
    - Users can read and create topics and message other users
    - Administrators manage users, topics and categories


## 2. Database - relationships between tables
![database](./database.png)

- User to Category – Many-to-Many: Multiple users can have read access to multiple categories, and each category can be accessed by multiple Users. And only admins can create a Category.
- User to Topic – One-to-many: A User can create multiple Topics, but one Topic is created by one user.
- User to Message – One-to-Many: A User can send multiple messages, but a message can belong to a single User.
- Replies to Users – One-to-Many:  A User can have many replies, but a Reply can belong to only one User.
- Category to Topic – One-to-many: A Category can have many Topics, but a Topic can be part of only one Category.
- Topic to Reply – One-to-many: A Topic can have multiple replies, but a single reply can only belong to one Topic.


## 3. Models
### 3.1. `User`model has the following attributes:
- id &rarr; int
- username &rarr; str
- password &rarr; str
- role &rarr; str

### 3.2. `Message` model has the following attributes:
- message_id &rarr; int 
- text &rarr; str
- timestamp &rarr; datetime
- sender_id &rarr; int
- recipient_id &rarr; int

### 3.3. `Category` model has the following attributes:
- category_id &rarr; int 
- category_name &rarr; str
- is_private &rarr;  int
    - in the schema, related column is is_private where 1 = private, 0 = public
- is_locked &rarr; int
    - in the schema, related column is is_locked where 1 = locked, 0 = unlocked

### 3.4.`Topic` model has the following attributes:
- topic_id &rarr; int 
- title &rarr; str
- date_time &rarr; datetime
- category_id &rarr; int
- user_id &rarr; int
- best_reply_id &rarr; str
- is_locked &rarr; str (allowed values: 'locked' or 'unlocked')
    - in the schema, related column is is_locked where 1 = locked, 0 = unlocked

### 3.5.`Reply` model has the following attributes:
- reply_id &rarr; int 
- text &rarr; str
- date_time &rarr; datetime
- topic_id &rarr; int
- user_id &rarr; int


## 4. Endpoints
### 4.1. User 
- ✔ GET /users: 

    -`GET http://127.0.0.1:8000/users/info`
    recieves the username and the role of the user
- ✔ POST / users
    - `POST http://127.0.0.1:8000/users/register`
    {
    "username": "Mike",
    "password": "1234"
    }
    - `POST http://127.0.0.1:8000/users/login`
    {
    "username": "Mike",
    "password": "1234"
    }

    ADMIN CREDENTIALS
    {
    "username": "admin",
    "password": "blacksheepwall"
    }   
    

### 4.2. Category
- ✔ GET /categories: 
    -`GET http://127.0.0.1:8000/categories`
    responds with a list of categories depending on the role and the privacy status
    -`GET http://127.0.0.1:8000/categories/name/Arts`
    responds the details of the category
    -`GET http://127.0.0.1:8000/categories/id/{category_id`
    responds with the details of the category with id
    -`GET http://127.0.0.1:8000/categories/{category_id}/topics` - requires admin token
    -`GET http://127.0.0.1:8000/categories/privileged/{category_id}` - requires admin token

- ✔ POST /categories:
    - `POST http://127.0.0.1:8000/categories/privacy`
    changes the status of the privacy, requires admin token

    {
	"category_name": "Arts",
	"is_private": 1,
	"is_locked": 0
    }

     -`POST http://127.0.0.1:8000/categories/membership`
    - requires admin token
    {
	"user_id": 8,
	"category_id": 1,
	"can_read": 1,
	"can_write": 1
    }
    - `POST http://127.0.0.1:8000/categories/new`
    {
	"category_name": "Cars",
	"is_private": 1,
	"is_locked":0
    }


- ✔ PUT/categories
    
    - `PUT http://127.0.0.1:8000/categories/privacy`
    changes the status of the privacy, requires admin token

    {
	"category_name": "Arts",
	"is_private": 1,
	"is_locked": 0
    }

    - `PUT http://127.0.0.1:8000/categories/lock`
    requires admin credential

- ✔ DELETE / categories:
    - `DELETE http://127.0.0.1:8000/categories/new`
         requires admin token
    - `DELETE http://127.0.0.1:8000/categories/`
         requires admin token



### 4.3. Message 

### 4.4. Topic
- ✔ GET /topics: ALL GOOD
    - DESCRIPTION: Responds with a list of Topic resources.
    - REQUEST:
        - example: no token added
        - example: token => 7;skankhunt42
        - example: token => 5;Eric
        - `GET http://127.0.0.1:8000/topics`
        - `GET http://127.0.0.1:8000/topics?search=sprint`
        - `GET http://127.0.0.1:8000/topics?sort=asc&sort_by=title`
        - `GET http://127.0.0.1:8000/topics?sort=desc&sort_by=date_time`
        - `GET http://127.0.0.1:8000/topics?search=sprint&sort=asc&sort_by=title`
        - `GET http://127.0.0.1:8000/topics?page=1&topics_per_page=3&search=f1`
    - RESPONSE: See Postman.

- ✔ GET /{topic_id}: 
    - DESCRIPTION: Responds with a single Topic resource and a list of Reply resources if there are any.
    - REQUEST:
        - example: no token added
        - example: token => 7;skankhunt42  `GET http://127.0.0.1:8000/topics/8` 
        - example: token => 5;Eric
        - `GET http://127.0.0.1:8000/topics/3` 
        - `GET http://127.0.0.1:8000/topics/4` 
    - RESPONSE: See Postman.
    
- ✔ POST /topics:
    - DESCRIPTION: Creates a new Topic.
    - REQUEST: `POST http://127.0.0.1:8000/topics` 
        ```json
        example 1: x-token => 3;MoSalah
        {
            "title": "F1 Miami GP Highlights",
            "category_id": 2,
            "is_locked": "unlocked"
        }
        example 2: x-token => 3;MoSalah
        {
            "title": "F1 Miami GP Breaking News",
            "category_id": 2,
            "is_locked": "unlocked"
        }
        example 3: x-token => 7;skankhunt42
        {
            "title": "Hellooooo, art.",
            "category_id": 1,
            "is_locked": "unlocked"
        }
        example 4: x-token => 3;MoSalah
        {
            "title": "Hellooooo, art.",
            "category_id": 1,
            "is_locked": "unlocked"
        }
        ```
    - RESPONSE: See Postman.

- ✔ PUT /{topic_id}: 
    - DESCRIPTION: Updates a Topic resource with a best Reply resource.
    - REQUEST: `PUT http://127.0.0.1:8000/topics/4` -
        ```json
        example 1: x-token => 5;Eric
        {
            "best_reply": "Daniel Ricciardo P4 and points for the RB pilot.",
            "reply_id": "4"
        }
        example 2: x-token => 5;Eric
        {
            "best_reply": "Daniel Ricciardo P4 and points for the RB pilot.",
            "reply_id": "5"
        }
        ```
    - RESPONSE: See Postman.

- ✔ DELETE /topics: 
    - DESCRIPTION: Deletes a Topic resource and all of its Replies.
    - REQUEST: `DELETE http://127.0.0.1:8000/topics/6` x-token => 3;MoSalah
    - RESPONSE: See Postman.

### 4.5. Reply  
- ✔ POST /replies: 
    - DESCRIPTION: Creates a Reply data which is associated with a specific Topic.
    - REQUEST: `POST http://127.0.0.1:8000/replies` 
        ```json
        example: x-token => 3;MoSalah
        {
            "text": "Lando Norris won by a dominant 7.6-second margin.",
            "topic_id": 6
        }
        ```
    - RESPONSE: See Postman.

- ✔ PUT /replies/{id}: 
    - DESCRIPTION: Updates a Reply's text if you are the owner of the Reply.
    - REQUEST: `PUT http://127.0.0.1:8000/replies/7` 
        ```json
        example: x-token => 3;MoSalah
        {
            "text": "Lando Norris won by a dominant 7.6-second margin over Max Verstappen's Redbull.",
            "topic_id": 6
        }
        ```
    - RESPONSE: See Postman.

- ✔ DELETE /replies/{id}: 
    - Description: Deletesa Reply.
    - REQUEST: `DELETE http://127.0.0.1:8000/replies/7` x-token => 3;MoSalah
    - RESPONSE: See Postman.

- ✔ POST /replies/id/{reply_id}/votes: 
    - DESCRIPTION: Updates a Reply's text if you are the owner of the Reply.
    - REQUEST: `POST http://127.0.0.1:8000/replies/id/5/votes` 
        ```json
        example: x-token => 3;MoSalah
        {
            "user_id": 3,
            "reply_id": 5,
            "type_of_vote": "downvote"
        }
        ```
    - RESPONSE: See Postman.

- ✔ PUT /replies/{reply_id}/votes: 
    - DESCRIPTION: Updates a Reply's text if you are the owner of the Reply.
    - REQUEST: `PUT http://127.0.0.1:8000/replies/3/votes` 
        ```json
        example: x-token => 3;MoSalah
        {
            "reply_id": 3,
            "type_of_vote": "downvote"
        }
        ```
    - RESPONSE: See Postman.

- ✔ GET /{reply_id}: 
    - DESCRIPTION: Responds with a single Reply resource.
    - REQUEST:
        - `GET http://127.0.0.1:8000/replies/3`
        - `GET http://127.0.0.1:8000/replies/1` 
    - RESPONSE: See Postman.

## 5. How to Install and Run the Project
- Navigate to /server and open a terminal
- Run `uvicorn main:app`
- Open a browser and type `http://127.0.0.1:8000/docs`. There should be documentation of the available endpoints.