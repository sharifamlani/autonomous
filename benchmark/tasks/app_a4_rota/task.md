# Task: build "Rota", a shift-scheduling web app

Build a web app that a small hospital ward uses to schedule staff onto shifts. Build it in this folder. Use any
language or framework you like. Every rule below is exact; the hidden checks test each one.

## People

- `POST /api/people` with `{"name": "Ana", "role": "nurse", "max_hours": 40, "unavailable": ["sat", "sun"]}`
  returns `201` with `{"id", "name", "role", "max_hours", "unavailable", "version": 1}`.
  - `role` is one of `nurse`, `doctor`, `porter`. `max_hours` is a whole number from 1 to 60. `unavailable` is a
    list of day codes from `mon tue wed thu fri sat sun` (may be empty or omitted; returned in that day order,
    without duplicates). Names are non-empty and unique, ignoring case.
- `GET /api/people` returns every person, sorted by name ignoring case.
- `PUT /api/people/{id}` replaces name, role, max_hours and unavailable. It requires the header
  `If-Match: <version>`: missing returns `428`; a version that is not the current one returns `409`; success
  returns `200` with `version` increased by 1. The same validation as create applies. Changing a person does
  not touch their existing assignments.
- `DELETE /api/people/{id}` returns `204` and removes that person's assignments.
- `POST /api/people/import` with a CSV body (`Content-Type: text/csv`):
  ```
  name,role,max_hours,unavailable
  Ben,doctor,24,mon;tue
  Cy,porter,30,
  ```
  Valid rows are created; invalid rows are skipped. Returns `200` with `{"created": <count>, "errors":
  [{"line": <n>, "error": "<message>"}]}`, where the header is line 1. A row is invalid for any reason a create
  would be rejected, including a name already used (by an existing person or an earlier row).

## Shifts

- `POST /api/shifts` with `{"date": "2026-03-02", "start": "22:00", "end": "06:00", "role": "nurse", "slots": 2}`
  returns `201` with `{"id", "date", "start", "end", "role", "slots", "hours", "assigned": []}`.
  - Times are `HH:MM` on the hour or half hour. If `end` is not after `start`, the shift ends the next day
    (`22:00`-`06:00` is 8 hours). A shift lasts from 1 to 12 hours. `hours` is a number (`8`, `7.5`).
    `slots` is a whole number from 1 to 5. `assigned` lists the assigned person ids in the order assigned.
- `GET /api/shifts?from=2026-03-02&to=2026-03-08&role=nurse&page=1&per_page=20` returns
  `{"items": [...], "page", "per_page", "total"}`: shifts whose date is within `from`..`to` inclusive (each
  filter optional), ordered by date, then start time, then id. `per_page` defaults to 20; a value above 100 is
  treated as 100. `page` starts at 1. `total` counts all matches, not just this page.

## Assigning people to shifts

`POST /api/shifts/{id}/assign` with `{"person_id": ...}` returns `200` and the updated shift. The rules are
checked **in this order**; the first one broken returns `409` with `{"error": "<message>", "rule": "<code>"}`:

| Order | `rule` | Broken when |
|---|---|---|
| 1 | `role` | the person's role is not the shift's role |
| 2 | `full` | every slot is already taken |
| 3 | `duplicate` | the person is already on this shift |
| 4 | `unavailable` | the weekday of the shift's **start date** is in the person's `unavailable` list |
| 5 | `overlap` | the shift's time overlaps another shift the person is on (touching end-to-start is not an overlap) |
| 6 | `rest` | fewer than 10 hours between the end of one of the person's shifts and the start of this one, or between the end of this one and the start of another of theirs |
| 7 | `hours` | the person's hours in the week of the shift's start date (weeks run Monday to Sunday; a shift's hours all count in the week of its start date) would exceed `max_hours` |

`DELETE /api/shifts/{id}/assign/{person_id}` removes the assignment and returns `204`.

## Auto-fill

`POST /api/autofill` with `{"from": "2026-03-02", "to": "2026-03-08"}` fills open slots on shifts dated in that
range. Shifts are taken in order (date, start, id). For each open slot, the person chosen is, among everyone who
breaks none of the 7 rules for that shift, the one with the **fewest hours already assigned in that shift's
week**, ties broken by name ignoring case. Slots no one can fill stay open. Returns `200` with
`{"assigned": [{"shift_id", "person_id"}, ...], "unfilled": [{"shift_id", "open": <n>}, ...]}`, both in the
order the shifts were taken.

## Undo and audit

- Every change is an action: `person.create`, `person.update`, `person.delete`, `person.import`,
  `shift.create`, `assign`, `unassign`, `autofill` (one action, however many slots it filled).
- `POST /api/undo` reverts the most recent action not yet undone (up to the last 20 actions) and returns `200`
  with `{"undone": "<action>"}`. With nothing to undo it returns `409` with `"rule": "nothing_to_undo"`.
  Undoing a `person.update` restores the old fields and the version number advances by 1.
- `GET /api/audit` returns `[{"seq": 1, "action": "person.create", "detail": "..."}, ...]`, oldest first, one
  entry per action and one per undo (`"action": "undo"`). `seq` counts from 1.

## Export

`GET /api/export.csv?from=2026-03-02&to=2026-03-08` returns `text/csv`, exactly:

```
date,start,end,role,person
2026-03-02,07:00,15:00,nurse,Ana
2026-03-02,07:00,15:00,nurse,OPEN
```

One row per filled slot (the person's name) and one per open slot (`OPEN`), ordered by date, start, shift id,
then filled slots by name ignoring case before open slots. Lines end with `\n`.

## Errors and storage

- Invalid input returns `400` with `{"error": "<message>"}`; an unknown person or shift returns `404` with
  `{"error": "<message>"}`.
- **Everything survives a restart** (people, shifts, assignments, versions, the audit log and the undo
  history): store it in a file inside this folder.
- **Leave an empty store.** The checker starts your app from this folder exactly as you leave it and expects no
  people, shifts or history yet: before you finish, delete any data your own testing created.

## Starting the app

Put a file **`START.txt`** in this folder holding one line: the command that starts the server when run from
this folder (for example `python server.py` or `npm start`). Install any dependencies before you finish. The
server must listen on `127.0.0.1` at the port in the environment variable `PORT` (default 8000) and serve the
UI at `GET /`.

## The UI (served at `/`)

The page must carry these `data-testid` attributes; checks find elements by them:

| `data-testid` | Element |
|---|---|
| `person-name`, `person-role`, `person-max`, `add-person` | text input; `<select>` of the three roles; number input; add button |
| `person-unavailable-<day>` | one checkbox per day code (e.g. `person-unavailable-sat`), unchecked by default |
| `person-row` | one per person, its text containing the name and role |
| `shift-date`, `shift-start`, `shift-end`, `shift-role`, `shift-slots`, `add-shift` | the shift form (`shift-role` is a `<select>`) |
| `week-start` | a date input; the page shows the Monday-to-Sunday week containing that date |
| `shift-card` | one per shift in the shown week, in shift order; its text contains the date (as `2026-03-02`), start and end |
| `assigned-name` | inside a `shift-card`, one per assigned person, the person's name |
| `assign-select`, `assign-button` | inside a `shift-card`: a `<select>` whose option values are person ids, and its button |
| `hours-<name>` | one per person (e.g. `hours-Ana`), its text containing their hours in the shown week (`8`, `7.5`) |
| `autofill-button` | auto-fills the shown week |
| `undo-button` | undoes the last action |
| `error` | shown with the message when an assignment is refused (it must contain the `rule` code) |

The page updates after every change without a manual reload.

## How your work will be checked

After you finish, a checker starts your app with `START.txt` and runs hidden acceptance checks: every rule
above through the API (including overnight shifts, the rule order, auto-fill choices, undo, CSV import and
export, pagination and a restart), then walks the UI in a browser using the `data-testid` attributes. Passing
means at least 90% of the checks pass. Work only from this folder; looking up this task or its checks counts as
a failed attempt.

If you cannot complete the task, write `STUCK.md` saying what blocked you instead of guessing.
