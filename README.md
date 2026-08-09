# Mini_Bot

A Bale Messenger bot built with Flask and SQLAlchemy. The project is designed to collect user reports and experiences and, in a later stage, use useful experiences as a knowledge source for an LLM + RAG system.

## Project Goals

Users can:

- Chat with the bot and an LLM.
- Submit reports.
- View their latest report.
- View their report count.
- Use a user panel.
- Later contribute useful experiences to a searchable knowledge base for RAG.

The project intentionally keeps responsibilities separated:

- `core/logic.py` handles decisions, routing, commands, and state transitions.
- `handlers/message.py` handles outgoing messages and inline keyboards.
- `handlers/rag/report.py` handles the report Wizard.
- `handlers/rag/chat.py` handles LLM conversations.
- `database/crud.py` handles database operations.
- `database/models.py` defines SQLAlchemy models.

---

## Project Structure

```text
Mini_Bot/
├── app.py
├── config.py
│
├── core/
│   ├── constants.py
│   ├── enums.py
│   ├── __init__.py
│   ├── logic.py
│   └── validates.py
│
├── database/
│   ├── crud.py
│   ├── db.py
│   ├── __init__.py
│   ├── models.py
│   └── RAG.db
│
├── handlers/
│   ├── __init__.py
│   ├── message.py
│   └── rag/
│       ├── chat.py
│       └── report.py
│
├── utils/
│   ├── __init__.py
│   ├── send_message.py
│   └── Set_Webhook.py
│
├── scripts/
│   └── run.sh
│
├── test/
│   ├── __init__.py
│   └── test_report.py
│
├── runtime/
│   ├── tunnel.log
│   └── tunnel_url.txt
│
├── requirements.txt
└── README.md
```

`__pycache__` directories are generated Python bytecode and are not part of the application architecture.

---

## Architecture

The main message flow is:

```text
Bale
  │
  ▼
app.py
  │
  ▼
core/logic.py
  │
  ├── Command handling
  ├── State handling
  ├── Chat mode
  └── Report Wizard
       │
       ▼
handlers/rag/report.py
       │
       ▼
database/crud.py
       │
       ▼
database/RAG.db
```

---

## State Machine

The current state of a user is stored in `User.current_state`.

Main states:

```text
NORMAL
CHAT

REPORT_TITLE
REPORT_CATEGORY
REPORT_PRIORITY
REPORT_DESCRIPTION
```

The report flow is:

```text
NORMAL
  │
  │ /Report
  ▼
REPORT_TITLE
  │
  │ title
  ▼
REPORT_CATEGORY
  │
  │ category
  ▼
REPORT_PRIORITY
  │
  │ priority
  ▼
REPORT_DESCRIPTION
  │
  │ description
  ▼
NORMAL
```

`/Report` starts the report Wizard.

After that, normal user messages are interpreted according to the current report state.

---

## `core/logic.py`

`logic.py` is the decision-making and routing layer.

It decides:

1. Whether a message is a command.
2. Whether the user is in Chat Mode.
3. Whether the user is in a report state.
4. Which handler should process the message.
5. Which `next_state` should be applied after the Wizard returns.
6. When the database transaction should be committed.

Conceptually:

```text
Message
   │
   ▼
logic.py
   │
   ├── /Start
   ├── /Help
   ├── /About
   ├── /UserPanel
   ├── /ChatMode
   ├── /Report
   └── Report State
          │
          ▼
    process_report_step()
```

The Wizard does not commit the database transaction itself.

`logic.py` is responsible for applying `StepResult.next_state` and committing the change.

---

## `handlers/rag/report.py`

This file contains the report Wizard.

The Wizard receives the current user state and the user's text.

It updates the current `ReportDraft` and returns a `StepResult`.

For example:

```python
StepResult(
    message="Enter the report category:",
    next_state=UserState.REPORT_CATEGORY,
    finished=False
)
```

The Wizard does not call `commit()`.

Its responsibility is:

```text
Current state
      │
      ▼
process_report_step()
      │
      ├── update Draft
      │
      └── return StepResult
```

---

## `StepResult`

`StepResult` represents the result of one Wizard step.

It contains:

```text
StepResult
├── message
├── next_state
└── finished
```

Example:

```python
StepResult(
    message="Enter the report priority:",
    next_state=UserState.REPORT_PRIORITY,
    finished=False
)
```

This means:

- The next message should ask for the report priority.
- The user's next state is `REPORT_PRIORITY`.
- The Wizard is not finished yet.

---

## `ReportDraft`

A report is incomplete while the user is going through the Wizard.

For this reason, the project uses `ReportDraft`.

The flow is:

```text
/Report
   │
   ▼
Create ReportDraft
   │
   ├── title
   ├── category
   ├── priority
   └── description
```

Each Wizard step fills another field of the same Draft.

Example:

```text
Draft

title       = "Pump failure"
category    = "Breakdown"
priority    = "HIGH"
description = "Pump number 2 stopped during operation."
```

After the Wizard finishes, the Draft can be used to create the final `Report`.

---

## Reports and Experiences

The long-term purpose of the project is not only storing reports.

The project is intended to build a collection of real-world reports and experiences that can later be used by an LLM + RAG system.

The current approach intentionally keeps this simple:

```text
Report
  │
  └── can become a source for an Experience
```

A report does not have to be the same thing as an experience.

A useful experience can later be extracted from one or more reports.

This avoids making the first version of the project unnecessarily complicated.

---

## Database

The project uses SQLite with SQLAlchemy.

Database file:

```text
database/RAG.db
```

SQLAlchemy models:

```text
database/models.py
```

Database operations:

```text
database/crud.py
```

### User

The `User` model currently stores:

```text
User
├── id
├── bale_user_id
├── first_name
├── report_count
└── current_state
```

`current_state` is persisted in the database so the bot knows which step the user is currently in.

### Report

The `Report` model stores completed reports:

```text
Report
├── id
├── user_id
├── title
├── description
├── priority
├── category
└── created_at
```

`Report.user_id` is a foreign key pointing to `User.id`.

SQLAlchemy `relationship()` is used for object-level navigation between related models.

---

## `database/crud.py`

CRUD stands for:

```text
Create
Read
Update
Delete
```

This layer contains database operations such as:

```text
get_or_save_user()
get_report_draft()
get_last_report()
save_report()
```

The purpose is to keep SQL/database operations out of the main application logic whenever practical.

---

## `handlers/message.py`

This file is responsible for outgoing messages and the user interface.

Examples:

```text
send_start_menu()
send_user_panel()
send_help()
send_about()
send_report_count()
send_last_report()
```

It also creates inline keyboards.

This layer should not decide what the user's state means.

That decision belongs to:

```text
core/logic.py
```

---

## LLM Chat

The LLM chat functionality is located in:

```text
handlers/rag/chat.py
```

The basic flow is:

```text
User
 ↓
/ChatMode
 ↓
UserState.CHAT
 ↓
User message
 ↓
ask_llm()
 ↓
LLM response
 ↓
Bale
```

---

## RAG Roadmap

The current SQLite database is the source of application data.

RAG will not simply send the entire SQLite database to the LLM on every request.

The future architecture is approximately:

```text
Report / Experience
        │
        ▼
Clean / Prepare
        │
        ▼
Chunk
        │
        ▼
Embedding
        │
        ▼
Vector Database
        │
        ▼
Similarity Search
        │
        ▼
Relevant Experiences
        │
        ▼
LLM
```

A vector database does not need to be added yet.

The current priority is:

1. Make report submission reliable.
2. Make `ReportDraft` reliable.
3. Make the State Machine reliable.
4. Write unit tests.
5. Collect useful real-world data.
6. Then implement embeddings and RAG.

---

## Testing

Tests are located in:

```text
test/
```

The current report test is:

```text
test/test_report.py
```

The Wizard tests should verify the complete state flow:

```text
REPORT_TITLE
    ↓
REPORT_CATEGORY
    ↓
REPORT_PRIORITY
    ↓
REPORT_DESCRIPTION
    ↓
NORMAL
```

They should also verify that every user's input is stored in the correct `ReportDraft` field.

Run all tests:

```bash
python3 -m pytest
```

Run only the report tests:

```bash
python3 -m pytest test/test_report.py
```

---

## Running the Project

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Run the Flask application:

```bash
python3 app.py
```

Or use the project script:

```bash
bash scripts/run.sh
```

---

## Webhook and Tunnel

Runtime tunnel information is stored in:

```text
runtime/
```

Current tunnel URL:

```text
runtime/tunnel_url.txt
```

Tunnel log:

```text
runtime/tunnel.log
```

The `scripts/run.sh` script can use `runtime/tunnel_url.txt` to obtain the current tunnel URL.

---

## Development Principles

### 1. `logic.py` makes decisions

```text
core/logic.py
```

is the central routing and decision-making layer.

### 2. The Wizard handles report steps

```text
handlers/rag/report.py
```

The Wizard updates the Draft and returns a `StepResult`.

It does not commit the transaction.

### 3. CRUD handles database operations

```text
database/crud.py
```

### 4. Message handlers handle UI

```text
handlers/message.py
```

### 5. State is persisted in the User

```text
User.current_state
```

The next state is returned by:

```text
StepResult.next_state
```

and applied by `logic.py`.

### 6. Keep the architecture stable

The current project structure should not be changed without a clear technical reason.

The goal is to learn the architecture while building the project, rather than repeatedly replacing it with a different architecture.

---

## Current Project Status

Currently implemented or in progress:

- Flask webhook
- Bale Bot
- SQLite
- SQLAlchemy
- User model
- Report model
- ReportDraft
- UserState
- Command handling
- Report Wizard
- LLM chat
- CRUD layer
- Unit tests

Future roadmap:

```text
Reports
   ↓
Experience extraction
   ↓
Embedding
   ↓
Vector Search
   ↓
RAG
   ↓
LLM
```

The final goal is to build a searchable network of real-world experiences and failures so that the LLM can use relevant previous experiences when answering future questions.
