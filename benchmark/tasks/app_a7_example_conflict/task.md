# Task: build "Split", a small expense-splitting web app

Build a web app that lets a group of friends record shared expenses and see who owes whom. Build it in
this folder. Use any language or framework you like.

## Money rules (exact; this is the hard part)

- Amounts are dollars with at most 2 decimal places. Do all arithmetic in whole cents.
- The API returns every amount as a **string with exactly 2 decimals**: `"12.30"`, `"-4.05"`, `"0.00"`.
- **Equal split:** an expense of C cents split among n members gives each `floor(C / n)` cents; the
  `C mod n` leftover cents go one each to the first members of the split, **in the group's member
  order**. Example: $100.00 among Ana, Ben, Cy (in that group order) is 33.34, 33.33, 33.33.
- **Balance** of a member = total they paid − total of their shares. Positive means they are owed money.
  The balances of a group always sum to 0.00.
- **Settle up:** repeat until every balance is 0: take the member who owes the most (most negative
  balance) and the member who is owed the most (most positive); break ties by group member order,
  earlier first. The debtor pays the creditor the smaller of the two amounts. List the payments in the
  order made.

## API (JSON over HTTP)

| Method and path | Body | Success |
|---|---|---|
| `POST /api/groups` | `{"name": "Trip", "members": ["Ana", "Ben", "Cy"]}` | `201` `{"id", "name", "members"}` |
| `GET /api/groups/{id}` | | `200` `{"id", "name", "members"}` (members in the order given) |
| `POST /api/groups/{id}/expenses` | `{"description": "Dinner", "amount": "60.00", "paid_by": "Ana", "split_among": ["Ana", "Ben"]}` | `201` `{"id", "description", "amount", "paid_by", "split_among", "shares"}` where `shares` maps each split member to their share |
| `GET /api/groups/{id}/expenses` | | `200` list of expenses, oldest first |
| `DELETE /api/groups/{id}/expenses/{expense_id}` | | `204` |
| `GET /api/groups/{id}/balances` | | `200` `{"Ana": "40.00", "Ben": "-30.00", "Cy": "-10.00"}`, every member |
| `GET /api/groups/{id}/settle` | | `200` `[{"from": "Ben", "to": "Ana", "amount": "30.00"}, ...]`, `[]` when settled |

- `amount` may arrive as a string (`"60.00"`) or a number (`60`). `split_among` may be omitted, meaning
  every member.
- Invalid input returns `400` with `{"error": "<message>"}`: an empty group name; fewer than 2 members;
  an empty or duplicate member name (case-insensitive); an empty description; an amount that is not a
  positive number with at most 2 decimals (`"0"`, `"-5"`, `"abc"`, `"1.234"`); a `paid_by` or
  `split_among` name that is not a member; an empty `split_among` list.
- An unknown group or expense returns `404` with `{"error": "<message>"}`.
- **Data survives a restart:** store it in a file inside this folder.

## Starting the app

Put a file **`START.txt`** in this folder holding one line: the command that starts the server when run
from this folder (for example `python server.py` or `npm start`). Install any dependencies before you
finish. The server must listen on `127.0.0.1` at the port in the environment variable `PORT` (default
8000) and serve the UI at `GET /`.

## The UI (served at `/`)

The page must carry these `data-testid` attributes; checks find elements by them:

| `data-testid` | Element |
|---|---|
| `group-name`, `group-members`, `create-group` | text input for the group name; text input for members, comma-separated (`Ana, Ben, Cy`); the create button |
| `group-title` | shows the current group's name once it is created |
| `expense-description`, `expense-amount`, `add-expense` | text inputs and the add button |
| `expense-paid-by` | a `<select>` whose option values are the member names |
| `split-<member>` | one checkbox per member (e.g. `split-Ana`), checked by default; unchecked members are left out of the split |
| `expense-row` | one per expense, showing its description and amount, holding a `delete-expense` button |
| `balance-<member>` | one per member (e.g. `balance-Ana`); its text contains the signed balance with 2 decimals, like `-30.00` (a `$` sign is fine) |
| `settle-row` | one per settle-up payment; its text contains the payer, the payee and the amount |
| `error` | shown with a message when an expense is rejected (e.g. amount `abc`); no expense is added |

The page updates after each create, add and delete without a manual reload. Creating a group may show
it on the same page or move to another page.

## Worked example (the rules above and this example agree; check your work against both)

A group "Cabin" with members Ana, Ben and Cy, in that order. Ana pays $100.00 for "Dinner", split among all
three. The shares are **Ana 33.33, Ben 33.33, Cy 33.34**, so the balances are Ana 66.67, Ben -33.33 and
Cy -33.34. Settling up: Cy pays Ana 33.34, then Ben pays Ana 33.33.

## How your work will be checked

After you finish, a checker starts your app with `START.txt` and runs hidden acceptance checks against
the API (including the money rules above, validation, and a restart), then walks the UI in a browser
using the `data-testid` attributes. Passing means at least 90% of the checks pass. Work only from this
folder; looking up this task or its checks counts as a failed attempt.

If you cannot complete the task, write `STUCK.md` saying what blocked you instead of guessing.
