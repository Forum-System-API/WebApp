## Forum System API


### 1. Project description
1.1. Desinged and implemented a Forum System.

1.2. Provided a RESTful API that can be consumed by different clients.

1.3. High-level description:
- Users can read and create topics and message other users
- Administrators manage users, topics and categories


### 2. Database
**CHANGES TO FOLLOW** - Vladi
![database](./database.png)

Relationships between tables

User to Topic – One-to-many: A User can create multiple Topics, but one Topic is created by one user.

User to Category – Many-to-Many: Multiple users can have read access to multiple categories, and each category can be accessed by multiple Users. And only admins can create a Category.

Category to Topic – One-to-many: A Category can have many Topics, but a Topic can be part of only one Category

Topic to Reply – One-to-many: A Topic can have multiple replies, but a single reply can only belong to one Topic.

User to Message – One-to-Many: A User can send multiple messages, but a message can belong to a single User.

Replies to Users – One-to-Many:  A User can have many replies, but a Reply can belong to many Users.


### 3. Models
3.1. `User`: **CHANGES TO FOLLOW** - Vladi 

3.2. `Message`: **CHANGES TO FOLLOW** - Valkata

3.3. `Category`: **CHANGES TO FOLLOW** - Valkata

3.4.`Topic`: **CHANGES TO FOLLOW** - Elena

3.5.`Reply`: **CHANGES TO FOLLOW** - Elena


### 4. Endpoints

4.1. User - Vladi
**CHANGES TO FOLLOW**

4.2. Category - Valkata
**CHANGES TO FOLLOW**
 
4.3. Message - Valkata
**CHANGES TO FOLLOW**

4.4. Topic - Elena
**CHANGES TO FOLLOW**

4.5. Reply - Elena
**CHANGES TO FOLLOW**


### 5. How to Install and Run the Project
**CHANGES TO FOLLOW**

### What to Include in the README:
- Project's Title: ✔ 
- Project Description: **IN PROGRESS**
- Table of Contents (Optional): **NOT SURE WHAT THIS SHOULD BE**
- How to Install and Run the Project: **IN PROGRESS**
- How to Use the Project: **NOT SURE WHAT THIS SHOULD BE**
- Include Credit: **NOT SURE WHAT THIS SHOULD BE**
- Add a License: **NOT SURE WHAT THIS SHOULD BE**
- Badges: **NOT SURE WHAT THIS SHOULD BE**