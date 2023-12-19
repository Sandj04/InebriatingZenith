# Database Design

## Main Database (MySQL) Design

The database stores almost all data. It is used for authentication users and admins and stores the cart / order information for each user. It als stores data about available products and their categories.

Furthermore, the credentials and authentication for admins / bartenders are stored in here.

```mermaid
---
title: Main Database (MySQL) Design
---

erDiagram
    USERS {
        int id
        string username
        int code
        int balance
    }
    SESSIONS {
        int id
        int user
        string hashed_token
    }
    USERS }|--|{ SESSIONS : Authentication

    CARTS {
        int id
        int user
        bool payed
        bool ready
        bool delivered
    }
    USERS }|--|{ CARTS : Buying

    CART_ITEMS {
        int id
        int cart
        int item
    }
    CARTS }|--|{ CART_ITEMS : Storage

    PRODUCTS {
        int id
        string name
        string description
        int category
        int price
        string ingredients
        datetime unlock_time
    }
    CART_ITEMS }|--|{ PRODUCTS : Identification

    CATEGORY {
        int id
        string name
        string icon_path
    }
    PRODUCTS }|--|{ CATEGORY : Identification

    USER_TASKS {
        int id
        int task
        int user
        bool completed
    }
    USERS }|--|{ USER_TASKS : Rewards

    TASKS {
        int id
        string description
        int reward
    }
    USER_TASKS }|--|{ TASKS : Identification

    ADMINS {
        int id
        string username
        string hashed_password
    }

    ADMIN_SESSIONS {
        int id
        int admin
        string hashed_token
    }

    ADMINS }|--|{ ADMIN_SESSIONS : Authentication
```
