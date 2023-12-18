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
    USERS ||--|{ SESSIONS : Authentication
```
