## Forum System API


### 1. Project description
1.1. Desinged and implemented a Forum System.

1.2. Provided a RESTful API that can be consumed by different clients.

1.3. High-level description:
- Users can read and create topics and message other users
- Administrators manage users, topics and categories


### 2. Database - relationships between tables
![database](./database.png)

- User to Category – Many-to-Many: Multiple users can have read access to multiple categories, and each category can be accessed by multiple Users. And only admins can create a Category.

- User to Topic – One-to-many: A User can create multiple Topics, but one Topic is created by one user.

- User to Message – One-to-Many: A User can send multiple messages, but a message can belong to a single User.

- Replies to Users – One-to-Many:  A User can have many replies, but a Reply can belong to only one User.

- Category to Topic – One-to-many: A Category can have many Topics, but a Topic can be part of only one Category.

- Topic to Reply – One-to-many: A Topic can have multiple replies, but a single reply can only belong to one Topic.


### 3. Models
3.1. `User`: **CHANGES TO FOLLOW** - Vladi 

3.2. `Message`: **CHANGES TO FOLLOW** - Valkata

3.3. `Category`: **CHANGES TO FOLLOW** - Valkata

3.4.`Topic` model has the following attributes:
- id &rarr; int 
- title &rarr; str
- category_id &rarr; int
- user_id &rarr; list of ints

3.5.`Reply` model has the following attributes:
- id &rarr; int 
- text &rarr; str
- upvotes &rarr; int 
- downvotes &rarr; int 
- topic_id &rarr; int
- topic_category_id &rarr; int
- user_id &rarr; int


### 4. Endpoints

4.1. User - Vladi
**CHANGES TO FOLLOW**

4.2. Category - Valkata
**CHANGES TO FOLLOW**
 
4.3. Message - Valkata
**CHANGES TO FOLLOW**

4.4. Topic


**CHANGES TO FOLLOW**


- ✔ GET /topics:
    - It must (View Topics): Responds with a list of Topic resources; Consider adding search, sort and pagination query params.
    - REQUEST: `GET http://127.0.0.1:8000/topics` 
    - RESPONSE:
```json
[
    to follow: example code
]
```
- ✔ GET /topics/{id}:
    - It must (View Topic): Responds with a single Topic resource and a list of Reply resources.
    - REQUEST: `GET http://127.0.0.1:8000/topics/1` 
    - RESPONSE:
```json
[
    to follow: example code
]
```
- ✔ POST /topic:
    - It must (Create Topic): Requires authentication token; Topic data must contain at least a title and a Category.
    - REQUEST: `POST http://127.0.0.1:8000/topics` 
    - RESPONSE:
```json
[
    to follow: example code
]
```

4.5. Reply 


**CHANGES TO FOLLOW**


- ✔ POST /reply:
    - It must (Create Reply ): Requires authentication token; Reply data should contain at least text and is associated with a specific Topic.
    - REQUEST: `POST http://127.0.0.1:8000/replies` 
    - RESPONSE:
```json
[
    to follow: example code
]
```
- ✔ PUT /reply/{id}:
    - It must (Upvote/Downvote a Reply): Requires authentication; A user should be able to change their downvotes to upvotes and vice versa but a reply can only be upvoted/downvoted once per user
    - REQUEST: `POST http://127.0.0.1:8000/replies/1` 
    - RESPONSE:
```json
[
    to follow: example code
]
```
- ✔ PUT /reply/{id}:
    - It must (Choose Best Reply): Requires authentication; Topic Author can select one best reply to their Topic.
    - REQUEST: `POST http://127.0.0.1:8000/replies/1` 
    - RESPONSE:
```json
[
    to follow: example code
]
```


### 5. How to Install and Run the Project
- Navigate to /server and open a terminal
- Run `uvicorn main:app`
- Open a browser and type `http://127.0.0.1:8000/docs`. There should be documentation of the available endpoints.


### What to Include in the README:
- Project's Title: ✔ 
- Project Description: **IN PROGRESS**
- Table of Contents (Optional): **NOT SURE WHAT THIS SHOULD BE**
- How to Install and Run the Project: ✔ 
- How to Use the Project: **NOT SURE WHAT THIS SHOULD BE**
- Include Credit: **NOT SURE WHAT THIS SHOULD BE**
- Add a License: **NOT SURE WHAT THIS SHOULD BE**
- Badges: **NOT SURE WHAT THIS SHOULD BE**