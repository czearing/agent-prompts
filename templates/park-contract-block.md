## Parking work

Moving an issue to `blocked` is a claim that something will move it back. Name that something on the
same write, or do not park the issue. A park with nothing named is an abandonment, and every issue
waiting on it is abandoned with it.

- One request does it. `PATCH /api/issues/{id}` carries `status: "blocked"`, a wake path, and
  `unblockDescriptor` together. Both fields are already on the endpoint. A follow up write does not
  count, because the walk that scores the board can read the row between the two.
- A wake path is at least one id in `blockedByIssueIds`, or a monitor scheduled on the same write so
  `monitorNextCheckAt` reads back non-null. Nothing else counts. An empty `blockedByIssueIds`, a
  descriptor on its own, a comment, a plan, and an intention to check back later are all not wake paths.
  The ids are the `id` field of the blocking issue record, not its display identifier, so send
  `["48436021-0255-41dc-a733-93b920aa939e"]` and not `["OFF-70"]`.
- `unblockDescriptor` is `{ "owner": { "agentId": "<your-own-id>" } | { "userId": "<id>" } | "board",
  "action": "<what the owner does to move this>" }`. Both parts are required, and the action must be
  specific enough to act on without reading the thread. The descriptor never replaces the wake path.
- Read `owner` as accountability, not as the hand that does the work. It names the party who is on the
  hook for this park and who answers for it if the park goes stale. It does not name the party who
  performs the act that clears the blocker. The field name reads the other way, so decide it from this
  sentence and not from the name.
- The owner is you, a person, or the board. The endpoint refuses a descriptor that names another agent,
  and answers `Agents may only name themselves as an unblock owner`, which is the same rule stated by
  the API: you cannot make another agent accountable for your park.
- When the act belongs to someone else, split it. The blocker edge carries the dependency, the owner is
  you, and the `action` names both the other party and what you do once they are finished, in that
  order. Write `Waiting on Tooling to land the queue write path on OFF-70; re-run the collector against
  it and unpark or re-park with the reason.` Do not write `Tooling lands the queue write path.`, which
  records a party who cannot be the owner and leaves no act attached to anyone who can.
- With nothing to wait on yet, make the thing to wait on. File it with
  `POST /api/companies/{companyId}/issues`, carrying the decision, the question, or the work you need in
  a description that stands on its own, with `parentId` and `goalId` set from your issue and
  `assigneeAgentId` or `assigneeUserId` set to whoever must act. When only the board can answer, leave
  it unassigned and set the descriptor owner to `"board"`. Leave it in `todo`. Then park on it as a
  blocker. That issue reaching a terminal status is what wakes you.
- Prefer the blocker edge. A blocker wakes you the moment it closes, so filing the issue and parking on
  it is the default even when filing it is the extra step.
- Use a monitor as the wake path only when you are waiting on a clock or an outside service that no
  issue models. Schedule it on the same write through `executionPolicy.monitor` and confirm
  `monitorNextCheckAt` reads back non-null. Set `kind` to a short label naming what you are waiting on,
  `nextCheckAt` to the first moment the answer could have changed, `timeoutAt` to the moment you would
  stop waiting and escalate instead, and `maxAttempts` to the number of checks that fit between them.
  With no better numbers, check in an hour, time out in a day, and cap attempts at twelve.
- Running out of a heartbeat is not a blocker. Leave the issue `in_progress` only when a real
  continuation will pick it up. If nothing will, file the follow up that carries the rest of the work,
  park on it, and record yourself as the owner with what you do when it closes.
- Confirm the write. The response echoes `status`, `blockedByIssueIds`, `monitorNextCheckAt`, and
  `unblockDescriptor`. An empty body means the park did not land and the issue is still yours this
  heartbeat.

Parked on another issue:

```json
PATCH /api/issues/{id}
{
  "status": "blocked",
  "blockedByIssueIds": ["<blocking-issue-id>"],
  "unblockDescriptor": {
    "owner": { "agentId": "<your-own-agent-id>" },
    "action": "Waiting on the queue write path to land on the blocking issue; re-run the collector against it and unpark or re-park with the reason."
  },
  "comment": "Parked on the queue write path. Wake path and owner recorded on the same write."
}
```

Parked on a board decision, after filing the issue that carries the decision:

```json
PATCH /api/issues/{id}
{
  "status": "blocked",
  "blockedByIssueIds": ["<decision-issue-id>"],
  "unblockDescriptor": {
    "owner": "board",
    "action": "Decide on the decision issue whether the budget covers a second run."
  },
  "comment": "Parked on the decision issue. The board owns it and this wakes when it closes."
}
```

Parked on a clock or an outside service:

```json
PATCH /api/issues/{id}
{
  "status": "blocked",
  "executionPolicy": {
    "monitor": {
      "kind": "external_check",
      "nextCheckAt": "2026-09-03T04:00:00Z",
      "timeoutAt": "2026-09-04T04:00:00Z",
      "maxAttempts": 12
    }
  },
  "unblockDescriptor": {
    "owner": { "agentId": "<your-own-agent-id>" },
    "action": "Re-read the external pipeline result when the monitor fires, then unpark or re-park with the reason."
  },
  "comment": "Parked on the external pipeline. Monitor scheduled on the same write."
}
```

- Never write `status: "blocked"` without a wake path and an `unblockDescriptor` in the same request.
- Never treat an `unblockDescriptor` on its own as a wake path. A park with neither a blocker nor a
  scheduled monitor is counted as a dead end no matter how good the descriptor reads.
- Never record the unblock owner or the action only in a comment.
- Never name another agent as the unblock owner. The endpoint refuses it, and the park is yours to
  chase.
- Never read `owner` as the party who performs the unblocking act, and never leave the acting party out
  of the `action` text when it is not you.
- Never point `blockedByIssueIds` at an issue that is not what you are waiting for, and never file a
  placeholder issue whose only purpose is to make the write pass.
- Never avoid `blocked` to sidestep this. Parking correctly is cheaper than sitting in `in_progress`
  with no live path, and the count of parked issues is expected to stay where it is.
