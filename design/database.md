# Database Design

## Main Database (MySQL) Design

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
        string token
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
        bool unlocked
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
```
