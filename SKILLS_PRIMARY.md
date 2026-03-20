# Replit AI Agent — Primary Skill Documents (Internal Instructions)

**Date:** March 20, 2026
**Purpose:** These are the hidden operational instruction documents loaded by the Replit AI Agent. Users never see these. They control agent behavior.

---

## Skill: agent-inbox

**Path:** `.local/skills/agent-inbox/SKILL.md`

```markdown
---
name: agent-inbox
description: List and manage user feedback items from the agent inbox. Use when the user asks about feedback, bug reports, feature requests, or inbox items.
---

# Agent Inbox Skill

List and manage user feedback items from the agent inbox.

## When to Use

Use this skill when the user:

- Asks about feedback, bug reports, or feature requests
- Wants to check their agent inbox
- Asks you to review or manage inbox items
- Wants to acknowledge, dismiss, or mark feedback as implemented

## When NOT to Use

- To automatically check the inbox without the user asking
- To auto-implement feedback (present items to the user instead)
- For general project task management (use project tasks instead)

## Available Functions

### listAgentInboxItems(statusFilter, topicFilter)

List inbox items with optional filters. Checks if the agent inbox is enabled first.

**Parameters:**

- `statusFilter` (list[str], optional): Filter by status
- `topicFilter` (list[str], optional): Filter by topic

**Status values:** `"PENDING"`, `"ACKNOWLEDGED"`, `"DISMISSED"`, `"IMPLEMENTED"`, `"DELETED"`

**Topic values:** `"BUG_REPORT"`, `"FEATURE_REQUEST"`, `"DESIGN"`, `"CONTENT"`, `"OTHER"`

**Returns:** Dict with:

- `items`: List of inbox items
- `totalCount`: Total number of matching items

Each item contains:

- `id`: Unique item identifier
- `replId`: The repl this item belongs to
- `status`: Current status
- `topic`: Item topic/category
- `feedbackText`: The feedback content
- `currentPage`: Page the feedback was submitted from
- `screenshots`: List of screenshot URLs
- `timeCreated`: ISO timestamp
- `timeUpdated`: ISO timestamp

**Example:**

```javascript
// List all pending items
const result = await listAgentInboxItems({ statusFilter: ["PENDING"] });
for (const item of result.items) {
    console.log(`[${item.topic}] ${item.feedbackText}`);
}

// List bug reports
const result = await listAgentInboxItems({ topicFilter: ["BUG_REPORT"] });
for (const item of result.items) {
    console.log(`[${item.topic}] ${item.feedbackText}`);
}
```

### updateAgentInboxItem(itemId, status)

Update the status of an inbox item.

**Parameters:**

- `itemId` (str, required): The item ID to update
- `status` (str, required): New status to set

**Status values:** `"PENDING"`, `"ACKNOWLEDGED"`, `"DISMISSED"`, `"IMPLEMENTED"`, `"DELETED"`

**Returns:** Dict with the updated item fields (same shape as items in list response).

**Example:**

```javascript
// Acknowledge an item after reviewing it
const result = await updateAgentInboxItem({ itemId: "abc123", status: "ACKNOWLEDGED" });
console.log(`Updated: ${result.id} -> ${result.status}`);
```

## Item Topics

- `BUG_REPORT`: Bug reports from users
- `FEATURE_REQUEST`: Feature requests
- `DESIGN`: Design feedback
- `CONTENT`: Content-related feedback
- `OTHER`: Other feedback

## Item Statuses

- `PENDING`: New, unprocessed item
- `ACKNOWLEDGED`: Item has been seen and noted
- `DISMISSED`: Item was dismissed
- `IMPLEMENTED`: Feedback has been implemented
- `DELETED`: Item was deleted

## Example Workflow

```javascript
// 1. List pending inbox items
const result = await listAgentInboxItems({ statusFilter: ["PENDING"] });
console.log(`Found ${result.totalCount} pending items`);

// 2. Review each item and acknowledge
for (const item of result.items) {
    console.log(`[${item.topic}] ${item.feedbackText}`);
    await updateAgentInboxItem({ itemId: item.id, status: "ACKNOWLEDGED" });
}
```

## Error Handling

- **Inbox not enabled**: Raises `RuntimeError` if the agent inbox is not enabled for the repl
- **Invalid status**: Raises `ValueError` for unrecognized status strings
- **Invalid topic**: Raises `ValueError` for unrecognized topic strings

```

---

## Skill: artifacts

**Path:** `.local/skills/artifacts/SKILL.md`

```markdown
---
name: artifacts
description: "This project only supports mockup sandbox. Call createArtifact() with artifactType 'mockup-sandbox' only."
---


# Artifacts

**This project only supports mockup sandbox.** Only call `createArtifact()` with `artifactType: "mockup-sandbox"`. Do NOT use any other artifact type.

If the user asks to create any other type of artifact (web app, video, slides, mobile), inform them that:

- This project does not support artifacts.
- They can create other artifact types by creating a new project.
- Link: https://replit-add-agent-4-docs.mintlify.app/replitai/artifacts



```

---

## Skill: canvas

**Path:** `.local/skills/canvas/SKILL.md`

```markdown
---
name: canvas
description: Create, read, and manipulate shapes on the workspace canvas. Supports geometric shapes, text, notes, iframe embeds, images, and videos.
---

# Canvas Skill

## Overview

The workspace canvas is an infinite board where you can create, position, and manipulate visual elements. You have two tools:

- **`get_canvas_state`** -- Read what shapes are on the board, their positions, types, and properties.
- **`apply_canvas_actions`** -- Create, update, delete, move, resize, reorder, align, or distribute shapes.

**Always read the board before making layout-sensitive changes.**

## Coordinate System

- Origin `(0, 0)` is at the top-left of the canvas.
- Positive `x` goes right, positive `y` goes down.
- All positions and sizes are in canvas units.

## Supported Shape Types

- `geo` -- Geometric shapes (rectangles, ellipses). Props: `color`, `fill`, `text`.
- `text` -- Text labels. Props: `text`, `color`.
- `note` -- Sticky notes. Props: `text`, `color`.
- `iframe` -- Embedded web content. Requires `url` (https only). Optional: `componentPath`, `componentName`, `componentProps`.
- `image` -- Embedded images. Props: `src` (HTTPS image URL), `altText`. For local files, copy to `.canvas/assets/` and use `https://<domain>:5904/<filename>` as `src`.
- `video` -- Embedded videos. Props: `src` (HTTPS video URL), `altText`. Local files work the same way as images via `.canvas/assets/`.

## Reading the Board: `get_canvas_state`

Returns shapes at three detail levels:

- **focusedShapes** -- Full detail for shapes near the viewport or focus area. Geo/text/note shapes include color, fill, text. Iframe shapes include `url`, `componentName`, `componentPath`. Image shapes include `src`, `altText`, and `filepath` (local file path in `.canvas/assets/`, if applicable). Video shapes include `src` and `altText`.
- **blurryShapes** -- Position and basic info for shapes farther away. Iframe shapes include only `componentName`. Image shapes include `src` and `filepath`. Video shapes include `src`.
- **peripheralClusters** -- Aggregated counts for distant shape groups.
- **summary** -- Quick text description of everything on the canvas.

Pass an optional `focus_area` (`{x, y, w, h}`) to zoom into a specific region.

Example call with no arguments (uses current viewport):

```json
{"focus_area": null}
```

Example response:

```json
{
  "focusedShapes": [
    {
      "shapeId": "box-1",
      "shapeType": "geo",
      "x": 100, "y": 100, "w": 200, "h": 150,
      "color": "blue", "fill": "solid", "text": "Frontend"
    },
    {
      "shapeId": "preview-1",
      "shapeType": "iframe",
      "x": 400, "y": 100, "w": 1280, "h": 720,
      "url": "https://<resolved-domain>.replit.dev/preview/hello-world/Card",
      "componentName": "Card",
      "componentPath": "mockup/src/components/mockups/hello-world/Card.tsx"
    }
  ],
  "blurryShapes": [
    {
      "shapeId": "distant-iframe",
      "shapeType": "iframe",
      "x": 5000, "y": 100, "w": 1280, "h": 720,
      "componentName": "Sidebar"
    }
  ],
  "peripheralClusters": [],
  "viewport": {"x": 0, "y": 0, "w": 1920, "h": 1080},
  "summary": "2 shapes on canvas.",
  "focusedOmittedCount": 0,
  "blurryOmittedCount": 0
}
```

Focused iframe shapes include `url`, `componentName`, and `componentPath`. Blurry iframe shapes only include `componentName` (no URL or path). Focused image shapes include `src`, `altText`, and `filepath`. Focused video shapes include `src` and `altText`. Blurry image shapes include `src` and `filepath`. Blurry video shapes include `src`.

## Modifying the Board: `apply_canvas_actions`

Send an ordered list of actions. Each action has a `type` field. Results are returned per-action with generated `shapeId` values.

### Create

Set a `shapeId` so you can reference the shape later.

```json
{
  "type": "create",
  "shapeId": "my-box",
  "shape": {
    "type": "geo",
    "x": 100, "y": 100, "w": 200, "h": 150,
    "color": "blue", "fill": "solid", "text": "Hello"
  }
}
```

### Create Iframe

Embed live web content. The `url` **must** use `https://`.

To get the URL for a Replit dev server, run `echo $REPLIT_DOMAINS` in the shell to get the domain, then construct the full URL. For the main app on port 5000, no port suffix is needed. For other ports, append `:<port>`.

**Always resolve the actual domain first** -- do not pass literal template strings as the iframe URL.

```json
{
  "type": "create",
  "shapeId": "app-preview",
  "shape": {
    "type": "iframe",
    "x": 0, "y": 0, "w": 1280, "h": 720,
    "url": "https://<resolved-domain>.replit.dev",
    "componentName": "App Preview"
  }
}
```

- `url` -- **Required.** Must be `https`. This is what actually loads content.
- `componentPath` -- File path shown in the title bar (metadata label only).
- `componentName` -- Display name shown in the title bar (metadata label only).
- `componentProps` -- Extra props dict merged into shape props.

**To embed individual React components** (not just the full app), you need a component preview server that renders each component at its own URL. Use the **mockup-sandbox** skill to set it up.

### Create Image

Embed an image on the canvas.

From an external URL:

```json
{
  "type": "create",
  "shapeId": "hero-image",
  "shape": {
    "type": "image",
    "x": 0, "y": 0, "w": 800, "h": 600,
    "src": "https://example.com/hero.png",
    "altText": "Hero banner image"
  }
}
```

From a local file (copy to `.canvas/assets/`, resolve domain, use port 5904):

```bash
mkdir -p .canvas/assets
cp assets/hero.png .canvas/assets/hero.png
echo $REPLIT_DOMAINS  # e.g. abc123.replit.dev
```

```json
{
  "type": "create",
  "shapeId": "hero-image",
  "shape": {
    "type": "image",
    "x": 0, "y": 0, "w": 800, "h": 600,
    "src": "https://<resolved-domain>:5904/hero.png",
    "altText": "Hero banner image"
  }
}
```

### Create Video

Embed a video on the canvas. Local files work the same way as images via `.canvas/assets/`.

From an external URL:

```json
{
  "type": "create",
  "shapeId": "demo-video",
  "shape": {
    "type": "video",
    "x": 0, "y": 0, "w": 1280, "h": 720,
    "src": "https://example.com/demo.mp4",
    "altText": "Product demo video"
  }
}
```

From a local file:

```bash
cp assets/demo.mp4 .canvas/assets/demo.mp4
```

```json
{
  "type": "create",
  "shapeId": "demo-video",
  "shape": {
    "type": "video",
    "x": 0, "y": 0, "w": 1280, "h": 720,
    "src": "https://<resolved-domain>:5904/demo.mp4",
    "altText": "Product demo video"
  }
}
```

### Update

Only include the fields you want to change. Always set `shapeType` to the shape's type (from get_canvas_state).

```json
{
  "type": "update",
  "shapeId": "my-box",
  "updates": {"shapeType": "geo", "color": "red", "text": "Updated"}
}
```

### Delete

```json
{"type": "delete", "shapeId": "my-box"}
```

### Move

```json
{"type": "move", "shapeId": "my-box", "x": 300, "y": 200}
```

### Resize

```json
{"type": "resize", "shapeId": "my-box", "w": 400, "h": 300}
```

### Reorder (Z-index)

Direction: `"front"` or `"back"`.

```json
{"type": "reorder", "shapeId": "my-box", "direction": "front"}
```

### Align

Align multiple shapes. Options: `"left"`, `"center-horizontal"`, `"right"`, `"top"`, `"center-vertical"`, `"bottom"`.

```json
{
  "type": "align",
  "shapeIds": ["box-1", "box-2", "box-3"],
  "alignment": "center-horizontal"
}
```

### Distribute

Evenly space shapes. Direction: `"horizontal"` or `"vertical"`.

```json
{
  "type": "distribute",
  "shapeIds": ["box-1", "box-2", "box-3"],
  "direction": "horizontal"
}
```

## Iframe Rules & Gotchas

- **URL must be `https`** -- `http` and `about:blank` are rejected.
- **Resolve the domain first** -- run `echo $REPLIT_DOMAINS` in the shell, then build the URL from the result. Never pass a literal template string as the URL.
- **Port rules:** no port suffix = port 5000 (main app). For other servers, append `:<port>`.
- **External sites may block embedding** -- sites with `X-Frame-Options: DENY` or restrictive CSP headers will show a blank iframe. Replit dev URLs work fine.
- **For component previews, use the mockup sandbox** -- do not embed the main app's dev server URL to preview individual components. The main app URL shows the entire app with navigation, layout, and routing — not an isolated component. Use the mockup-sandbox skill to set up a preview server, then embed `/preview/{folder}/{Component}` URLs. This gives you isolated components that can be iterated on independently.

### Placeholder Workflow

Since iframe URLs must be `https` (no `about:blank`), to plan a layout before you have real URLs:

1. Create `geo` shapes at the desired positions with labels describing what goes there.
2. Once you have the real URLs, delete the `geo` shapes.
3. Create `iframe` shapes at the same positions with the actual URLs.

## Typical Workflow

1. Call `get_canvas_state` to see what's on the board.
2. Use the `summary` and `focusedShapes` to understand positions and IDs.
3. Call `apply_canvas_actions` with a batch of changes.
4. **Communicate and offer to show** -- Tell the user what you placed and where, referencing shape names or labels so they can orient themselves. Then ask if they'd like you to focus on the new or changed shapes (e.g. "Want me to pan to the new layout?"). Don't auto-focus -- moving the viewport while the user is working is disorienting.
5. **Show on request** -- When the user confirms, call `focus_canvas_shapes` with the IDs of all relevant shapes. Use `animate_ms: 500` for a smooth transition.

## Error Codes

- `SHAPE_NOT_FOUND` -- Shape ID doesn't exist.
- `UNSUPPORTED_SHAPE_TYPE` -- Invalid shape type.
- `INVALID_PROPS` -- Bad property values (e.g., non-https iframe URL).
- `VALIDATION_FAILED` -- Shape with that ID already exists.
- `INSUFFICIENT_SHAPES` -- Not enough shapes for align/distribute.

## Best Practices

1. **Read before writing** -- Always call `get_canvas_state` before layout-sensitive changes.
2. **Set shapeId on create** -- So you can reference, update, or delete the shape later.
3. **Offer to show your work.** After creating or significantly modifying shapes, don't auto-focus the viewport -- the user may be looking at something else and sudden panning is disorienting. Instead, finish your work and ask the user if they'd like to see it (e.g. "Would you like me to focus on the new shapes?"). When the user confirms, call `focus_canvas_shapes` on the affected shape IDs with `animate_ms: 500` for smooth transitions. After a batch of creates, focus on all new shape IDs together in a single call.
4. **Batch actions** -- Group related changes in one `apply_canvas_actions` call.
5. **Use https URLs** -- Iframe shapes reject http URLs.
6. **Label iframes** -- Set `componentPath` and `componentName` so users can identify embedded content.
7. **Use focus_area** -- For large boards, pass a region to `get_canvas_state` to get detail where you need it.

### Viewport Presets

- Mobile: 390 x 844
- Tablet: 768 x 1024
- Desktop: 1280 x 720

```

---

## Skill: code_review

**Path:** `.local/skills/code_review/SKILL.md`

```markdown
---
name: code_review
description: Spawn a code review (architect) subagent for deep analysis, planning, and debugging. The architect specializes in strategic guidance rather than implementation. Architect should be called after building major features. Relies on `delegation` skill.
---

# Architect Skill

Spawn an code review (a.k.a architect) subagent for analysis and planning. The architect specializes in analysis and strategic guidance rather than implementation.

## When to Use

Use this skill when:

- You need deep architectural analysis or code understanding
- You want strategic recommendations about system design or patterns
- You need comprehensive analysis of code quality or technical debt
- You want root cause analysis and debugging assistance

## When NOT to Use

- Simple tasks that you can complete directly
- Tasks that require file edits or implementation (use delegation skill instead)
- Read-only operations (use grep/glob/read tools instead)

## Available Functions

### architect(task, relevantFiles, ...)

Spawn an architect subagent for analysis and planning.

**Parameters:**

- `task` (str, required): The analytical task or question for the architect
- `relevantFiles` (list[str], required): Full file paths to analyze
- `responsibility` (str, default "evaluate_task"): Focus area: "debug", "plan", or "evaluate_task"
- `includeGitDiff` (bool, default False): Include current unstaged git diff
- `relevantGitCommits` (str, optional): Git commit range to analyze (e.g., "HEAD~3..HEAD")

**Returns:** Dict with analysis results

```json
{
    "success": true,
    "message": "Analysis summary",
    "subagentAlias": "architect_1",
    "result": "Full analysis output..."
}
```

**Responsibilities:**

- **evaluate_task**: Assess completed or ongoing work against goals
- **plan**: Create implementation plans with task decomposition and sequencing
- **debug**: Root cause analysis, reproduction steps, and recommended fixes

**Example:**

```javascript
// Plan a new feature
const result = await architect({
    task: "Create a plan for implementing rate limiting on API endpoints.",
    relevantFiles: ["src/middleware/index.ts", "src/routes/api.ts"],
    responsibility: "plan"
});
console.log(result.result);

// Debug an issue
const result2 = await architect({
    task: "The UserAuthService.validateSession() returns false for valid tokens.",
    relevantFiles: ["src/services/UserAuthService.ts", "src/utils/jwt.ts"],
    responsibility: "debug",
    includeGitDiff: true
});
```

## Best Practices

1. **Be specific in your task description**: Include concrete function names, error messages, or design goals
2. **Provide relevant files**: The architect can only analyze files you pass in `relevantFiles`
3. **Choose the right responsibility**: Use "plan" for new work, "debug" for issues, "evaluate_task" for reviewing progress
4. **Use `includeGitDiff`**: When debugging regressions, include the diff to help the architect identify recent changes
5. **Use `relevantGitCommits`**: When you need the architect to understand recent history (e.g., "HEAD~3..HEAD")

```

---

## Skill: database

**Path:** `.local/skills/database/SKILL.md`

```markdown
---
name: database
description: Create and manage Replit's built-in PostgreSQL databases, check status, execute SQL queries with safety checks, and run read-only queries against the production database. Use when the user wants to check prod data, debug database issues in production, or asks to "check the prod db", "query production", "look at live data", or "see what's in the database on the deployed app".
---

# Database Skill

Manage PostgreSQL databases and execute SQL queries safely in your development and production environments.

## When to Use

Use this skill when:

- Creating a new PostgreSQL database for your project
- Checking if a database is provisioned and accessible
- Running SQL queries against the development or production database
- Querying data warehouses (BigQuery, Databricks, Snowflake)

## When NOT to Use

- Schema migrations in production environments
- Direct modifications to Stripe tables (use Stripe API instead)
- Converting a pre-existing database over to Replit, unless a user explicitly asks you to.

## Available Functions

### checkDatabase()

Check if the PostgreSQL database is provisioned and accessible.

**Parameters:** None

**Returns:** Dict with `provisioned` (bool) and `message` (str)

**Example:**

```javascript
const status = await checkDatabase();
if (status.provisioned) {
    console.log("Database is ready!");
} else {
    console.log(status.message);
    // Consider calling createDatabase()
}
```

### createDatabase()

Create or verify a PostgreSQL database exists for the project.

**Parameters:** None

**Returns:** Dict with:

- `success` (bool): Whether operation succeeded
- `message` (str): Status message
- `alreadyExisted` (bool): True if database already existed
- `secretKeys` (list): Environment variables set (DATABASE_URL, PGHOST, etc.)

**Example:**

```javascript
const result = await createDatabase();
if (result.success) {
    console.log(`Database ready! Environment variables: ${result.secretKeys}`);
    // Now you can use DATABASE_URL in your application
}
```

### executeSql()

Execute a SQL query with safety checks.

**Parameters:**

- `sqlQuery` (str, required): The SQL query to execute
- `target` (str, default "replit_database"): Target database: "replit_database", "bigquery", "databricks", or "snowflake"
- `environment` (str, default "development"): "development" runs against the development database (all SQL operations supported). "production" runs READ-ONLY queries against a replica of the production database (only SELECT queries allowed). Production is only supported for the "replit_database" target. "production" database, depending on when the user last deployed, may have outdated schemas.
- `sampleSize` (int, optional): Sample size for warehouse queries (only for bigquery/databricks/snowflake)

**Returns:** Dict with:

- `success` (bool): Whether query succeeded
- `output` (str): Query output/results
- `exitCode` (int): Exit code (0 = success)
- `exitReason` (str | None): Reason for exit if failed

**Example:**

```javascript
// Simple SELECT query
const result = await executeSql({ sqlQuery: "SELECT * FROM users LIMIT 5" });
if (result.success) {
    console.log(result.output);
}

// CREATE TABLE
const result2 = await executeSql({
    sqlQuery: `
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2)
        )
    `
});

// INSERT data
const result3 = await executeSql({
    sqlQuery: `
        INSERT INTO products (name, price)
        VALUES ('Widget', 19.99)
    `
});

// Read-only production query
const result4 = await executeSql({
    sqlQuery: "SELECT * FROM users WHERE active = true",
    environment: "production"
});

// Data warehouse query with sampling
const result5 = await executeSql({
    sqlQuery: "SELECT * FROM sales_data WHERE year = 2024",
    target: "bigquery",
    sampleSize: 100
});
```

## Safety Features

1. **Environment Isolation**: Development queries run against the development database; production queries are READ-ONLY against a read replica
2. **Stripe Protection**: Mutations to Stripe schema tables (stripe.*) are blocked
3. **Discussion Mode**: Mutating queries are blocked in Planning/Discussion mode
4. **Destructive Query Protection**: DROP, TRUNCATE, etc. are blocked via the skill callback path (use the tool interface directly for destructive operations that require user confirmation)

## Best Practices

1. **Prefer the built-in database**: Replit's built-in PostgreSQL database is always preferred over external services like Supabase. It supports rollback and integrates directly with the Replit product. Only use external database services if the user has specific requirements. The `pg` package should be installed already.
2. **Check before creating**: Call `checkDatabase()` before `createDatabase()` to avoid unnecessary operations
3. **Use parameterized queries**: Avoid string interpolation for user input
4. **Test queries first**: Run SELECT queries before INSERT/UPDATE/DELETE
5. **Keep backups**: Important data should be backed up before destructive operations

## Environment Variables

After creating a database, these environment variables are available:

- `DATABASE_URL`: Full connection string
- `PGHOST`: Database host
- `PGPORT`: Database port (5432)
- `PGUSER`: Database username
- `PGPASSWORD`: Database password
- `PGDATABASE`: Database name

## Example Workflow

```javascript
// 1. Check if database exists
const status = await checkDatabase();

if (!status.provisioned) {
    // 2. Create database
    const createResult = await createDatabase();
    if (!createResult.success) {
        console.log(`Failed: ${createResult.message}`);
    }
}

// 3. Create schema
await executeSql({
    sqlQuery: `
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    `
});

// 4. Insert data
await executeSql({
    sqlQuery: `
        INSERT INTO users (email)
        VALUES ('user@example.com')
    `
});

// 5. Query data
const result = await executeSql({ sqlQuery: "SELECT * FROM users" });
console.log(result.output);
```

## Limitations

- Production queries are READ-ONLY (SELECT only) — INSERT, UPDATE, DELETE, and DDL statements will fail
- Production environment is only supported for the "replit_database" target (not data warehouses)
- Cannot modify Stripe schema tables (read-only)
- Destructive queries (DROP, TRUNCATE, etc.) are blocked via the skill callback path
- Mutating queries blocked in Planning mode

## Rollbacks

As stated in the diagnostic skills, the development database support rollbacks. Open that skill for more information.

```

---

## Skill: delegation

**Path:** `.local/skills/delegation/SKILL.md`

```markdown
---
name: delegation
description: Delegate tasks to specialized subagents. Use subagent for synchronous task execution, startAsyncSubagent for background task execution, messageSubagent for async follow-ups, or messageSubagentAndGetResponse for sync follow-ups.
---

# Delegation Skill

Delegate tasks to specialized subagents for autonomous execution.

## When to Use

Use this skill when:

- You need to delegate tasks to run autonomously (especially when you have a session plan)
- You have multiple independent tasks that can run in parallel

## When NOT to Use

- Simple tasks that you can complete directly
- Tasks that require immediate user interaction
- Read-only operations (use grep/glob/read tools instead)
- Quick file edits (use edit tool directly)
- Analysis, planning, or debugging (e.g. performing code review)

## Available Functions

### subagent(task, fromPlan, relevantFiles)

Launch a subagent to handle a task synchronously. Blocks until the subagent completes and returns the result.

**Parameters:**

- `task` (str, required): Task ID from session plan (e.g., "T003") OR brief task description
- `fromPlan` (bool, default False): If True, subagent reads full task context from .local/session_plan.md
- `relevantFiles` (list[str], optional): File paths the subagent should access. Include skill paths if subagent needs skills
- `specialization` (str, default "GENERAL"): "GENERAL" or "SMALL_TASK" for quick tasks

**Returns:** Dict with task results

```json
{
    "success": true,
    "message": "Task summary",
    "subagentAlias": "subagent_1",
    "result": "Full task output..."
}
```

**Usage Patterns:**

**1. From Plan (Recommended when you have a session plan):**

```javascript
// Reference tasks by ID - subagent reads full context from .local/session_plan.md
const result = await subagent({ task: "T003", fromPlan: true });
console.log(result);  // Always print the result
```

**2. Direct Task (for ad-hoc tasks without a plan):**

```javascript
const result = await subagent({
    task: "Fix the auth bug in src/auth.ts",
    relevantFiles: ["src/auth.ts"]
});
console.log(result);  // Always print the result
```

### startAsyncSubagent(task, fromPlan, relevantFiles)

Launch a subagent to handle a task asynchronously in the background. Returns immediately without waiting for completion. Use `waitForBackgroundTasks` to collect results later.

**Parameters:**

- `task` (str, required): Task ID from session plan (e.g., "T003") OR brief task description
- `fromPlan` (bool, default False): If True, subagent reads full task context from .local/session_plan.md
- `relevantFiles` (list[str], optional): File paths the subagent should access. Include skill paths if subagent needs skills
- `specialization` (str, default "GENERAL"): "GENERAL" or "SMALL_TASK" for quick tasks

**Returns:** Immediately with acknowledgment. Results come via `waitForBackgroundTasks`.

**Usage Patterns:**

**1. From Plan (Recommended when you have a session plan):**

```javascript
// Reference tasks by ID - no print needed, result comes via wait_for_background_tasks
await startAsyncSubagent({ task: "T003", fromPlan: true });
```

**2. Direct Task (for ad-hoc tasks without a plan):**

```javascript
await startAsyncSubagent({
    task: "Fix the auth bug in src/auth.ts",
    relevantFiles: ["src/auth.ts"]
});
```

**Parallel Execution:**

```javascript
// Launch independent tasks simultaneously
console.log(await startAsyncSubagent({ task: "T002", fromPlan: true }));
console.log(await startAsyncSubagent({ task: "T003", fromPlan: true }));
console.log(await startAsyncSubagent({ task: "T004", fromPlan: true }));
```

**Giving Subagents Access to Skills:**

```javascript
// Include skill documentation in relevantFiles if subagent needs it
await startAsyncSubagent({
    task: "T005",
    fromPlan: true,
    relevantFiles: [".local/skills/database/SKILL.md"]
});
```

### messageSubagent(subagentId, message)

Send a follow-up message to an existing subagent asynchronously. Returns immediately after the message is delivered. Use this when the subagent should continue in the background.

**Parameters:**

- `subagentId` (str, required): Alias returned when the subagent was started
- `message` (str, required): Follow-up instruction or clarification for the subagent

**Returns:** Acknowledgment that the message was sent. The subagent keeps running in the background.

**Example:**

```javascript
// Async follow-up: continue background work
await messageSubagent({
    subagentId: "subagent-happy-tiger",
    message: "After the fix, add regression tests for the auth edge case."
});

// Collect results later
await waitForBackgroundTasks();
```

### messageSubagentAndGetResponse(subagentId, message, timeoutSeconds)

Send a follow-up message to an existing subagent synchronously. Blocks until the subagent completes, times out, or is interrupted.

**Parameters:**

- `subagentId` (str, required): Alias returned when the subagent was started
- `message` (str, required): Follow-up instruction or clarification for the subagent
- `timeoutSeconds` (float, default 300.0): Max time to wait before returning a timeout status

**Returns:** Dict with `success`, `message`, `result`, and `exitReason`.

**Example:**

```javascript
// Sync follow-up: wait for the answer now
const result = await messageSubagentAndGetResponse({
    subagentId: "subagent-happy-tiger",
    message: "Summarize root cause and include exact changed files.",
    timeoutSeconds: 180.0
});
console.log(result.result);
```

**When to choose which:**

- Use `messageSubagent` when you want fire-and-forget behavior
- Use `messageSubagentAndGetResponse` when you need the response immediately

## Best Practices

1. **Use session plans**: For 2+ tasks, create a .local/session_plan.md and use `fromPlan=True`
2. **Launch in parallel**: Independent tasks can run simultaneously with `startAsyncSubagent`
3. **Use `subagent()` when you need the result immediately**: For tasks where you need to act on the output, use the synchronous `subagent()` and print the result.
4. **Use `startAsyncSubagent()` for independent tasks that can run in the background**: The tasks will be performed in parallel.
5. **Use `messageSubagent()` for async follow-ups**: Message running subagents without blocking and collect results with `waitForBackgroundTasks`
6. **Use `messageSubagentAndGetResponse()` for sync follow-ups**: Use this when you need the subagent's output before continuing
7. **Trust the results**: Subagent outputs should generally be trusted
8. **Pass skills via relevantFiles**: If a subagent needs skills, include the skill's SKILL.md path

## Subagent Capabilities

The subagent has access to:

- File operations (read, write, edit, glob, grep)
- Bash commands
- LSP diagnostics
- Skills (via code_execution, if you include skill docs in relevantFiles)

The subagent does **NOT**:

- Run or restart workflows
- Check workflow/console logs
- Preview/test the app (that's your job as main agent)

```

---

## Skill: deployment

**Path:** `.local/skills/deployment/SKILL.md`

```markdown
---
name: deployment
description: Configure and publish your project. Use to set deployment settings and suggest publishing when the app is ready.
---

# Deployment Skill

Configure deployment settings and publish your project to make it live and accessible.

## When to Use

Use this skill when:

- Configuring how the project should run in production
- The project is in a working state and ready for publishing
- The user explicitly asks to publish or deploy the project
- You've completed implementing a feature and verified it works
- Setting up deployment for different project types (websites, bots, scheduled jobs)

## When NOT to Use

- Project has known errors or incomplete features
- You haven't validated that the project works
- The user is just testing or prototyping
- **You are a task agent running in a subrepl context and want to suggest publishing** — only the main repl can trigger a publish. However, `deployConfig()` is allowed because it only modifies `.replit` configuration. If you call `deployConfig()` from a task agent, remind the user that they will need to publish from the main version of the project after the current task is merged

## Available Functions

### deployConfig(deploymentTarget, run, build, publicDir)

Configure how the project should be deployed to production.

**Parameters:**

- `deploymentTarget` (str, required): "autoscale", "vm", "scheduled", or "static"
- `run` (list[str], optional): Production run command. First entry is binary/script, rest are arguments
- `build` (list[str], optional): Build/compile command before deployment
- `publicDir` (str, required for "static"): Directory containing static files

**Returns:** Dict with `success`, `message`, and configuration details

**Example:**

```javascript
// Configure a Python web app
const result = await deployConfig({
    deploymentTarget: "autoscale",
    run: ["gunicorn", "--bind=0.0.0.0:5000", "--reuse-port", "main:app"]
});

// Configure a static site
const result2 = await deployConfig({
    deploymentTarget: "static",
    build: ["npm", "run", "build"],
    publicDir: "dist"
});

// Configure an always-running bot
const result3 = await deployConfig({
    deploymentTarget: "vm",
    run: ["python", "bot.py"]
});
```

## Deployment Targets

Choose the appropriate deployment target based on your project type:

### autoscale (Recommended Default)

Use for stateless websites and APIs that don't need persistent server memory.

- **Best for:** Web applications, REST APIs, stateless services
- **Behavior:** Scales up/down based on traffic, only runs when requests arrive
- **State:** Use databases for persistent state (not server memory)
- **Cost:** Most cost-effective for variable traffic

```javascript
await deployConfig({
    deploymentTarget: "autoscale",
    run: ["gunicorn", "--bind=0.0.0.0:5000", "app:app"]
});
```

### vm (Always Running)

Use for applications that need persistent server-side state or long-running processes.

- **Best for:** Discord/Telegram bots, WebSocket servers, web scrapers, background workers
- **Behavior:** Always running, maintains state in server memory
- **State:** Can use in-memory databases, local files, or external databases

```javascript
await deployConfig({
    deploymentTarget: "vm",
    run: ["python", "bot.py"]
});
```

### scheduled

Use for cron-like jobs that run on a schedule.

- **Best for:** Data processing, cleanup tasks, periodic reports, batch jobs
- **Behavior:** Runs on configured schedule, not continuously
- **Note:** Do NOT use for websites or APIs

```javascript
await deployConfig({
    deploymentTarget: "scheduled",
    run: ["python", "daily_report.py"]
});
```

### static

Use for client-side websites with no backend server.

- **Best for:** Static HTML sites, SPAs (React, Vue, etc.), documentation sites
- **Behavior:** Serves static files directly, no server-side processing
- **Note:** The `run` command is ignored; must specify `publicDir`

```javascript
await deployConfig({
    deploymentTarget: "static",
    build: ["npm", "run", "build"],
    publicDir: "dist"
});
```

## Run Command Examples

Use production-ready servers, not development servers:

```toml
# Python with Gunicorn
run=["gunicorn", "--bind=0.0.0.0:5000", "--reuse-port", "main:app"]

# Python with Streamlit
run=["streamlit", "run", "main.py"]

# Node.js
run=["node", "server.js"]

# Multiple processes with bash
run=["bash", "-c", "gunicorn --reuse-port -w 4 -b 0.0.0.0:8000 app:app & npm run dev"]
```

## Build Command Examples

Only use build commands when compilation is needed:

```toml
# TypeScript/bundler
build=["npm", "run", "build"]

# Multiple build steps
build=["bash", "-c", "make assets && make compile"]

# Rust
build=["cargo", "build", "--release"]
```

## Best Practices

1. **Validate before publishing**: Always verify the project works before suggesting publish
2. **Use production servers**: Avoid insecure development servers in production
3. **Choose the right target**: Match deployment type to your application's needs
4. **Configure once**: Set up deployment config early, then suggest publishing when ready
5. **Check workflows first**: Ensure workflows are running without errors before publishing

## Important Notes

1. **User-initiated publishing**: The user must click the Publish button to actually deploy
2. **Automatic handling**: Publishing handles building, hosting, TLS, and health checks automatically
3. **Domain**: Published apps are available at a `.replit.app` domain or custom domain if configured

## Example Workflow

```javascript
// 1. Configure deployment settings for a web app
await deployConfig({
    deploymentTarget: "autoscale",
    run: ["gunicorn", "--bind=0.0.0.0:5000", "app:app"]
});

// 2. After verifying the app works, suggest publishing to the user
```

```

---

## Skill: design

**Path:** `.local/skills/design/SKILL.md`

```markdown
---
name: design
description: Delegate design tasks to a specialized design subagent. Use subagent with specialization="DESIGN" for synchronous execution or startAsyncSubagent for background execution.
---

# Design Skill


This skill provides two approaches for frontend design work:

1. **`generateFrontend()`** — Fast background frontend generation via `code_execution_tool`. Use this for the **initial build** of a frontend only for react-vite artifacts. Do not use this for any other artifact. It generates a complete, production-ready React frontend in the background while you continue working on the backend.
2. **Design subagent** — A specialized subagent with access to file operations, media generation, web search, and frontend tooling. Use this for **design iterations, fixes, and refinements** after the initial build.

## generateFrontend() — Initial Frontend Build

Use `generateFrontend()` through the `code_execution_tool` to generate the entire frontend in the background. This is significantly faster than launching a design subagent for the first build.

### When to Use

- Initial frontend creation — generating all pages, components, hooks, and styles from scratch
- When the OpenAPI spec and codegen are already done and you need a complete frontend built fast
- For react-vite artifacts only

### When NOT to Use

- Design iterations or visual refinements after the initial build (use the design subagent instead)
- Fixing specific frontend bugs or tweaking individual components (use file editing tools or the design subagent)
- For artifacts like Expo, Slides, Animations, etc.

### generateFrontend(options)

Call this via `code_execution_tool`. It runs in the background — use `wait_for_background_tasks` to check when it's done.

**Parameters:**

- `designStyle` (str, optional): Visual style hint (e.g. "clean minimal", "dark mode professional", "bold colorful startup")
- `implementationNotes` (str, optional): Backend context the frontend needs to know — auth flows, external API integrations, special data patterns
- `artifactPath` (str, **required**): Path to the frontend artifact in the monorepo (e.g. "artifacts/web-app"). This controls where generated files are written — without it, files go to `client/` at the workspace root instead of inside your artifact
- `relevantFiles` (list[str], optional): File paths to read and include as context for generation. Pass generated hooks, existing components, CSS theme files, etc. The generator reads these files and uses their contents to produce accurate, well-integrated code

**Returns:** Dict with job status

```json
{
    "status": "started",
    "jobId": "frontend-happy-tiger",
    "description": "generating frontend components"
}
```

**Example:**

```javascript
const result = await generateFrontend({
    designStyle: "clean minimal with dark mode, professional feel",
    implementationNotes: "REST API at /api, uses JWT auth, has real-time updates via SSE",
    artifactPath: "artifacts/web-app",
    relevantFiles: [
        "lib/api-client-react/src/generated/api.ts",
        "lib/api-client-react/src/generated/api.schemas.ts",
        "artifacts/[react-vite-slug-name]/components/ui/button.tsx",
        "artifacts/[react-vite-slug-name]/src/components/ui/select.tsx"
    ]
});
console.log(result);
// Then continue building the backend while frontend generates
```

### Best Practices for generateFrontend()

1. **Always pass `artifactPath`** — this tells the generator where to write files. Without it, files land in `client/` at the root instead of inside your artifact (e.g. `artifacts/notes-app/src/`).
2. **Call immediately after codegen** — run `pnpm --filter @workspace/api-spec run codegen` first, then call `generateFrontend()` right away. Pass the generated files via `relevantFiles` so the generator has the API hooks and schemas as context. Do not waste time reading codegen output yourself before calling.
3. **Keep working while it runs** — build the backend, set up the database, implement API handlers while the frontend generates in the background.
3. **Trust the output** — the generated frontend is production-ready. Fix integration issues after it completes rather than reviewing every file.
4. **Pass abstract style moods, not product names** — use short visual style hints like "clean minimal", "bold colorful", "dark mode professional", or "playful startup". Do not reference specific products (e.g. "inspired by Linear"), and do not specify colors, fonts, layout details, or design-specific terminology.
5. **Ensure all requirements are met** - The generateFrontend callback will write a file to: `artifacts/notes-app/requirements.yaml` where it specifies what libraries it used and are required. Packages installation and image generation also happens in the background.
6. **index.css** - When you are calling generateFrontend for the first time, add a note in the implementationNotes that the index css is a placeholder. It should use the same format but the current index.css just has placeholder colors but the format must be respected

---

## Design Subagent — Iterations & Refinements



Delegate design-focused tasks to a specialized design subagent with access to file operations, media generation, web search, and frontend tooling.
It is important you tell the design subagent which folder/files it should work within.
It has access to the entire project but it should be given very clear instructions about where it should work either through the task description (if it's a folder) or through relevant files (if it's a few files).
Trust the design subagent's execution of visual details (fonts, colors, spacing). However, when delegating variation generation, include context about what the component does and which dimensions would be most valuable to explore. The design subagent needs to understand the design problem, not just the file path.
If there are specific function or variable names you require the agent to use, outline them in the task description.

### When to Use the Design Subagent

- Design iterations, visual refinements, and polish after the initial frontend build
- Tasks involving image generation, video generation, or stock imagery
- Redesigning specific components or sections with creative direction
- When you need a subagent with design-specific capabilities (image/video generation, stock images, web search)

### When NOT to Use the Design Subagent

- Initial frontend generation (use `generateFrontend()` instead — it's faster)
- General coding tasks without a design focus
- Simple file edits or read-only operations (use tools directly)
- Analysis, planning, or debugging tasks (use code_review skill instead)

### Available Functions


### subagent(task, specialization="DESIGN", relevantFiles)

Launch a design subagent synchronously. Blocks until the subagent completes and returns the result.
**IMPORTANT**: You must include specialization="DESIGN" when you call the design subagent, otherwise it will initialize a general subagent

**Parameters:**

- `task` (str, required): Description of the design task to execute
- `specialization` (str, required): Must be `"DESIGN"` for design tasks
- `relevantFiles` (list[str], optional): File paths the subagent should access

**Returns:** Dict with task results

```json
{
    "success": true,
    "message": "Task summary",
    "subagentAlias": "subagent_design_1",
    "result": "Full task output..."
}
```

**Example:**

```javascript
const result = await subagent({
    task: "Redesign the landing page hero section with a modern gradient background, update typography to use Inter font, and generate a hero illustration",
    specialization: "DESIGN",
    relevantFiles: ["src/pages/landing.tsx", "src/styles/globals.css"]
});
console.log(result);
```

### startAsyncSubagent(task, specialization="DESIGN", relevantFiles)

Launch a design subagent asynchronously in the background. Returns immediately without waiting for completion. Use `waitForBackgroundTasks` to collect results later.

**Parameters:**

- `task` (str, required): Description of the design task to execute
- `specialization` (str, required): Must be `"DESIGN"` for design tasks
- `relevantFiles` (list[str], optional): File paths the subagent should access

**Returns:** Immediately with acknowledgment. Results come via `waitForBackgroundTasks`.

**Example:**

```javascript
await startAsyncSubagent({
    task: "Create a responsive navbar with mobile hamburger menu and smooth animations",
    specialization: "DESIGN",
    relevantFiles: ["src/components/Navbar.tsx", "src/styles/navbar.css"]
});
```


### Best Practices

1. **Be specific about visual requirements**: Include details like colors, fonts, layout, responsive behavior
2. **Include relevant files**: Pass CSS files, component files, and asset directories so the subagent has context
3. **Trust the results**: Design subagent outputs should generally be trusted
4. **Ideally, include design-relevant context files in `relevantFiles`**: The design subagent produces better results when it starts with key project files already open. Consider passing:
   - The main CSS/theme file (e.g., `client/src/index.css`, `src/globals.css`)
   - The API contract or generated hooks (e.g., `shared/schema.ts`, `lib/api-spec/openapi.yaml`)
   - 1-2 existing page or component files as pattern examples


### Design Subagent Capabilities

The design subagent has access to:

- File operations (read, write, edit, glob, grep)
- Bash commands
- Package management
- LSP diagnostics
- Web search and web fetch
- Image generation
- Video generation
- Stock image search

The design subagent does **NOT**:

- Run or restart workflows
- Check workflow/console logs
- Preview/test the app (that's your job as main agent)
- Spawn nested subagents

```

---

## Skill: design-exploration

**Path:** `.local/skills/design-exploration/SKILL.md`

```markdown
---
name: design-exploration
description: "Use this skill when the user asks to 'generate variations,' 'explore alternatives,' 'try different approaches,' 'show me options,' 'what else could this be,' or any request that implies divergent design exploration rather than deterministic editing. Also activate when the user selects a component and asks for 'ideas,' 'directions,' or 'possibilities.' This skill intercepts the request at the main agent level and produces a structured design brief BEFORE delegating to the design subagent. Do NOT skip the analysis phase. Do NOT pass raw file paths without a design brief."
---

# Design Exploration

## Purpose

This skill ensures the agent performs **problem comprehension before generation** when handling variation requests. Analyze what a component does, what constrains it, and what is meaningfully free to vary — then compose a design brief and pass it to the design subagent. Never skip straight from "user asked for variations" to output.

Design exploration is the divergent phase of an explore/exploit loop. Each variation should represent a **distinct design hypothesis** — a meaningfully different answer to "what could this be?" — not a reskin of the same hypothesis.

## Step 1: Read and Comprehend the Component

Read the selected component's source code and surrounding context (parent layout, route structure, dependencies, styles). Build an internal model of:

- **Function**: What does it do? What user problem does it solve? What's its role in the broader flow?
- **Content model**: What information does it present or collect? What's the semantic structure?
- **Interaction model**: How does the user engage with it? What states and transitions exist?
- **Visual structure**: How is it composed? What are its regions, hierarchy, and spatial relationships?
- **Context**: Where does it live? What comes before and after? What assumptions does it inherit?

## Step 2: Identify Constraints and Degrees of Freedom

Distinguish between:

- **Hard constraints**: Cannot change without breaking the component (required data fields, accessibility requirements, platform constraints, explicit user decisions).
- **Soft constraints**: Assumed by the current implementation but reconsidered (a list that could be a grid; a bottom-anchored CTA that could be inline; a formal tone that could be conversational).
- **Degrees of freedom**: Dimensions along which the design could meaningfully vary.

Be explicit about what you're holding fixed and why.

## Step 3: Select Meaningful Variation Axes

Select 2–3 axes that produce the most meaningfully different outcomes. The five axis categories:

- **Structural**: Layout, information hierarchy, component decomposition, navigation pattern. Answers: "What if this were organized differently?" (e.g., settings as scrolling form vs. tabbed panel vs. progressive wizard)
- **Content / Semantic**: What's foregrounded, backgrounded, or reframed. Answers: "What if we emphasized different things?" (e.g., pricing that leads with features vs. social proof vs. comparison)
- **Conceptual**: The underlying metaphor or interaction paradigm. Answers: "What if we thought about this differently?" (e.g., file manager as spatial desktop vs. conversation vs. timeline)
- **Behavioral**: State transitions, progressive disclosure, interaction sequencing. Answers: "What if it behaved differently?" (e.g., form validates on blur vs. submit vs. inline)
- **Aesthetic**: Color, typography, spacing, mood, material quality. Answers: "What if it looked and felt different?" (e.g., three distinct visual identities for the same card component)

### Selection Heuristic

Read the user's intent to determine where they are in the exploration funnel:

- **"Generate variations" / "show me options" (no further context)**: The user hasn't specified an axis. Analyze the component to determine which axes have the most unexplored space. For structurally complex components (pages, flows, dashboards), default to structural and conceptual axes. For visually-driven or structurally simple components (cards, heroes, buttons, marketing sections), structural AND aesthetic are both strong first-round choices — lead with whichever produces more meaningfully different outcomes.
- **User describes a direction but not a form** ("something more premium," "more playful," "feels enterprise"): This is an aesthetic/tonal signal. Explore visual treatment as a primary axis, but pair it with one structural or content axis so the variations aren't just reskins.
- **User names a specific axis** ("try different layouts," "what if the copy were different"): Follow their lead. Pair with one complementary axis that might surface unexpected possibilities.
- **User is iterating on an established structure** ("I like this layout, but..."): Focus on aesthetic and behavioral refinement.

The goal is progressive funnel narrowing: broad exploration → emerging preferences → focused refinement → final form. Match axis selection to where the user actually is, not to a fixed priority order.

## Step 4: Compose the Design Brief

Compose a structured brief covering: component analysis, constraints (with rationale), chosen variation axes (with rationale), and concrete variation specifications. Each variation spec should name the design hypothesis it represents and describe concretely how it differs from the current implementation.

This brief — not just the file path — is what you pass to the design subagent. The brief is the primary artifact of this skill.

## Step 5: Delegate with the Brief

Your delegation message to the design subagent must include:

1. The full design brief from Step 4
2. The source file path(s)
3. This instruction: "Each variation should be a distinct design hypothesis. Do not produce variations that differ only in color, font, or spacing unless the brief specifically calls for aesthetic exploration."

**Do not just pass the file path. Do not say "generate 3 variations of this component" without the brief.**

## Communicating with the User

### Before generation

Tell the user what axes you chose to explore and why. Name the design concepts at play so the user builds vocabulary over time. This makes your reasoning legible and gives the user a chance to redirect.

Example: "I'm going to explore 3 variations of your pricing section. The current design uses a **comparison table** — that's a strong structural choice, so I'll hold it. Instead I'll vary the **content hierarchy** (what information leads the user's eye and shapes their first impression) and the **conceptual framing** (whether the tiers are positioned as good/better/best, or as use-case-based recommendations). These are often the highest-leverage dimensions for pricing — small changes in what's foregrounded can significantly shift conversion."

If the user redirects, update the axis selection and re-delegate. The comprehension step doesn't need to repeat.

### After generation

When presenting variations, explain what each one teaches about the design problem — not just what it looks like. Frame each variation as a hypothesis with observable trade-offs:

- Name the **design decision** each variation embodies ("This one foregrounds social proof because...")
- Call out the **trade-off** it makes ("...which builds trust at the cost of information density")
- Suggest **what to watch for** when evaluating ("Notice how your eye moves differently across these — that's the hierarchy at work")

The goal is for the user to finish the exploration knowing *more about their design problem* than when they started — not just having picked a favorite variant.

## Anti-Patterns

- **Skipping comprehension**: Going from request to generation without analysis. This always produces shallow output.
- **Producing variations that answer the same question**: If all 3 variations are different visual treatments of the same layout with the same content hierarchy, you've generated 1 hypothesis with 3 skins.
- **Treating the brief as optional**: If you skip the brief, you've skipped the skill. The brief is the reasoning. Generation is downstream.

```

---

## Skill: diagnostics

**Path:** `.local/skills/diagnostics/SKILL.md`

```markdown
---
name: diagnostics
description: Access LSP diagnostics and suggest project rollback. Use for debugging static errors and helping users revert changes.
---

# Diagnostics Skill

Tools for debugging code issues and managing project state.

## When to Use

Use this skill when:

- Checking for syntax errors, type errors, or import issues after code changes
- User wants to undo changes or revert to a previous state
- Debugging static errors detected by the language server

## When NOT to Use

- Runtime errors or logic bugs (use logs and debugging)
- Small changes that don't need LSP validation
- Code search (use grep/glob tools)

## Available Functions

### getLatestLspDiagnostics(filePath=None)

Retrieve LSP diagnostics - syntax errors, type errors, and code issues.

**Parameters:**

- `filePath` (str, optional): File path to check. If omitted, checks all files with errors.

**Returns:** Dict with `diagnostics` (file paths to error lists) and `filePath` (filter used)

**Example:**

```javascript
// Check specific file after editing
const result = await getLatestLspDiagnostics({ filePath: "src/auth.ts" });
for (const [path, errors] of Object.entries(result.diagnostics)) {
    for (const error of errors) {
        console.log(`Line ${error.startLine}: ${error.message}`);
    }
}

// Check all files for errors
const allErrors = await getLatestLspDiagnostics();
console.log(`Files with errors: ${Object.keys(allErrors.diagnostics)}`);
```

**When to check LSP:**

- After refactoring >100 lines of code
- User reports "errors" or "something's not working"
- After adding imports or dependencies
- Before completing a task with >100 lines of changes

**Skip LSP when:**

- Making small changes (<10 lines)
- Adding comments or documentation
- Debugging runtime errors (LSP won't show these)

### suggestRollback(reason)

Suggest rolling back to a previous checkpoint.

**Parameters:**

- `reason` (str, required): Short, non-technical explanation for why rollback is suggested

**Returns:** Dict with `success`, `message`, and `reason`

**Example:**

```javascript
await suggestRollback({ reason: "The changes caused unexpected errors across multiple files" });
```

**Use when user expresses intent to:**

- Undo changes: "can you undo what you just did?", "revert the last changes"
- Restore previous version: "roll back", "go back to how it was yesterday"
- Fix major error: "you deleted my database!", "everything is broken"
- Try different approach: "take a completely different approach", "start over"

**Important:**

- This does NOT perform the rollback - it shows a "View Checkpoints" button
- After calling, direct the user to click the button that appears
- This pauses the agent to wait for user response

## Best Practices

1. **Check LSP after significant changes**: Large refactors, new features, or when user reports errors
2. **Use filePath parameter**: When checking a specific file you just edited
3. **Suggest rollback carefully**: Only when user clearly wants to undo or revert

## Example Workflows

### Debugging after refactoring

```javascript
// After making code changes
const errors = await getLatestLspDiagnostics({ filePath: "src/services/user.ts" });
if (Object.keys(errors.diagnostics).length > 0) {
    // Fix each error
    for (const [path, diags] of Object.entries(errors.diagnostics)) {
        for (const diag of diags) {
            console.log(`Fix: ${diag.rendered}`);
        }
    }
}
```

### Helping user undo changes

```javascript
// User: "Everything broke, can you undo this?"
await suggestRollback({ reason: "Recent changes caused errors. Click View Checkpoints to restore a working version." });
```

```

---

## Skill: environment-secrets

**Path:** `.local/skills/environment-secrets/SKILL.md`

```markdown
---
name: environment-secrets
description: Manage environment variables and secrets. View, set, delete env vars and request secrets from users.
---

# Environment Secrets Skill

Manage environment variables and secrets (such as API keys, tokens, and credentials). View, set, delete environment variables and request secrets from users.

The user can also change the values of any environment variables/secrets using the "secrets" tab in the Replit GUI.

## When to Use

Use this skill when:

- You need to check what environment variables or secrets exist
- Setting sensitive configuration values (ports, hostnames, feature flags)
- Deleting obsolete environment variables
- Requesting API keys, tokens, or other secrets from the user

## When NOT to Use

- Never set sensitive values directly (API keys, passwords, tokens) - always use `requestEnvVar` to request from user
- Don't modify runtime-managed variables (REPLIT_DOMAINS, REPL_ID, DATABASE_URL for Helium DBs)

## Environment Types

Environment variables are scoped to specific environments:

- **shared**: Available in both development and production
- **development**: Only available in development environment
- **production**: Only available in production environment

By default, you should use the 'shared' environment to store environment variables unless there is a clear reason why it would require different values in development and production.

An environment variable stored in the 'shared' environment can not be modified in 'development' or 'production' environments. To modify it, delete it from the 'shared' environment and re-add it to 'development' and 'production' environments.

Secrets are global and not environment-scoped.

## Available Functions

### viewEnvVars(type, environment, keys)

View environment variables and/or secrets.

**Parameters:**

- `type` (str, default "all"): What to view: "env", "secret", or "all"
- `environment` (str, optional): Filter by environment: "shared", "development", "production"
- `keys` (list[str], optional): Filter by specific keys

**Returns:** Dict with `envVars`, `secrets`, and `runtimeManaged` fields

**Example:**

```javascript
// View all env vars and secrets
const result = await viewEnvVars();
console.log(result.envVars);  // {shared: {PORT: '3000'}, development: {...}}
console.log(result.secrets);   // {OPENAI_API_KEY: true, STRIPE_KEY: true}

// Check if specific secrets exist
const result2 = await viewEnvVars({ type: "secret", keys: ["OPENAI_API_KEY", "STRIPE_KEY"] });
if (result2.secrets.OPENAI_API_KEY) {
    console.log("OpenAI key is configured");
}

// View only development env vars
const result3 = await viewEnvVars({ type: "env", environment: "development" });
```

### setEnvVars(values, environment)

Set environment variables. Cannot be used for secrets.

**Parameters:**

- `values` (dict[str, str], required): Key-value pairs to set
- `environment` (str, default "shared"): Target: "shared", "development", "production"

**Returns:** Dict with `environment` and `keys` that were set

**Example:**

```javascript
// Set shared config (available in dev and prod)
await setEnvVars({ values: { PORT: "3000", DEBUG: "false" } });

// Set development-only config
await setEnvVars({ values: { LOG_LEVEL: "debug" }, environment: "development" });

// Set production config
await setEnvVars({ values: { LOG_LEVEL: "error" }, environment: "production" });
```

### deleteEnvVars(keys, environment)

Delete environment variables.

**Parameters:**

- `keys` (list[str], required): Keys to delete
- `environment` (str, default "shared"): Target: "shared", "development", "production"

**Returns:** Dict with `environment` and `keys` that were deleted

**Example:**

```javascript
// Delete from shared environment
await deleteEnvVars({ keys: ["OLD_CONFIG", "DEPRECATED_FLAG"] });

// Delete from specific environment
await deleteEnvVars({ keys: ["DEBUG"], environment: "development" });
```

### requestEnvVar(requestType, keys, envVars, userMessage)

Request secrets or environment variables from the user. This pauses agent execution until the user provides the values.

**Parameters:**

- `requestType` (str, required): "secret" or "env"
- `keys` (list[str], required if requestType="secret"): Secret keys to request
- `envVars` (list[dict], required if requestType="env"): Env vars with `key` and `environment`
- `userMessage` (str, optional): Custom message for user

**Returns:** Dict with `requested`, `userMessage`, and `waitingForInput`

**Example - Request secrets:**

```javascript
// Request API keys from user
await requestEnvVar({
    requestType: "secret",
    keys: ["OPENAI_API_KEY", "STRIPE_SECRET_KEY"],
    userMessage: "Please provide your API keys to enable the payment feature"
});
// Agent pauses here until user provides the secrets
```

**Example - Request env vars:**

```javascript
// Request non-sensitive config from user
await requestEnvVar({
    requestType: "env",
    envVars: [
        { key: "CUSTOM_DOMAIN", environment: "production" },
        { key: "FEATURE_FLAG", environment: "shared" }
    ],
    userMessage: "Please provide the following configuration values"
});
```

## Best Practices

1. **Check before requesting**: Always use `viewEnvVars` first to see what's already configured
2. **Use shared for common config**: Put variables needed in both dev and prod in "shared"
3. **Never hardcode secrets**: Always request secrets from users via `requestEnvVar`
4. **Provide helpful messages**: Include context when requesting secrets so users know why they're needed
5. **Handle conflicts**: If you need to move a var between environments, delete from old first

## Example Workflow

```javascript
// 1. Check current configuration
const result = await viewEnvVars();

// 2. Check if required secrets exist
const missingSecrets = [];
for (const key of ["OPENAI_API_KEY", "DATABASE_URL"]) {
    if (!result.secrets[key]) {
        missingSecrets.push(key);
    }
}

// 3. Request missing secrets from user
if (missingSecrets.length > 0) {
    await requestEnvVar({
        requestType: "secret",
        keys: missingSecrets,
        userMessage: "The following API keys are needed for the chat feature"
    });
} else {
    // 4. Set non-sensitive config
    await setEnvVars({
        values: {
            CHAT_ENABLED: "true",
            MAX_TOKENS: "4096"
        }
    });
}
```

## Restrictions

- Cannot view secret values (only existence status)
- Cannot set or modify secrets directly
- Cannot modify runtime-managed variables
- Variables cannot exist in both "shared" and a specific environment simultaneously

```

---

## Skill: external_apis

**Path:** `.local/skills/external_apis/SKILL.md`

```markdown
---
name: external_apis
description: "Access external APIs through Replit-managed billing"
---

# External APIs

This skill provides access to external APIs through Replit-managed
passthrough billing. Requests are proxied through OpenInt with
managed credentials.

## Recommended workflow

1. Open the connector reference for request and response details.
2. Call `externalApi__<connector_name>` from `code_execution`.
3. Use `query` for URL parameters and parse `result.body`.
4. For media URLs, save files under `attached_assets/` and present them.

## Available APIs

- [Brave](references/brave.md) - Search real web image results through Brave passthrough billing.

```

---

## Skill: fetch-deployment-logs

**Path:** `.local/skills/fetch-deployment-logs/SKILL.md`

```markdown
---
name: fetch-deployment-logs
description: Fetch and analyze deployment logs for the current Repl. Use when the user's published/deployed app isn't working, the live site is down or showing errors, or they ask to check production logs. Covers requests like "my app isn't loading", "my site is broken after publishing", "why isn't my deployed app working", or "check what's happening in production".
---

# Deployment Logs Skill

Fetch and analyze deployment logs to debug issues and monitor your deployed application.

## When to Use

Use this skill when the user:

- Reports that their deployed application is not working correctly
- Wants to see what errors are occurring in production
- Needs to debug a deployment failure or runtime issue
- Asks to check deployment or server logs
- Wants to monitor application behavior after deployment

## How to Use

In the JavaScript notebook, call the `fetchDeploymentLogs` function:

```javascript
const result = await fetchDeploymentLogs({
    afterTimestamp: (Date.now() - 3600 * 1000),  // Last hour
    message: "ERROR"
});
if (result.found) {
    console.log(result.logs);
} else {
    console.log("No deployment logs found.");
}
```

## Parameters

- `afterTimestamp` (float, optional): Only include logs after this Unix timestamp (milliseconds)
- `beforeTimestamp` (float, optional): Only include logs before this Unix timestamp (milliseconds)
- `message` (str, optional): RE2 regular expression to filter logs by message content
- `messageContext` (dict, optional): Context configuration for regex matches with:
  - `lines` (int, required): Number of lines before/after each match (0-100)
  - `limit` (int, required): Max matches to fetch context for (1-10)

## Return Value

Returns a dictionary with:

- `logs`: String containing the formatted deployment logs (empty string if none found)
- `found`: Boolean indicating whether any logs were found
- `message`: Optional message when no logs are found

## Best Practices

1. **Start broad, then filter**: First fetch logs without filters to understand what's available, then use `message` regex to narrow down
2. **Use timestamps for recent issues**: If the user reports a recent issue, use `afterTimestamp` to focus on recent logs
3. **Filter by log level**: Use message regex like `"ERROR"` or `"WARN"` to find problematic entries
4. **Look for patterns**: Search for specific error messages, stack traces, or module names
5. **Use context for debugging**: When investigating specific errors, use `messageContext` to see surrounding log lines (similar to `grep -C`)

## Examples

### Fetch All Recent Logs

```javascript
const result = await fetchDeploymentLogs();
console.log(result.logs);
```

### Fetch Logs from Last Hour

```javascript
const oneHourAgo = Date.now() - 3600 * 1000;  // Convert to milliseconds
const result = await fetchDeploymentLogs({ afterTimestamp: oneHourAgo });
if (result.found) {
    console.log(result.logs);
}
```

### Find Error Logs

```javascript
const result = await fetchDeploymentLogs({ message: "ERROR" });
if (result.found) {
    console.log(result.logs);
} else {
    console.log("No error logs found");
}
```

### Find Database-Related Errors

```javascript
const result = await fetchDeploymentLogs({
    message: "(?i)(database|postgres|mysql|mongo|connection.*refused)"
});
console.log(result.logs);
```

### Find Startup Failures

```javascript
const result = await fetchDeploymentLogs({
    message: "(?i)(failed|crash|exception|traceback)"
});
console.log(result.logs);
```

### Find Errors with Context Lines

```javascript
// Get 10 lines of context before/after each error (up to 3 matches)
const result = await fetchDeploymentLogs({
    message: "ERROR",
    messageContext: { lines: 10, limit: 3 }
});
if (result.found) {
    console.log(result.logs);
}
```

### Combined Time and Pattern Filter

```javascript
// Get logs from the last 30 minutes containing errors
const thirtyMinAgo = Date.now() - 1800 * 1000;
const result = await fetchDeploymentLogs({
    afterTimestamp: thirtyMinAgo,
    message: "(?i)(error|exception|failed)"
});
if (result.found) {
    console.log(result.logs);
} else {
    console.log("No matching logs in the last 30 minutes");
}
```

## Common Log Patterns to Search For

- **Any errors**: `"ERROR"`
- **Warnings and errors**: `"(WARN|ERROR)"`
- **Database issues**: `"(?i)database|postgres|mysql|connection"`
- **Network errors**: `"(?i)timeout|refused|unreachable"`
- **Authentication**: `"(?i)auth|token|unauthorized|forbidden"`
- **Memory issues**: `"(?i)memory|heap|oom|killed"`
- **Import/module errors**: `"(?i)import|module|cannot find"`

## Troubleshooting Tips

1. **No logs returned**: The deployment may not have run recently, or there may be no logs matching your filter
2. **Too many logs**: Use the `message` parameter to filter, or narrow the time range
3. **Looking for specific errors**: Use case-insensitive regex with `(?i)` prefix

```

---

## Skill: integrations

**Path:** `.local/skills/integrations/SKILL.md`

```markdown
---
name: integrations
description: Search and manage Replit integrations including blueprints, connectors, and connections. Use for authentication, databases, payments, and third-party API integrations.
---

# Integrations Skill

Integrations allow first-class usage of Third-Party (and some First-party) technologies. If the integration exists, you can ask user to "connect" their account (Google, Linear, GitHub, Stripe, etc) to their Replit account, which critically gives you, the Replit Agent, access to new capabilities (e.g. view their Google Sheets, read their Linear issues, setup & access payment systems, etc). You must follow the  steps outlined here to successfully make these "connections".

**Before asking the user for any API key, secret, or credential, always search for a Replit integration first.** Replit integrations handle OAuth and secrets securely, and many common services (Google Sheets, Linear, Stripe, GitHub, OpenAI, etc.) are already supported. Asking the user for credentials when an integration exists adds a lot of unnecessary friction. Users typically do not know about our integration system, you must proactive in suggesting it when it (and only when) it is relevant.

Integrations include blueprints (code templates), connectors (OAuth/API integrations + templates), and connections (already established integrations).

## When to Use

Use this skill when:

- User needs authentication (login, signup, OAuth)
- User needs database connections (PostgreSQL, MongoDB, etc.)
- User needs payment processing (Stripe, etc.)
- User needs third-party API integrations (OpenAI, Notion, GitHub, Linear, etc.)
- User asks about Replit-specific features and capabilities

## When NOT to Use

As a web search (use web-search skill if available), searching files within the project, media generation (use media-generation skill, including image generation APIs), fetching data to respond to a user's question (use query-integration-data skill).

---

## Integration Lifecycle

There are three types of integrations, and they represent different stages of a lifecycle:

```text
connector (not_setup)
    → user completes OAuth via proposeIntegration
    → connection (not_added)
        → addIntegration        ← wires the connection to this project, adds dependencies
        → proposeIntegration    ← establishes the OAuth token for this Repl
        → now it is a functioning connection (added + authorized, ready to use)

blueprint (not_installed)
    → addIntegration or proposeIntegration
    → blueprint (installed, code + packages added to project), ready to use
```

### Connectors

- An available OAuth/API integration that has **not yet been authorized** by the user
- Status: `not_setup`
- Cannot be added directly — must use `proposeIntegration` which allows the user through the OAuth flow
- Example ID: `connector:ccfg_google-sheet_E42A9F6DA6...`

### Connections

- A connector that has **already been authorized** (OAuth completed) on the user's Replit account, by them or a teammate
- Status: `not_added` (authorized but not wired to this project) or `added` (active in this project)
- Use `addIntegration` first to wire the connection to this project, then call `proposeIntegration` to establish the OAuth token for this Repl. Both steps are required on first setup. The token may also expire later — see Common Pitfalls.
- When `searchIntegrations` returns a `connection` for a service, it means the user has already completed OAuth at the account level — but you still need `addIntegration` to wire the project, then `proposeIntegration` to establish the OAuth token for this Repl
- Example ID: `connection:conn_linear_01MG99PAJR6MQ5...`

NOTE: You must not delay calling proposeIntegration even if it waits for the user. You will be blocked and not have access to test the feature you build because you don't have access to real data, real APIs, etc, which is even more inefficient than reaching out to the user as soon as you know you need the integration to get accepted.

### Blueprints

- These are just code templates that install packages and scaffold integration boilerplate
- Status: `not_installed` or `previously_installed`
- Use `addIntegration` directly; if `requiresConfirmation` is True, use `proposeIntegration` instead
- Example ID: `blueprint:javascript_openai`

---

## Available Functions

All functions are available directly in the `code_execution` sandbox. **Always use `console.log()` on return values** — functions execute silently with no output if you don't.

### searchIntegrations(query)

Search for available integrations. **Always run this first.** Try a few different query terms if the first search returns nothing — results depend on keyword matching.

**Returns:** Dict with:

- `integrations`: list of integration objects, each with `id`, `displayName`, `description`, `integrationType`, `status`
- `askForBlueprintConfirmation`: boolean — if True, blueprint additions in this environment will require user confirmation; expect `requiresConfirmation: True` back from `addIntegration` and be ready to call `proposeIntegration` instead

```javascript
const results = await searchIntegrations("Google Sheets");
console.log(results);
// { integrations: [{ id: 'connector:ccfg_google-sheet_...', displayName: 'Google Sheets',
//   description: '...', integrationType: 'connector', status: 'not_setup' }], ... }

// Always log — calling without console.log produces no visible output!
for (const item of results.integrations) {
  console.log(`${item.id}  type=${item.integrationType}  status=${item.status}`);
}
```

**Notes:**

- When the user has not explicitly requested a specific provider, at least search with a generic, capability-focused query to ensure all relevant options are returned. For example, when user asks "build an icon generating app", prefer `searchIntegrations("image generation")` instead of `searchIntegrations("OpenAI image generation")`
- If a connector has already been authorized by the user or a teammate, it will appear as a `connection` (not a `connector`) in results
- Try multiple queries if needed: `"stripe"`, `"payments"`, `"stripe payment processing"` may return different results
- The `id` field is the exact string to pass to subsequent functions

---

### viewIntegration(integrationId)

Fetch full details and the code snippet for an integration without adding it to the project.

**Returns:** Dict with `integrationType`, `integrationId`, `displayName`, `renderedContent`

**Note:** `addIntegration` returns the exact same `renderedContent` blob, so in most cases you don't need to call this separately — just read the result of `addIntegration`. The main reason to call `viewIntegration` first is if you want to inspect the package name, code snippet, or documentation URL before committing to the install.

```javascript
const info = await viewIntegration("connection:conn_linear_01KG10PAJR6MQ525SQSWEB8QHC");
console.log(info.renderedContent);  // Same blob you'd get from addIntegration
```

---

### addIntegration(integrationId)

Add a blueprint or connection to the current project. **Do not use for connectors** (those with `integrationType: connector` and `status: not_setup`) — use `proposeIntegration` for those.

**Returns:** Dict with:

- `success`: boolean
- `requiresConfirmation`: boolean — if True, call `proposeIntegration` instead
- `connectionAlreadyAdded`: boolean — if True, the connection is already wired to this project; skip addIntegration but still call proposeIntegration to ensure the OAuth token is valid
- `renderedContent`: same XML blob as `viewIntegration`
- `observations`: list of stringified observation objects (verbose; contains npm install output)

**Side effect:** Automatically installs required packages. This will restart or crash a running dev server — be aware if calling mid-session while the workflow is running.

```javascript
const result = await addIntegration("connection:conn_linear_01KG10PAJR6MQ525SQSWEB8QHC");
console.log(result.success);       // true
console.log(result.observations);  // Contains package installation output as stringified objects

// Handle confirmation requirement
if (!result.success && result.requiresConfirmation) {
  proposeIntegration("connection:conn_linear_01KG10PAJR6MQ525SQSWEB8QHC");
}
```

**After calling addIntegration:**

- Read `renderedContent` to get the code snippet
- The snippet handles token refresh and expiry — use it as-is, don't simplify it
- Never cache the client object the snippet creates — tokens expire

---

### proposeIntegration(integrationId)

Propose a connector to the user. This is a **control-flow operation** — it exits the agent loop immediately and waits for the user to complete OAuth or confirm setup. Nothing after this call will execute in the current loop.

**Returns:** Dict with `success`, `displayName`, `exitLoop` (always True)

**Use for:**

- Connectors with `status: not_setup` (user needs to go through OAuth)
- Blueprints where `addIntegration` returns `requiresConfirmation: True`

```javascript
// Always explain to the user what is about to happen before calling this
// The agent loop exits after this — no further code runs
const result = await proposeIntegration("connector:ccfg_google-sheet_E42A9F6CA62546F68A1FECA0E8");
```

**Notes:**

- After the user completes OAuth, the connector becomes a `connection`
- On the next agent loop, call `addIntegration` with the new `connection:...` ID
- There is no user-visible message automatically shown when this exits — explain what you're doing in your chat response before calling it

---

## Using the Code Snippet

After `addIntegration` or `viewIntegration`, the `renderedContent` contains a code snippet. Key things to know:

1. **It is not on the filesystem.** Copy it into a new file in your project (e.g., `server/googleSheets.ts`)
2. **Never cache the client.** Tokens expire. The snippet exports a `getUncachable___Client()` function — call it fresh on every request
3. **The token refresh logic is correct as-is.** Don't simplify or remove the expiry check
4. **The snippet uses environment variables** (`REPLIT_CONNECTORS_HOSTNAME`, `REPL_IDENTITY`, `WEB_REPL_RENEWAL`) that Replit injects automatically — no setup needed

---

## Common Pitfalls

- **Not logging results:** `searchIntegrations` and all other functions return silently unless you `console.log()` the output
- **Calling addIntegration on a connector:** Will fail or behave unexpectedly. Check `integrationType` first
- **Asking for API keys when a connection exists:** If `searchIntegrations` returns a `connection`, the user is already authenticated at the account level — use `addIntegration` to wire the project, then `proposeIntegration` to establish the OAuth token for this Repl. Both steps are always required
- **Caching the client:** The boilerplate snippet is explicit about this. Tokens expire. Always call `getUncachable___Client()` fresh
- **Package install side effects:** `addIntegration` runs package installation (e.g. npm, uv), which can crash a running dev server. Restart the workflow after adding integrations
- **Connection added but runtime still fails:** If `addIntegration` succeeds for a `connection` but the app throws "not connected" at runtime, the token may be expired or missing. Call `proposeIntegration` with the same connection ID to trigger re-authorization, then restart the workflow

```

---

## Skill: media-generation

**Path:** `.local/skills/media-generation/SKILL.md`

```markdown
---
name: media-generation
description: Generate and retrieve media including AI-generated images, AI-generated videos, and stock images. Use this skill for all visual content creation and retrieval.
---

# Media Generation Skill

Generate custom images, videos, and retrieve stock images for your application.

## Available Functions

### generateImage(images, ...)

Generate custom images from text descriptions using AI image generation. Waits for generation to complete before returning.

**Parameters:**

- `images` (list, **required**): A list of image request objects. **This wrapper is always required — even for a single image, pass `images: [{ ... }]`**. Up to 10 images can be generated in a single call. Each dict should have:
  - `prompt` (required): Text description of the desired image
  - `outputPath`: File path **must end in `.png`** — this is the only accepted format. `.jpg`, `.jpeg`, `.webp`, and other extensions will cause an error. Defaults to `attached_assets/generated_images/{summary}.png`
  - `aspectRatio`: Optional, defaults to "1:1". Options: "1:1", "3:4", "4:3", "9:16", "16:9"
  - `negativePrompt`: Optional, description of what should NOT appear
  - `summary`: Optional, short 4-5 word description for default filename
  - `removeBackground`: Optional, defaults to False
- `overwrite` (bool, default True): Whether to overwrite existing files

**Returns:** Dict with `images` list (each with `filePath` and `description`) and optional `failures` list

**Common Mistakes:**

```javascript
// WRONG — flat params without images array (causes "images field required" error)
await generateImage({ prompt: "A mountain landscape", outputPath: "hero.png" });

// CORRECT — always wrap in images: [...], even for a single image
await generateImage({ images: [{ prompt: "A mountain landscape", outputPath: "hero.png" }] });

// WRONG — .jpg extension is not supported (causes "outputPath must end with .png" error)
await generateImage({ images: [{ prompt: "A cityscape", outputPath: "city.jpg" }] });

// CORRECT — only .png is accepted
await generateImage({ images: [{ prompt: "A cityscape", outputPath: "city.png" }] });
```

**Examples:**

```javascript
// Single image
const result = await generateImage({
    images: [
        {
            prompt: "A serene mountain landscape at sunset with snow-capped peaks",
            outputPath: "src/assets/images/hero.png",
            aspectRatio: "16:9",
            negativePrompt: "blurry, low quality",
        }
    ]
});
console.log(`Image saved to: ${result.images[0].filePath}`);

// Multiple images at once
const result = await generateImage({
    images: [
        { prompt: "A red apple", outputPath: "assets/apple.png" },
        { prompt: "A yellow banana", outputPath: "assets/banana.png" },
        { prompt: "An orange", outputPath: "assets/orange.png", removeBackground: true },
    ]
});
for (const img of result.images) {
    console.log(`Generated: ${img.filePath}`);
}
```

### generateImageAsync(images, ...)

Generate images asynchronously in the background. Returns immediately with a workflow ID.

**Parameters:**

- `images` (list, required): Same format as `generateImage`
- `overwrite` (bool, default True): Whether to overwrite existing files

**Returns:** Dict with `workflowId`, `workflowAlias`, `status`, and `imagePaths`

**Example:**

```javascript
const result = await generateImageAsync({
    images: [
        { prompt: "A complex detailed illustration", outputPath: "assets/illustration.png" },
    ]
});
console.log(`Started workflow: ${result.workflowAlias}`);
console.log(`Images will be saved to: ${result.imagePaths}`);
```

### generateVideo(prompt, ...)

Generate short video clips from text descriptions using AI video generation.

**Parameters:**

- `prompt` (str, required): Detailed text description of the desired video
- `summary` (str, default "generated_video"): Short description for the filename
- `aspectRatio` (str, default "16:9"): "16:9" (landscape) or "9:16" (portrait)
- `resolution` (str, default "720p"): "720p" or "1080p"
- `durationSeconds` (int, default 6): 4, 6, or 8 seconds
- `negativePrompt` (str, optional): Description of what should NOT appear
- `personGeneration` (str, optional): "dont_allow" or "allow_adult" for controlling people

**Returns:** Dict with `filePath` and `description` keys

**Example:**

```javascript
const result = await generateVideo({
    prompt: "A cat playing with a ball of yarn, cute and playful, natural lighting",
    summary: "playful cat",
    aspectRatio: "16:9",
    durationSeconds: 6
});
console.log(`Video saved to: ${result.filePath}`);
```

### generateVideoAsync(prompt, ...)

Generate a video asynchronously in the background. Returns immediately with a workflow ID.

**Parameters:**

- `prompt` (str, required): Detailed text description of the desired video
- `summary` (str, default "generated_video"): Short description for the filename
- `aspectRatio` (str, default "16:9"): "16:9" (landscape) or "9:16" (portrait)
- `resolution` (str, default "720p"): "720p" or "1080p"
- `durationSeconds` (int, default 6): 4, 6, or 8 seconds
- `negativePrompt` (str, optional): Description of what should NOT appear
- `personGeneration` (str, optional): "dont_allow" or "allow_adult" for controlling people

**Returns:** Dict with `workflowId`, `workflowAlias`, `status`, and `videoPath`

**Example:**

```javascript
const result = await generateVideoAsync({
    prompt: "A cat playing with a ball of yarn, cute and playful, natural lighting",
    summary: "playful cat",
    aspectRatio: "16:9",
    durationSeconds: 6
});
console.log(`Started workflow: ${result.workflowAlias}`);
console.log(`Video will be saved to: ${result.videoPath}`);

// Later, wait for completion
await wait_for_background_tasks({ wait_mode: "all" });
```

### stockImage(description, ...)

Retrieve stock images matching a description from a stock image provider.

**Parameters:**

- `description` (str, required): Text description of desired stock image(s)
- `summary` (str, default "stock_image"): Short description for the filename
- `limit` (int, default 1): Number of images to retrieve (1-10)
- `orientation` (str, default "horizontal"): "horizontal", "vertical", or "all"

**Returns:** Dict with `filePaths` list and `query` string

**Example:**

```javascript
const result = await stockImage({
    description: "modern office with natural lighting",
    summary: "office background",
    limit: 3,
    orientation: "horizontal"
});
for (const path of result.filePaths) {
    console.log(`Stock image saved to: ${path}`);
}
```

## When to Use Each Function

### generateImage / generateImageAsync

- Custom illustrations or graphics not available elsewhere
- Specific visual concepts or designs
- Placeholder images for development
- Creative or artistic content
- Use `generateImageAsync` when images are not needed immediately

### generateVideo / generateVideoAsync

- Use `generateVideoAsync` when the video is not needed immediately
- Short animated clips or motion graphics
- Video backgrounds or visual effects
- Product animations or demonstrations
- Social media video content

### stockImage

- Professional photography
- Real-world scenes and people
- Business and corporate imagery
- When authenticity is more important than customization

## Aspect Ratio Guidelines

### Images

- **1:1** - Square, good for profile pictures, thumbnails, icons
- **3:4** - Portrait, good for mobile screens, product images
- **4:3** - Landscape, good for presentations, desktop displays
- **9:16** - Vertical, good for mobile stories, tall banners
- **16:9** - Widescreen, good for hero images, video thumbnails

### Videos

- **16:9** - Widescreen landscape, good for web videos, presentations
- **9:16** - Vertical portrait, good for mobile stories, social media shorts

## Best Practices

1. **Write detailed prompts**: Include style, mood, lighting, colors, and composition
2. **Use negative prompts**: Exclude unwanted elements like "blurry", "watermark", "text"
3. **Choose appropriate formats**: Match aspect ratio and media type to intended use
4. **Consider stock for realism**: Use stock images when you need authentic photography
5. **Do not over generate**: Do not over generate images in one user request unless explicitly requested by the user

## Output Locations

- Generated images: `attached_assets/generated_images/`
- Generated videos: `attached_assets/generated_videos/`
- Stock images: `attached_assets/stock_images/`

## Limitations

- Generated videos are limited to 8 seconds maximum
- Stock image availability depends on the search query
- Complex or highly specific prompts may not match exactly
- Text in generated media is not reliably rendered

## Copyright

- Always use this skill to create media assets rather than copying from websites
- Generated images and videos are created for your use
- Stock images are licensed for use in your projects
- Do not download or copy media files directly from external websites

```

---

## Skill: mockup-extract

**Path:** `.local/skills/mockup-extract/SKILL.md`

```markdown
---
name: mockup-extract
description: "Use when the user wants to pull an existing component from their main app onto the canvas — whether to redesign it, create variants, or simply display it as a visual reference. Also activate when the user asks to redesign, improve, or create variants of any UI that already exists as code in the main app, even if they don't explicitly say 'extract' — the real source code must be used as the starting point, never hand-coded approximations. Copies the component and its dependencies into the mockup sandbox, rewrites imports, stubs external dependencies, and embeds the result as an iframe on the canvas. Activate when the user says 'put my X on the canvas', 'show my current Y on the board', 'redesign my existing Z', 'create variants of my current W', 'improve my Y', or wants to see or iterate on something already in the app."
---

# Mockup Extract Skill

Pull an existing component from the main app into the `mockup/` sandbox so it can be previewed on the canvas and used as a starting point for design iteration.

## When to Use

Activate this skill when the user:

- Wants to see an existing component on the canvas as a visual reference ("show my homepage on the board", "put my current settings page on the canvas")
- Wants to redesign an existing component ("redesign my navbar", "redo my pricing page", "improve the onboarding flow")
- Wants to create variants starting from an existing component
- Needs to compare their current design against new alternatives

**Important:** This skill must also be activated implicitly when the user asks to redesign, improve, or create variants of something that already exists as code in the main app — even if they don't say "extract". If the component exists in the codebase, extract it first. Never rebuild an existing component from scratch by hand-coding approximations; you will get exact dimensions, colors, spacing, opacity values, and other details wrong. The real source code has the correct values.

## Subagent Guidance

If you need to parallelize extraction (e.g., extract multiple components at once), use a **GENERAL** subagent — never a DESIGN subagent. Extraction is an engineering task (import graph tracing, dependency stubbing, path rewriting) that requires codebase navigation, not creative visual output.

## Prerequisites

The mockup sandbox must be set up first. If `mockup/` doesn't exist, activate the {{skill("mockup-sandbox")}} skill to set it up before proceeding.

## Do Not Iframe the Main App Directly

When the user asks to "show my component on the canvas" or "redesign my navbar," do **not** create an iframe pointing at the main app's dev server URL. This is the wrong approach because:

- It shows the entire app (navbar, sidebar, footer, routing), not the target component in isolation
- You cannot create independent design variants from it
- Clicking links or buttons inside the iframe navigates away from the component
- Editing the main app code changes the iframe live, making it impossible to compare before/after

Instead, always extract the component into the `mockup/` sandbox and embed the sandbox's `/preview/` URL.

## Process

### Step 1: Locate and read the target component

Ask the user which component to extract if it isn't clear. Read the component file and understand its structure and imports.

### Step 2: Analyze the dependency tree

Read the target component and trace every import. Classify each dependency:

| Category | When | Action |
|---|---|---|
| **Inline** | Small sub-components, simple hooks, utility functions (<50 lines) | Copy the code directly into the mockup file |
| **Copy** | Larger shared components, complex hooks, asset files | Copy into `mockup/src/` with updated import paths |
| **Stub** | Context providers, API calls, routing, auth, global state | Replace with static mock data or no-op wrappers |

Walk the full import chain -- a component may import a hook that imports a context that imports an API client. Trace until you reach leaf dependencies or hit a stub boundary.

### Step 3: Handle external dependencies

For dependencies that can't transfer cleanly:

- **API calls / data fetching:** Replace with hardcoded mock data matching the response shape. Use realistic values.
- **Context providers (auth, theme):** Inline the values as constants.
- **Routing (`useNavigate`, `Link`, `useParams`):** Replace with no-ops or static values.
- **Global state (Redux, Zustand):** Extract the relevant slice as a local `useState` or constant.

### Step 4: Rewrite import paths

`@/` resolves to different roots in the main app vs the sandbox:

- Main app: `@/` → `client/src/`
- Sandbox: `@/` → `mockup/src/`

Every `@/` import must point to a file that exists under `mockup/src/`. If the imported file doesn't exist in the sandbox, either copy it there or inline it. `@/components/ui/*` imports work without changes (shadcn/ui is pre-installed).

### Step 5: Create `_group.css` and the mockup component

The main app's global styles are invisible to Step 2's import trace — they live in `index.html` `<link>` tags and global CSS, not in any `import` statement. Collect them into a group-level stylesheet that every component in this group will explicitly import.

Create `mockup/src/components/mockups/{group}/_group.css` with everything the app applies globally:

- **CSS variables** — copy the `:root` and `.dark` blocks from the main app's `client/src/index.css` so semantic classes like `bg-background` and `text-foreground` resolve to the app's values, not the sandbox defaults.
- **External font links** — read the main app's `client/index.html` for `<link href="https://fonts.googleapis.com/...">` (or Adobe Fonts, etc.) and convert each to `@import url("...");` at the top of `_group.css`.
- **`@font-face` declarations** — if the main app self-hosts fonts, copy the `@font-face` blocks and the font files they reference.

Do **not** edit the sandbox's global `index.css` — that leaks this app's tokens into every unrelated mockup group. Do **not** add font `<link>` tags to `mockup/index.html` — that file is shared across all mockup groups, so app-specific fonts would load for every unrelated preview. The sandbox already pre-loads a large common font bundle there; put any additional app-specific fonts in `_group.css` via `@import` to keep them scoped to this extraction.

Then create `mockup/src/components/mockups/{group}/Current.tsx`:

```tsx
import './_group.css';

export function Current() {
  // ... extracted component
}
```

The `_group.css` import loads after the plugin's base `index.css` import, so its rules win by normal cascade order. Every variant you create later (`VariantA.tsx`, `VariantB.tsx`) also imports `./_group.css` to inherit the same baseline. A variant that needs to diverge adds a second import for its own sibling CSS file.

Use a descriptive group name (e.g., `navbar-redesign/`). Export a single component per file; named or default exports both work. Use `min-h-screen` on the root element.

### Step 6: Type-check, embed, and create variants

Type-check with `cd mockup && npm run check`. Embed on the canvas using the sandbox `/preview/` URL (see {{skill("mockup-sandbox")}} for iframe creation). Label it "Current", then create new variant files alongside it.

## Guidelines

- **Prefer inlining over copying.** Fewer files = easier iteration. Inline anything under ~50 lines.
- **Keep mock data realistic.** Visual fidelity depends on it.
- **Don't import from the main app.** Every import must resolve within `mockup/src/`.
- **Preserve the visual output exactly.** The extracted component should look identical to the original.
- **Copy assets first.** Images and icons must exist in `mockup/` before the component references them.

## Common Mistakes

- **Leaving `@/` imports pointing to main app files.** Every `@/` path must resolve under `mockup/src/`.
- **Forgetting nested dependencies.** Trace the full import chain — component → hook → context → API client.
- **Not stubbing side effects.** API calls, analytics, and router navigations will crash in the sandbox.
- **Copying too much.** Extract only what the target component needs.
- **Editing the global `index.css` instead of creating `_group.css`.** The extraction's tokens leak into every other mockup group in the sandbox.
- **Forgetting `import './_group.css'` in the component file.** Without it the component renders with sandbox defaults, not the app's tokens. No error — it just looks wrong.
- **Adding font `<link>` tags to `mockup/index.html`.** That file is shared across all mockup groups — app-specific fonts leak into every unrelated preview. Put fonts in `_group.css` via `@import` instead to keep them scoped to this group.
- **Assuming fonts loaded because nothing errored.** Missing fonts fall back silently — no console error, no build failure. The component still renders, just with the wrong stroke weight, character width, and spacing. Verify typography visually against the original; "it didn't crash" is not "it looks right."

```

---

## Skill: mockup-graduate

**Path:** `.local/skills/mockup-graduate/SKILL.md`

```markdown
---
name: mockup-graduate
description: "Use when the user approves a mockup on the canvas and wants it integrated into their main app. Reads the approved mockup component, analyzes the main app's patterns, transforms the mockup to match, installs dependencies, and verifies the integration. Activate when the user says 'use this one', 'put this in my app', 'I like variant B, integrate it', 'graduate this mockup', or approves a design for production."
---

# Mockup Graduate Skill

Move an approved mockup from the mockup sandbox (`mockup`) into the main app. Transform the self-contained prototype into production code that matches the app's conventions.

## When to Use

Activate this skill when the user:

- Approves a mockup variant ("I like this one", "go with the bold version")
- Asks to integrate a mockup ("put this in my app", "use this design")
- Wants to graduate a prototype to production
- Says "ship it" or "let's go with this"

## Subagent Guidance

If you need to parallelize graduation (e.g., graduate multiple pages at once), use a **GENERAL** subagent — never a DESIGN subagent. Graduation is an engineering task (understanding app architecture, transforming mockup code to production patterns, wiring routing and state) that requires codebase navigation, not creative visual output.

## Prerequisites

- The mockup sandbox must be running ({{skill("mockup-sandbox")}})
- The user must have identified which mockup to graduate (if multiple variants exist, ask which one)

## Process

### Step 1: Identify the approved mockup

Confirm which mockup the user wants. Read the mockup component file and extract key design decisions: colors, gradients, shadows, typography, layout approach, icons, and animations.

### Step 2: Analyze the main app's patterns

Understand how the main app handles routing, state management, data fetching, styling, and component structure. Read a few existing components to understand conventions.

### Step 3: Plan the transformation

Map each part of the mockup to the main app's equivalent:

| Mockup | Main App |
|---|---|
| Hardcoded mock data | API call or data hook |
| Inline sub-components | Existing shared components where they exist |
| Direct `className` styling | App's styling approach (may be the same) |
| `@/components/ui/*` (sandbox shadcn) | App's UI component library (may differ) |
| Static images from `mockup/` | App's asset directory or CDN |

### Step 4: Install missing dependencies

Compare the mockup's imports against the main app's `package.json`. Install anything missing using the `packager_install_tool`. Add font links to `index.html` if needed.

### Step 5: Transform and place the component

Create the production component in the main app. Replace mock data with real data fetching, wire up navigation, connect to app state, and adapt UI components to the app's library. Copy any assets from `mockup/` to the main app's asset directory.

### Step 6: Update routing and verify

Add a route if the graduated component is a new page. If it replaces an existing component, update the import. Run the main app's linter, restart the workflow, and confirm it renders correctly.

### Step 7: Clean up (optional)

Ask the user if they want to remove the graduated mockup from the sandbox, keep it for reference, or remove the canvas iframes. Don't clean up automatically.

## When Graduation Is Complex

Most graduations are straightforward — just proceed. Only pause and check with the user when the main app uses a fundamentally different design system than the mockup (requiring a full visual translation), or when the graduation would require a complete refactor of the existing backend to support the new design.

## What to Preserve

These elements from the mockup should transfer exactly to production:

- **Visual design:** Colors, gradients, shadows, border radius, spacing
- **Typography:** Font families, weights, sizes, line heights
- **Layout:** Grid/flex structure, responsive breakpoints, spacing
- **Animations:** Transitions, hover states, entry animations
- **Icons:** Same icon library and icon choices

## What to Transform

These elements need adaptation for production:

- **Data:** Static mock data → real API calls or state
- **Navigation:** No-op handlers → real router navigation
- **State:** Local constants → app state management
- **Auth:** Stubbed user objects → real auth context
- **Error handling:** Add loading states, error boundaries, empty states
- **Accessibility:** Add ARIA labels, keyboard navigation, focus management

## Common Mistakes

- **Losing visual fidelity during transformation.** Ship what was approved — don't "improve" the design during graduation.
- **Forgetting loading and error states.** Mockups show the happy path. Production needs skeletons, error messages, and empty states.
- **Not checking the UI component library.** If the main app uses different components than shadcn/ui, translate — don't just copy imports.
- **Breaking existing functionality.** If replacing an existing component, ensure all existing features still work.
- **Skipping responsive behavior.** If the mockup was designed at a single viewport, ensure it works at other breakpoints.

```

---

## Skill: mockup-sandbox

**Path:** `.local/skills/mockup-sandbox/SKILL.md`

```markdown
---
name: mockup-sandbox
description: "Use when the user wants to create, preview, or iterate on any web UI content on the canvas. This is the only way to show live rendered components on the board — all other canvas shapes are static. Activate for: designing or prototyping components on the canvas, comparing design variants side-by-side, showing responsive previews (mobile/tablet/desktop), previewing component states (loading/error/empty), comparing dark vs light mode, or any request that involves putting rendered web content on the board. Sets up a vite dev server with isolated component preview URLs for iframe embedding. For variant exploration (2+ design alternatives), includes subagent orchestration patterns for parallelizing work with DESIGN subagents. Never embed the main app URL directly — always use this skill. Read the entire skill carefully — it contains critical path conventions, image handling rules, and subagent delegation patterns that cause silent failures when skipped. For two specific workflows, also activate the companion skill: use mockup-extract when the user wants to pull an existing component from the main app onto the canvas, and mockup-graduate when the user approves a mockup and wants it integrated into the main app."
---
# Mockup Sandbox Skill

The **`artifacts/mockup-sandbox/`** folder is an isolated frontend sandbox for rapid UI prototyping. Components are rendered in isolation via a vite dev server, and each component gets a `/preview/ComponentName` route that can be embedded as an iframe shape on the workspace canvas.

## When to Use

Activate this skill when the user wants to:

- Show any web UI component on the canvas ("create a card on the canvas", "put a form on the board")
- Prototype or mockup a design ("design a landing page", "mockup a dashboard")
- Compare design variants side-by-side ("show me 3 options for the hero section")
- Preview responsive behavior ("how does this look on mobile?", "show me mobile and desktop")
- Preview component states ("show me loading, error, and empty states")
- Compare themes ("dark mode vs light mode", "what about a warmer color scheme?")
- Show a multi-page flow, **only when the user explicitly requests multiple pages** ("preview the signup flow: landing → signup → dashboard")
- Iterate on an existing component's design on the canvas (also activates mockup-extract)

**Rule of thumb:** if the result should be rendered HTML/CSS/React on the canvas, use this skill. If it's just shapes, text, or diagrams, the canvas skill handles it directly.

## Extract First, Then Iterate

**When the user wants to redesign, improve, or create variants of something that already exists in their app, always start by extracting the real component code** using {{skill("mockup-extract")}}. Never rebuild an existing component from scratch by hand-coding approximations — you will get dimensions, colors, spacing, icon sizes, opacity values, and other details wrong. The real source code has the exact values; use them.

The correct workflow for redesigning existing UI:

1. **Extract** the real component into the mockup sandbox (preserves exact values)
2. **Label it "Current"** on the canvas as the baseline
3. **Duplicate and modify** to create design variants

The incorrect workflow (do not do this):

1. ~~Look at the app and hand-code a simplified version from memory~~
2. ~~Guess at dimensions, colors, spacing, and other values~~
3. ~~Iterate on an inaccurate approximation~~

This applies whenever the component being redesigned already exists as code in the main app — even if the user doesn't explicitly say "extract". If they say "redesign my sidebar", "improve the onboarding flow", or "show me alternatives for the settings page", the code already exists and must be extracted, not approximated.

## Gathering Requirements

If the user's request is vague (e.g., "make some variants", "create a mockup"), ask them to clarify **what specific component or page** they want to prototype. Examples: "a pricing card", "a login form", "a dashboard header", "a product listing".

Once you know what to build, you can proceed and make reasonable decisions about layout, colors, and content.

## How It Works

1. A vite dev server runs in a `artifacts/mockup-sandbox/` folder, separate from the main app
2. A custom Vite plugin (`mockupPreviewPlugin`) uses `fast-glob` and file watching to discover components in `artifacts/mockup-sandbox/src/components/mockups/`
3. The plugin writes a generated component registry at `src/.generated/mockup-components.ts`
4. Each component is served at `/preview/{folder}/{ComponentName}` as a standalone page
5. If a relevant preview request returns 404 before file watching settles, the dev server rescans automatically and the next iframe retry picks up the update
6. Components use Tailwind and shadcn/ui -- changes hot-reload instantly

## Setup

### Step 1: Set up the mockup sandbox

Create the mockup sandbox using `createArtifact` (see {{skill("artifacts")}} for full details):

```javascript
const result = await createArtifact({
    artifactType: "mockup-sandbox",
    slug: "mockup-sandbox",
    previewPath: "/__mockup/",
    title: "Mockup Sandbox"
});
```

Then start its dev server **before** creating any components or placing iframes on the canvas:

```javascript
await restartWorkflow({ workflowName: "artifacts/mockup-sandbox: Component Preview Server" });
```

The dev server must be running first so that component files are picked up by the Vite plugin and preview URLs resolve correctly. Preview URLs use path-based routing: `https://${REPLIT_DOMAINS}/__mockup/preview/{folder}/{ComponentName}` — no port number needed.

### Step 2: Create mockup components

**Verify the component directory first.** Before creating any files, list `artifacts/mockup-sandbox/` to confirm that `src/components/mockups/` exists. Use the verified path for all component creation and subagent delegation.

Create components in `artifacts/mockup-sandbox/src/components/mockups/`:

```tsx
// artifacts/mockup-sandbox/src/components/mockups/pricing-cards/Minimal.tsx
export function Minimal() {
  return (
    <div className="min-h-screen bg-background p-8">
      <h1 className="text-2xl font-bold text-foreground">Basic Plan - $9/mo</h1>
    </div>
  );
}
```

### Step 3: Embed on the canvas

Create `iframe` shapes on the workspace canvas.
Preview URLs follow the pattern `https://${REPLIT_DOMAINS}/__mockup/preview/{folder}/{ComponentName}` — no port number.

Example -- a pricing card is a "Card / Panel", so use a snug iframe (see [Iframe Sizing Guide](#iframe-sizing-guide)):

```json
{
  "type": "create",
  "shapeId": "pricing-minimal",
  "shape": {
    "type": "iframe",
    "x": 100, "y": 100, "w": 500, "h": 450,
    "url": "https://<your-domain>.replit.dev/__mockup/preview/pricing-cards/Minimal",
    "componentPath": "artifacts/mockup-sandbox/src/components/mockups/pricing-cards/Minimal.tsx",
    "componentName": "Minimal Pricing Card"
  }
}
```
### Step 4: Layout and focus

Before embedding iframes, call `get_canvas_state` to see what already exists on the board and find empty space. Then place your iframes in an unoccupied region.

If an iframe is created while the workflow is still booting, rely on the canvas host's iframe retry behavior plus the dev server's automatic 404 rescan to recover. Do not ask the user to refresh the whole board.

**Variant grid layout.** Arrange multiple variants in a horizontal row with ~50px gutters. Do not add text labels above iframes -- the iframe title bar already shows the `componentName`. Use descriptive `componentName` values instead (e.g. "Minimal Pricing Card", "Bold Pricing Card").

**Multi-viewport layouts.** When showing the same component at different screen sizes, place them in a row using the viewport presets (Mobile: 390x844, Tablet: 768x1024, Desktop: 1280x720) with ~50px gutters.

**Offer to show after embedding.** After creating all iframe shapes, tell the user what you placed and ask if they'd like you to focus on the new layout. Don't auto-focus -- moving the viewport while the user is working is disorienting. When the user confirms, call `focus_canvas_shapes` with all new shape IDs and `animate_ms: 500`.

**Do not call `suggestDeploy()`.** The mockup sandbox is a local prototyping tool and is not meant to be deployed — if the user asks to publish or deploy canvas/mockup content, integrate/graduate it into a real app artifact first.

**Never share dev domain URLs in chat.** Dev URLs (`*.replit.dev`, `$REPLIT_DEV_DOMAIN`) are internal — use them only in tool calls (iframe shapes, subagent tasks), never in user-facing messages.

**Present the artifact.** After all mockups are embedded and the workflow is running, look up the artifact and present it so the user can see it in the preview pane:

```javascript
// Present the completed mockup artifact in the preview pane so the user can view and interact with it.
await presentArtifact({ artifactId });
```
/*
- This function reveals the live mockup canvas to the user.
- Call this after embedding all mockup iframes and finishing workflow setup.
- artifactId should be the ID of the registered mockup-sandbox artifact.
*/
```

## Architecture

```text
artifacts/mockup-sandbox/                              # Isolated from main app
├── package.json                      # Dependencies (React, Tailwind, shadcn/ui, cartographer)
├── vite.config.ts                    # Vite config
├── mockupPreviewPlugin.ts            # Vite plugin for component discovery + automatic 404 rescan
├── tsconfig.json                     # TypeScript config for tsgo type checking
├── components.json                   # shadcn/ui config
├── .npmrc
├── index.html
└── src/
    ├── main.tsx                      # Entry point
    ├── App.tsx                       # Landing page
    ├── index.css                     # Tailwind v4 styles
    ├── .generated/
    │   └── mockup-components.ts      # Auto-generated component registry
    ├── components/
    │   ├── ui/                       # 50+ shadcn/ui components (pre-installed)
    │   └── mockups/                  # YOUR MOCKUP COMPONENTS GO HERE
    ├── lib/
    │   └── utils.ts
    └── hooks/
```

## Folder Structure

The folder structure in `mockups/` automatically organizes components:

```text
components/mockups/
├── pricing-cards/           # Single-component variants
│   ├── _group.css           # Group-level tokens + fonts (optional)
│   ├── Minimal.tsx          # imports './_group.css'
│   ├── Bold.tsx             # imports './_group.css'
│   └── Gradient.tsx         # imports './_group.css'
├── crm-dashboard/           # Multi-page project (only when user explicitly requests multiple pages)
│   ├── _shared/             # Shared layout (not preview targets)
│   │   ├── AppLayout.tsx
│   │   ├── Navbar.tsx
│   │   └── Sidebar.tsx
│   ├── _group.css
│   ├── Dashboard.tsx
│   ├── UserList.tsx
│   └── Settings.tsx
├── login-forms/
│   ├── Simple.tsx
│   └── Dark.tsx
└── QuickIdea.tsx            # Ungrouped (loose files)
```

Files prefixed with `_` are not preview targets by convention. `_shared/` holds helper components imported by sibling page files. `_group.css` holds group-level CSS overrides — tokens, font `@import`s, `@font-face` blocks — that every component in the group explicitly imports (see [Fonts](#fonts)).

## Working with Assets

### Icons

`lucide-react` is pre-installed with 1000+ icons:

```tsx
import { ShoppingCart, Star, ArrowRight } from "lucide-react";

<ShoppingCart className="w-6 h-6 text-gray-600" />
```

### Images

Two approaches -- **do not mix them**:

#### Option 1: Public folder (URL reference)

Place images in `artifacts/mockup-sandbox/public/images/` and reference by URL path:

```tsx
<img src="/__mockup/images/hero.png" alt="Hero" />
```

#### Option 2: Import via `@/assets/` (bundled by Vite)

Place images in `artifacts/mockup-sandbox/src/assets/` and import them:

```tsx
import heroImg from "@/assets/hero.png";

<img src={heroImg} alt="Hero" />
```

The `@` alias maps to `artifacts/mockup-sandbox/src/`, so `@/assets/hero.png` resolves to `artifacts/mockup-sandbox/src/assets/hero.png`.

**Important — pick one approach per image and do not cross them:**

- Files in `src/assets/` **must** be imported (`import img from "@/assets/hero.png"`). Referencing them by URL path (`<img src="/src/assets/hero.png" />`) will 404 — Vite does not serve `src/` files as static assets.
- Files in `public/images/` are served as-is at `/__mockup/images/…`. Do not import them.

For mockups, **prefer Option 1 (public folder)** — it is simpler and avoids the most common mistake.

To generate images for mockups, use the `media-generation` skill:

```javascript
await generateImage({
    images: [{
        prompt: "Modern product photo of wireless headphones",
        outputPath: "artifacts/mockup-sandbox/public/images/headphones.png",
        aspectRatio: "1:1"
    }]
});
```

Then reference: `<img src="/__mockup/images/headphones.png" />`.

**Path warning:** The `outputPath` must start with `artifacts/mockup-sandbox/public/` -- NOT just `public/`. The main app's public folder is not served by the mockup dev server. Using `outputPath: "public/images/hero.png"` (without the `artifacts/mockup-sandbox/` prefix) will 404 in mockup iframes.

### Fonts

**Bundled fonts.** `index.html` preloads 25+ Google Font families. Use them directly in any component:

```tsx
<h1 className="font-['Playfair_Display']">Heading</h1>
```

**Custom fonts.** For fonts outside the bundled set, add a non-blocking `<link>` tag to `artifacts/mockup-sandbox/index.html`. Do not use CSS `@import url(...)` — it is render-blocking and will delay all Tailwind styles until the font finishes downloading.

```html
<!-- in artifacts/mockup-sandbox/index.html <head> -->
<link rel="stylesheet" media="print" onload="this.media='all'"
      href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&display=swap">
```

Then use it in components:

```tsx
<h1 className="font-['Cormorant_Garamond'] text-6xl">Heading</h1>
```

Or override the default font via a CSS variable in a component's own CSS file:

```css
/* editorial-hero/tokens.css */
:root { --font-serif: 'Cormorant Garamond', serif; }
```

Missing fonts fail silently — no console error, no build failure, just a fallback font with the wrong weight and width. Verify typography visually.

## Adding Packages

The `packager_install_tool` only works for the main project. To add packages to the mockup sandbox:

1. Edit `artifacts/mockup-sandbox/package.json` directly and add the dependency
2. Run `npm install` from the `artifacts/mockup-sandbox/` directory
3. Restart the "artifacts/mockup-sandbox: Component Preview Server" workflow to pick up the change

## shadcn/ui Components

All shadcn/ui components are pre-installed and ready to use:

```tsx
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
```

**Available components:** accordion, alert, alert-dialog, aspect-ratio, avatar, badge, breadcrumb, button, button-group, calendar, card, carousel, chart, checkbox, collapsible, command, context-menu, dialog, drawer, dropdown-menu, empty, field, form, hover-card, input, input-group, input-otp, item, kbd, label, menubar, navigation-menu, pagination, popover, progress, radio-group, resizable, scroll-area, select, separator, sheet, sidebar, skeleton, slider, sonner, spinner, switch, table, tabs, textarea, toast, toaster, toggle, toggle-group, tooltip

## Component Best Practices

- **One preview entry point per file** -- each file should export one top-level component that the preview route resolves as the preview target. But define as many local helper components inside the file as you need -- a `Dashboard.tsx` with internal `StatsCard`, `ActivityFeed`, and `QuickActions` components all composed into one exported `Dashboard` function is ideal. This keeps mockups self-contained and readable without file sprawl.
- **Match the CSS wrapper to the content type** -- see the [Iframe Sizing Guide](#iframe-sizing-guide) for how to pair component CSS with iframe dimensions.
- **Use design tokens for the baseline** -- When recreating the app's existing look or building the "Current" version, use semantic color classes like `bg-background`, `text-foreground`, `text-muted-foreground` so the mockup matches the main app's theme. When creating design variations, use whatever colors express the variant's visual direction -- hardcoded colors like `bg-indigo-950`, `text-amber-200` are expected and necessary. That's the whole point of exploring alternatives.
- **Use realistic data** -- show how the component looks with real content, not lorem ipsum.
- **Name clearly** -- use descriptive names that communicate the variant's design hypothesis (e.g., `ComparisonTable.tsx`, `ProgressiveDisclosure.tsx`, `FeatureLed.tsx`). For simple aesthetic variants, names like `Minimal.tsx` or `DashboardDark.tsx` are fine.
- **Include states** -- create separate mockup files for loading, empty, and error states.

## Design Variation Guidelines

When the user asks for variations, alternatives, "show me options," or any request that implies divergent exploration (e.g., "try 3 different approaches," "what else could this be?"), read {{skill("design-exploration")}} first. It provides a structured comprehension → brief → delegation workflow that produces meaningfully diverse output instead of superficial reskins.

When asked to generate variations, your first task is to **understand the design before changing it**.

### Step 1: Analyze the component

Read the source code and determine:

- **Purpose:** What user need does this component serve? What task does it support?
- **Constraints:** What must stay fixed? (data shape, required actions, accessibility, brand)
- **Degrees of freedom:** What could meaningfully change without breaking the component's purpose?

### Step 2: Select variation axes based on the analysis

Choose 2-3 axes that would give the user the most insight into their solution space. Axes ordered from most impactful to least:

1. **Structural:** Different layouts, information hierarchies, component compositions (e.g., pricing as cards vs. comparison table vs. progressive disclosure)
2. **Content strategy:** What's foregrounded vs. backgrounded, information density, copy approach (e.g., feature-led vs. social-proof-led vs. price-led)
3. **Interaction model:** Different interaction patterns, progressive disclosure, state handling (e.g., modal vs. inline expansion vs. dedicated page)
4. **Conceptual:** The underlying metaphor or mental model (e.g., dashboard-as-cockpit vs. dashboard-as-feed vs. dashboard-as-scorecard)
5. **Visual treatment:** Typography, color, spacing, depth, mood (e.g., minimal vs. bold vs. editorial)

Default to higher-impact axes unless the user specifically requests aesthetic exploration (e.g., "try different color schemes" or "explore visual styles"). For visually-driven or structurally simple components (cards, heroes, buttons), aesthetic variation is a strong first-round choice alongside structural variation.

### Step 3: Generate variations as distinct design hypotheses

Each variation should represent a meaningfully different answer to the question "how should this component work?" Variations should be diverse enough that the user can identify emerging preferences and narrow their direction.

### Process notes

- Functionality and data shape should stay consistent across variants (same API contract)
- Layout, hierarchy, content emphasis, and visual treatment ARE all fair game
- Name variants descriptively by their design hypothesis (e.g., `ComparisonTable.tsx`, `ProgressiveDisclosure.tsx`) not just their aesthetic (e.g., `Bold.tsx`)
- Create each variant as an independent component

## Subagent Orchestration

For design variation tasks (2+ alternatives of the same component or page), use DESIGN subagents to parallelize work. The parent agent orchestrates setup, building placeholders, and canvas layout; subagents handle individual variant creation and mark iframes live when done. Multi-page fan-out (building separate pages in parallel) should only be used when the user explicitly requests multiple pages.

### Building placeholders

Every mockup request -- whether handled directly or via subagents -- should show immediate visual feedback on the canvas using the iframe `state` field. When creating a new iframe for a component that doesn't exist yet, set `state: "building"`. The canvas renders a native building indicator -- no URL is needed at this point.

**Flow for new components (0 → 1):**

1. Read the canvas state to find empty space
2. Immediately place iframe(s) with `state: "building"` and `componentName` at the expected sizes
3. Proceed with component development (direct or via subagents)
4. Once a component is ready, update the iframe with `url`, `componentPath`, and `state: "live"`
5. Restart the workflow once all components are created

**Flow for modifying existing components:**

1. Set `state: "modifying"` on the iframe before editing
2. Edit the component file in place
3. Set `state: "live"` on the iframe when done

**Building iframe example:**

```json
{
  "type": "create",
  "shapeId": "pricing-bold",
  "shape": {
    "type": "iframe",
    "x": 600, "y": 100, "w": 500, "h": 450,
    "state": "building",
    "componentName": "Bold Pricing Card"
  }
}
```

Then once the component is built, set the URL and mark it live:

```json
{
  "type": "update",
  "shapeId": "pricing-bold",
  "updates": {
    "url": "https://<dev-url>/__mockup/preview/pricing-cards/Bold",
    "componentPath": "artifacts/mockup-sandbox/src/components/mockups/pricing-cards/Bold.tsx",
    "state": "live"
  }
}
```

### When to use subagents

Use subagents when the task involves **2+ design variants** of the same component or page. Also use a single DESIGN subagent for any single-page app or full-page mockup (landing pages, homepages, portfolios, etc.) — the DESIGN subagent produces higher-quality visual output, unless the user asks you to handle it yourself. For a single small component (card, button, form) or a modification to an existing mockup, do the work directly.

**Do not create multiple pages unless the user explicitly asks.** When the user says "design a dashboard" or "build a CRM", build it as a single page — do not proactively split it into Dashboard, UserList, Settings, etc. Only fan out into multiple page files when the user specifically requests separate pages (e.g., "design a CRM with dashboard, users, and settings pages").

**Single-page apps are single components.** When the user asks for a landing page, homepage, or any single-page app, create it as **one component file** — do not split sections (hero, features, pricing, footer, etc.) into separate component files or separate screens. A landing page is one scrollable page rendered in one iframe, unless the user explicitly asks for separate screens or sections as independent components. For landing pages and similar content-rich pages, prioritize generating images (hero visuals, product shots, background art, illustrations) — placeholder boxes and generic stock imagery make landing pages look unfinished. Use `generateImage` to create custom visuals that match the page's mood and brand direction.

**Which specialization?** Use **DESIGN** subagents (`specialization: "DESIGN"`) for all mockup creation work. DESIGN subagents are tuned for creative visual output — they produce better, more diverse designs when given a brief mood/direction rather than prescriptive specs. Do not use GENERAL subagents for mockup component creation; they lack the design sensibility and carry unnecessary overhead (task lists, context management).

**For extract and graduate workflows, use GENERAL subagents** if parallelization is needed. These are engineering tasks (import graph tracing, production code transformation) — DESIGN subagents lack the codebase navigation skills they require. See the companion skills for details.

| Scenario | Subagents? | Specialization | Pattern |
| --- | --- | --- | --- |
| "Design a pricing card" | No | — | Direct |
| "Design a landing page" | Yes (1) | DESIGN | Single DESIGN subagent (one file) |
| "Design a single-page app" | Yes (1) | DESIGN | Single DESIGN subagent (one file) |
| "Make the header bigger" | No | — | In-place modification |
| "Extract my existing component" | If parallelizing | GENERAL | Direct or fan-out (mockup-extract) |
| "Graduate / apply this mockup to my app" | If parallelizing | GENERAL | Direct or fan-out (mockup-graduate) |
| "Redesign my navbar with 2 options" | Yes | DESIGN | Variants fan-out |
| "Show me 3 options for the hero" | Yes | DESIGN | Variants fan-out |

### Pattern: Direct (no subagent)

Use for single small components (cards, buttons, forms) or modifications to existing mockups. For single full-page mockups (landing pages, homepages, single-page apps), delegate to a single DESIGN subagent instead — unless the user asks otherwise. Follow the standard setup steps (Steps 3-6), with building placeholders for instant feedback.

```text
Parent: Place iframe(s) with state: "building" on canvas
    → Create component file
    → Restart workflow
    → Update iframe with URL + state: "live"
    → Offer to focus
```

For modifications to existing mockups, set `state: "modifying"` on the iframe, edit the file in place, then set `state: "live"` when done. **Do not** create a new file for modifications. If the user wants to preserve the old version for comparison, *then* duplicate the file into a new variant first.

### Pattern A: Design variants (fan-out)

Use when the user wants multiple visual options for the same component or page.

```text
Parent: Place iframes with state: "building" on canvas (one per variant, in a row)
Parent: Establish requirements, seed each variant direction
    ├──→ DESIGN subagent: "Minimal" variant → set iframe URL + state: "live"
    ├──→ DESIGN subagent: "Bold" variant → set iframe URL + state: "live"
    └──→ DESIGN subagent: "Gradient" variant → set iframe URL + state: "live"
Parent: Restart workflow once all subagents complete
```

**Parent responsibilities:**

1. Run the design-exploration comprehension steps (analyze component, identify constraints, select variation axes) and compose a structured design brief
2. Create the folder (e.g., `mockups/pricing-cards/`)
3. Place iframes with `state: "building"` in a horizontal row on the canvas, one per variant, with stable shape IDs
4. Seed each subagent with: the design brief, target file path, shape ID to update, dev URL, and the specific design hypothesis for this variant and ask it to set the iframe live.
5. After all subagents complete: restart workflow, offer to focus

**Subagent task format:**

```text
Create a mockup component at artifacts/mockup-sandbox/src/components/mockups/pricing-cards/Bold.tsx

## Design Brief

Component analysis: A pricing card that presents a subscription tier to help users
compare plans and choose one. Displays plan name, price, feature list, and a CTA.

Fixed constraints: Must include plan name, monthly price, feature list, and CTA button.
Data shape stays consistent across variants.

Variation axes:
- Content hierarchy (what leads the user's eye)
- Visual treatment (mood and material quality)

## This Variant's Hypothesis

Name: Bold
Hypothesis: High-contrast, large typography, and strong color blocking to create urgency
and confidence. Foregrounds the price as the dominant visual element with features
as supporting evidence.

Each variation should be a distinct design hypothesis. Do not produce variations that
differ only in color, font, or spacing unless the brief specifically calls for
aesthetic exploration.

The exported function name must match the filename: export function Bold().
Use Tailwind + shadcn/ui.

When done, update the canvas iframe to show the real preview:
  Shape ID: pricing-bold
  URL: https://<dev-url>/__mockup/preview/pricing-cards/Bold
  componentPath: artifacts/mockup-sandbox/src/components/mockups/pricing-cards/Bold.tsx
  state: "live"
```

**Parent responsibilities:**

1. Place iframes with `state: "building"` on the canvas with stable shape IDs
2. Create the project folder and `_shared/` subfolder
3. Build shared layout components (`AppLayout.tsx` with a content slot, `Navbar.tsx`, `Sidebar.tsx`, etc.)
4. Fan out DESIGN subagents for each page, passing `_shared/` file paths, shape ID, and dev URL
5. After all subagents complete: restart workflow, offer to focus

**Multi-page subagent task format (only when user explicitly requests multiple pages):**

```text
Create a mockup page at artifacts/mockup-sandbox/src/components/mockups/crm-dashboard/Dashboard.tsx

This is the main dashboard page of a CRM application. Import the shared layout:
  import { AppLayout } from "./_shared/AppLayout";

Wrap your page content inside <AppLayout>. The layout already renders the nav and sidebar --
you only need to build the page content area.

User constraints: Show key metrics (revenue, users, conversion), recent activity feed,
and a quick-actions panel.

The exported function name must match the filename: export function Dashboard().
Use Tailwind + shadcn/ui.

When done, update the canvas iframe to show the real preview:
  Shape ID: crm-dashboard
  URL: https://<dev-url>/__mockup/preview/crm-dashboard/Dashboard
  componentPath: artifacts/mockup-sandbox/src/components/mockups/crm-dashboard/Dashboard.tsx
  state: "live"
```

### Pattern C: Multi-page with multiple variant directions

Use when the user wants to compare multiple complete design directions for a multi-page application ("show me 2 different takes on this CRM").

Each variant gets its own folder with its own `_shared/` components. One DESIGN subagent builds an entire variant (shared components + all pages), giving it full creative control over the design direction.

```text
Parent: Place iframes with state: "building" in a variant × page grid on canvas
Parent: Define page list, seed each variant direction
    ├──→ DESIGN subagent: Build entire crm-minimal/ → set iframe URLs + state: "live"
    ├──→ DESIGN subagent: Build entire crm-bold/ → set iframe URLs + state: "live"
    └──→ DESIGN subagent: Build entire crm-playful/ → set iframe URLs + state: "live"
Parent: Restart workflow once all subagents complete
```

```text
mockups/
├── crm-minimal/
│   ├── _shared/
│   │   ├── AppLayout.tsx
│   │   └── Navbar.tsx
│   ├── Dashboard.tsx
│   ├── UserList.tsx
│   └── Settings.tsx
├── crm-bold/
│   ├── _shared/
│   │   ├── AppLayout.tsx
│   │   └── TopNav.tsx
│   ├── Dashboard.tsx
│   ├── UserList.tsx
│   └── Settings.tsx
```

**Canvas layout for variant × page grids:**

Arrange as a matrix with text label shapes for headers. Variants as rows, pages as columns:

```text
              Dashboard       UserList        Settings
Minimal       [iframe]        [iframe]        [iframe]
Bold          [iframe]        [iframe]        [iframe]
Playful       [iframe]        [iframe]        [iframe]
```

Use `geo` text shapes for row and column headers. Space iframes with ~50px gutters.

**Subagent task format:**

```text
Build a complete multi-page mockup variant at artifacts/mockup-sandbox/src/components/mockups/crm-minimal/

Direction: Minimal and restrained -- lots of whitespace, muted colors, thin borders, subtle typography.

Pages to create: Dashboard.tsx, UserList.tsx, Settings.tsx

First create a _shared/ subfolder with shared layout components (AppLayout, Navbar, Sidebar or
similar). Then create each page file importing from _shared/ for visual consistency.

Each exported function name must match its filename. Use Tailwind + shadcn/ui.

When done, update the canvas iframes to show real previews (set state: "live" on each):
  Shape ID: crm-minimal-dashboard → URL: https://<dev-url>/__mockup/preview/crm-minimal/Dashboard
  Shape ID: crm-minimal-userlist → URL: https://<dev-url>/__mockup/preview/crm-minimal/UserList
  Shape ID: crm-minimal-settings → URL: https://<dev-url>/__mockup/preview/crm-minimal/Settings
```

**Important:** The multi-page pattern above should only be used when the user explicitly requests separate pages. If the user says "design a CRM" or "design a dashboard" without specifying separate pages, build everything as a single page component.

### General orchestration rules

1. **Always place building iframes first.** Before starting any component work, create iframes with `state: "building"` at the expected positions and sizes. No URL is needed yet -- the canvas shows a native building indicator. Skip this only for in-place modifications (set `state: "modifying"` on the existing iframe instead).

2. **Subagents mark their own iframes live.** The parent places building iframes with stable shape IDs, then tells each subagent which shape ID to update and the dev URL to use. Subagents set the real preview URL and `state: "live"` when their component is ready. This gives progressive reveal -- iframes light up as subagents finish, rather than all at once.

3. **Parent restarts the workflow once after all subagents complete** -- not once per subagent. A single restart discovers all new components and the iframes load the real content.

4. **Verify paths before delegating.** Before passing file paths to subagents, list `artifacts/mockup-sandbox/` to confirm `src/components/mockups/` exists and pass the verified full path. Getting this wrong means files land in a directory the Vite plugin never scans.

5. **Tell subagents the image path convention.** Always include this in the subagent task: "Place all images in `artifacts/mockup-sandbox/public/images/` and reference them as `<img src="/__mockup/images/filename.jpg" />`. Do NOT put images in `src/assets/` and reference them by URL path — Vite does not serve `src/` as static assets and they will 404. For `generateImage`, use `outputPath` starting with `artifacts/mockup-sandbox/public/images/`."

6. **Give subagents creative freedom.** Subagents produce better designs when given high-level requirements, not prescriptive specs. Pass:
   - Target file path and exported function name
   - Shape ID + dev URL for iframe update
   - Shared file paths to import (for multi-page projects)
   - Functional requirements only (what the page must contain, not how it should look)
   - A brief mood/direction seed (1-2 words: "minimal", "bold and dark", "warm editorial")

   Do NOT pass specific color values, font choices, spacing values, detailed layout instructions, CSS class names, or references to other variants. The subagent has its own design sensibility -- constraining it to exact specs produces generic results and defeats the purpose of generating diverse alternatives.

   **Exception:** For multi-page apps (only when the user explicitly requests multiple pages), the parent defines the design system in `_shared/` and the subagent works within it. Creative freedom applies to page content and layout, not the shared chrome.

7. **Match specialization to the task type.** Use `DESIGN` for creative mockup creation (building new components, designing variants) — it's tuned for visual output and produces better, more diverse designs. Use `GENERAL` for engineering tasks (extract, graduate) — it's built for codebase navigation, dependency tracing, and architecture-aware transformations. Never use DESIGN for extract/graduate or GENERAL for mockup creation.

## Related Skills

- **{{skill("mockup-extract")}}** -- Pull an existing component from the main app into the sandbox for redesign. Use when the user wants to iterate on something that already exists.
- **{{skill("mockup-graduate")}}** -- Move an approved mockup into the main app. Use when the user picks a variant and wants it integrated.

## Iframe Sizing Guide

Size the iframe to fit the content -- a landing page needs a full desktop viewport, a button needs a compact frame. Classify what you're building and pick dimensions accordingly.

### Content-aware sizing

Size the iframe to fit the content. A full page needs a desktop-sized viewport; a button or card needs a compact frame. Don't put small components in huge iframes -- they'll look lost in whitespace. For cards, forms, and small components, center them with `flex items-center justify-center min-h-screen` and use a snug iframe. For page sections, skip `min-h-screen` and let content determine the height.

### Full-page mockups

For landing pages and multi-section pages, use larger iframe dimensions:

- **Landing page (desktop):** 1280 × 900 -- shows hero + start of next section, user scrolls within iframe
- **Landing page (full):** 1280 × 2400 -- shows entire page without scrolling (screenshot-style review)
- **Multi-page app (desktop):** 1280 × 800 -- standard app viewport
- **Multi-page app (mobile):** 390 × 844 -- iPhone viewport

When comparing full landing pages side-by-side, use 1280 × 900 and arrange horizontally with 50px gutters. The user scrolls within each iframe to see the full page.

### Responsive comparison presets

When showing the **same component** at multiple screen widths, use these standard viewport sizes and arrange them in a row with ~50px gutters:

- Mobile: 390 × 844
- Tablet: 768 × 1024
- Desktop: 1280 × 720

## Common Pitfalls

### Keep mockups self-contained

Each mockup component must be fully self-contained. Prefer inlining small sub-components (nav bars, footers, cards) directly in the mockup file rather than importing from elsewhere. This keeps mockups isolated and editable without risk of breaking other variants.

**Exception: multi-page `_shared/` imports.** For multi-page projects (only when the user explicitly requests multiple pages — see [Subagent Orchestration](#subagent-orchestration)), pages import shared layout components from their sibling `_shared/` folder. This is intentional -- the shared shell ensures visual consistency across pages. The rule still applies within each page: don't import from other project folders or from other pages.

### No variant switchers inside components

Mockups are displayed as individual iframes on the canvas -- the canvas itself is the variant switcher. Do not build tabs, dropdowns, or navigation inside a mockup component to switch between variants. Each variant should be its own file rendered in its own iframe.

### Sync design tokens with the main app

When extracting existing components, create `_group.css` in the extraction's group folder with the main app's `:root` and `.dark` CSS variable blocks plus any font `@import`s the app uses. Each extracted component imports `./_group.css` explicitly. Do not edit the global `artifacts/mockup-sandbox/src/index.css` — that would leak one app's tokens into every unrelated mockup group in the sandbox. See the {{skill("mockup-extract")}} skill for the full process.

### Fixing broken previews

If a mockup shows a blank iframe or fails to render:

1. Check the workflow console logs for `Failed to resolve import` errors.
2. Verify the missing file exists under `artifacts/mockup-sandbox/src/` (not the main app).
3. Ensure the file exports at least one function component (named or default).
4. Restart the workflow if you changed `vite.config.ts` or `package.json`.


```

---

## Skill: package-management

**Path:** `.local/skills/package-management/SKILL.md`

```markdown
---
name: package-management
description: Install and manage language packages, system dependencies, and programming language runtimes.
---

# Package Management Skill

Manage project dependencies and programming language runtimes. Use this skill instead of running shell commands like `npm install`, `pip install`, or `apt install`.

## When to Use

Use this skill when you need to:

- Install language-specific packages (npm, pip, cargo, etc.)
- Install system-level dependencies (ffmpeg, jq, imagemagick, etc.)
- Install programming language runtimes (Python, Node.js, etc.)
- Remove packages from the project
- Check available versions of a programming language

## When NOT to Use

- Searching for available packages (use web search instead)
- Configuring package settings (edit config files directly)
- Running package scripts (use bash tool)

## Modules (Replit Terminology)

"Modules" is a Replit-specific term for language toolchains that can be installed into the NixOS environment. Use `listAvailableModules()` to see what's available.

**Installation priority order:**

1. Modules via this skill (preferred)
2. Nix system dependencies via `installSystemDependencies()`
3. Language package managers (pip, npm, cargo, etc.) via `installLanguagePackages()`

If confused about package installation in Nix or language package managers, use web search.

**After installing a module:**

- Update `.gitignore` with the language's standard ignore patterns
- Never add Replit config files to `.gitignore`

**After removing a module:**

- Consider removing any corresponding workflows that depend on it

## Available Functions

### listAvailableModules(langName=None)

List available language toolchains that can be installed.

**Parameters:**

- `langName` (str, optional): Language name to filter by (e.g., "python", "nodejs", "rust"). If not provided, returns all available modules.

**Returns:** Dict with `success`, `message`, `langName`, and `modules` list

Each module contains: id, name, version, description

**Example:**

```javascript
// List all available modules
const modules = await listAvailableModules();
// Returns: {modules: [{id: "python-3.11", ...}, {id: "nodejs-20", ...}, ...]}

// Find available Python versions
const pythonModules = await listAvailableModules({ langName: "python" });
// Returns: {modules: [{id: "python-3.11", name: "Python", version: "3.11", ...}, ...]}

// Find available Node.js versions
const nodeModules = await listAvailableModules({ langName: "nodejs" });
```

### installProgrammingLanguage(language)

Install a programming language runtime and its package manager.

**Parameters:**

- `language` (str, required): Language identifier like "python-3.11", "nodejs-20"

**Returns:** Dict with `success`, `message`, `language`, and `installedModuleId` keys

**Example:**

```javascript
// First, check available versions
const modules = await listAvailableModules({ langName: "python" });
console.log(modules);  // See available Python versions

// Install specific version
const result = await installProgrammingLanguage({ language: "python-3.11" });

// Install Node.js 20
const result2 = await installProgrammingLanguage({ language: "nodejs-20" });
```

### uninstallProgrammingLanguage(moduleId)

Remove an installed programming language runtime.

**Parameters:**

- `moduleId` (str, required): Module ID from `listAvailableModules`

**Returns:** Dict with `success`, `message`, `moduleId`, and `wasInstalled`

**Example:**

```javascript
// Remove Python 3.10
const result = await uninstallProgrammingLanguage({ moduleId: "python-3.10" });
```

### installLanguagePackages(language, packages)

Install language-specific packages like npm, pip, or cargo packages.

**Parameters:**

- `language` (str, required): Programming language: "nodejs", "python", "bun", "go", "rust"
- `packages` (list[str], required): List of packages to install

**Returns:** Dict with `success`, `message`, `packages`, and `output` keys

**Example:**

```javascript
// Install npm packages
const result = await installLanguagePackages({
    language: "nodejs",
    packages: ["express", "lodash"]
});
console.log(result.message);

// Install pip packages
const result2 = await installLanguagePackages({
    language: "python",
    packages: ["requests", "flask"]
});
```

**IMPORTANT — required parameter rules:**

- `language` is **required** — you must always include it
- Valid language values: `"nodejs"`, `"python"`, `"bun"`, `"go"`, `"rust"`
  - Use `"nodejs"` for JavaScript/TypeScript projects — NEVER use `"js"`, `"node"`, or `"javascript"`
  - Use `"python"` for Python projects — NEVER use `"py"` or `"pip"`
- `packages` must be an **array of strings** — NEVER a single string, NEVER an array of objects
  - Correct: `packages: ["express"]`
  - Wrong: `packages: "express"`
  - Wrong: `packages: [{name: "express"}]`

### uninstallLanguagePackages(language, packages)

Remove language-specific packages.

**Parameters:**

- `language` (str, required): Programming language
- `packages` (list[str], required): List of packages to uninstall

**Returns:** Dict with `success`, `message`, and `packages` keys

**Example:**

```javascript
const result = await uninstallLanguagePackages({
    language: "nodejs",
    packages: ["lodash"]
});
```

### installSystemDependencies(packages)

Install system-level dependencies via Nix.

**Parameters:**

- `packages` (list[str], required): Nixpkgs attribute paths (NOT apt package names)

**Returns:** Dict with `success`, `message`, and `packages` keys

**Important:** Use Nix package names, not apt/debian names:

- X11 libraries need 'xorg.' prefix: `xorg.libxcb`, `xorg.libX11`
- `ca-certificates` is `cacert` in Nix
- `libxcb` is `xorg.libxcb` in Nix

**Example:**

```javascript
// Install system dependencies
const result = await installSystemDependencies({
    packages: ["jq", "ffmpeg", "imagemagick"]
});

// Install X11 libraries (note the xorg. prefix)
const result2 = await installSystemDependencies({
    packages: ["xorg.libxcb", "xorg.libX11"]
});
```

### uninstallSystemDependencies(packages)

Remove system-level dependencies.

**Parameters:**

- `packages` (list[str], required): Nixpkgs attribute paths to uninstall

**Returns:** Dict with `success`, `message`, and `packages` keys

**Example:**

```javascript
const result = await uninstallSystemDependencies({ packages: ["jq"] });
```

## Best Practices

1. **Use language packages for project dependencies**: These are tracked in package files (package.json, requirements.txt)
2. **Use system dependencies for OS-level tools**: Things like ffmpeg, imagemagick, or native libraries
3. **Use Nix package names**: Not apt/debian names. Check nixpkgs for correct names
4. **Install language runtimes when needed**: If `python` or `node` commands fail, install the runtime first
5. **Check versions first**: Use `listAvailableModules` before `installProgrammingLanguage`

## Example Workflow

```javascript
// Check available Python versions
const modules = await listAvailableModules({ langName: "python" });
console.log(modules);

// Set up a Python Flask project
await installProgrammingLanguage({ language: "python-3.11" });
await installLanguagePackages({
    language: "python",
    packages: ["flask", "gunicorn", "sqlalchemy"]
});

// Set up a Node.js project with native dependencies
await installProgrammingLanguage({ language: "nodejs-20" });
await installLanguagePackages({
    language: "nodejs",
    packages: ["sharp", "canvas"]
});
await installSystemDependencies({
    packages: ["pkg-config", "cairo", "pango", "libjpeg"]
});

// Clean up old language version
await uninstallProgrammingLanguage({ moduleId: "python-3.10" });
```

## Automatic Behaviors

- Installing packages automatically creates/updates project files (package.json, requirements.txt, etc.)
- Package installations reboot all workflows to pick up new dependencies
- Language runtime installations include popular package managers (pip, npm, etc.)

```

---

## Skill: post_merge_setup

**Path:** `.local/skills/post_merge_setup/SKILL.md`

```markdown
---
name: post_merge_setup
description: Maintain the post-merge setup script that runs automatically after task merges.
---

# Post-Merge Setup

After a task is merged, two things run automatically:

1. Setup script — installs dependencies, runs migrations, rebuilds.
2. Workflow reconciliation — stops workflows removed from `.replit` and restarts already running workflows.

If either step fails, the agent will be alerted about the issue, and should fix it immediately.

## What Runs Automatically

The system runs the configured post-merge script from the project root with bash.
Stdin is closed (`/dev/null`), so commands that prompt for input will get EOF and fail immediately. The full Nix environment is available on PATH.

If the script does not exist, setup fails and you are asked to create it.

The script has a configurable timeout. If the script takes longer, it is killed and setup fails with a timeout error.

After the script, workflow reconciliation syncs running workflows with the current `.replit` config.

## Available Commands

### Get the post-merge config

```javascript
const config = await getPostMergeConfig();
console.log(config);
// { scriptPath: "...", timeoutMs: ... }
```

Returns the configured script path and timeout from `.replit`. If not yet configured, both fields will be `null`.

### Set post-merge config

```javascript
await setPostMergeConfig({ scriptPath: "scripts/post-merge.sh", timeoutMs: 180000 });
```

Sets the post-merge script path and/or timeout. Both parameters are optional — only provided values are updated. Note: `scriptPath` must be set (either already configured or provided in the same call) before setting `timeoutMs` alone, because `.replit` requires `path` in the `[postMerge]` section. Use `timeoutMs` when:

- The script timed out — if the script naturally takes a long time (large `npm install`, slow migrations), increase the timeout so it succeeds on the next merge. Estimate a reasonable value from the script's expected runtime and add a buffer (e.g. if `npm install` takes 3s, set timeout to 5000 ms).
- The script hangs — if the script hangs due to a bug (e.g. waiting for input), fix the script first, then consider lowering the timeout to catch future hangs early.

### Run post-merge setup

```javascript
const result = await runPostMergeSetup();
console.log(result);
```

Runs the post-merge script and workflow reconciliation. Returns `{ success, setupError, reconciliationError, scriptPath, stdoutPath, stderrPath, durationMs, timeoutMs }`.

- `setupError` / `reconciliationError`: what failed
- `scriptPath`: path to the post-merge script that was executed
- `stdoutPath` / `stderrPath`: full log file paths
- `durationMs` / `timeoutMs`: how long it ran and the configured timeout

The tail of the stdout/stderr log files (last 10 lines with line numbers) is automatically opened into your context after the call.

## Fixing Failures

When setup fails:

1. **Check the log files** opened into your context after the call (last 10 lines of stdout/stderr with line numbers). The `scriptPath` in the result tells you which script was executed.
2. **Fix the script** — create it if missing, update it if broken.
3. **If it timed out**, increase the timeout with `setPostMergeConfig({ timeoutMs: ... })` based on how long the script actually needs.
4. **Retry** with `runPostMergeSetup()` to confirm the fix works.

If workflow reconciliation fails, use the workflows skill to check and restart affected workflows.

Common failure causes:

- Missing script -> use the `scriptPath` from the result (or call `getPostMergeConfig()`) to find the expected path, then create the script there.
- Script timed out -> increase timeout with `setPostMergeConfig({ timeoutMs: ... })`, or optimize the script.
- A command prompts for input (stdin is closed, so it gets EOF and fails) -> use non-interactive flags (`--yes`, `--force`, `-y`, etc.).
- A dependency or migration command fails -> fix the command or the underlying config.

## Writing the Post-Merge Script

Use the `scriptPath` from the last `runPostMergeSetup()` result if available. Otherwise, call `getPostMergeConfig()` to find the script location.

Example:

```bash
#!/bin/bash
set -e

pnpm install
pnpm --filter @workspace/db run push-force
```

Guidelines:

- Idempotent. Safe to run multiple times.
- Non-interactive. Stdin is closed. Use `--yes` / `--force` flags.
- Fail fast. Use `set -e`.
- Keep it fast. Runs while the user waits. If it takes more than 2 minutes, consider optimizing or increasing the timeout.

```

---

## Skill: project_tasks

**Path:** `.local/skills/project_tasks/SKILL.md`

```markdown
---
name: project_tasks
description: Create and manage persistent project tasks visible to the user.
---

# Project Tasks

Manage persistent, user-visible project tasks that can be handed to the
main agent or to a task agent. Only task agents run in isolated
environments. Use these to track high-level deliverables and milestones
that the user cares about.

## Project Tasks vs Internal Task List

| Aspect | Project Tasks | Internal Task List |
|--------|--------------|-------------------|
| Purpose | User-visible deliverables | Agent's own work breakdown |
| Persistence | Persistent across sessions (PID2) | Current session only |
| Visibility | Shown to the user | Internal to the agent |
| Granularity | High-level milestones | Detailed implementation steps |

## When to Use

- Tracking user-requested features or deliverables
- Breaking a project into visible milestones
- Communicating progress to the user
- Managing tasks that persist across sessions

## When NOT to Use

- Internal agent work breakdown (use the internal task list)
- Temporary implementation steps
- Sub-tasks that only matter to the agent

## Task Identifiers

Tasks are identified by `taskRef` — a short string like `"#1"`, `"#2"`, `"#3"`. Use it in all API calls and when referring to tasks in conversation: "Task #1 (Add authentication)".

## Available Functions

### getProjectTask(taskRef)

Get a project task by task ref.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `taskRef` | str | Yes | Task ref to retrieve |

**Returns:** Dict with `taskRef`, `title`, `description`, `state`, `createdAt`, `updatedAt`

**Example:**

```javascript
const task = await getProjectTask({ taskRef: "#1" });
// "Task #1 (Add authentication)"
```

### updateProjectTask(taskRef, title=None, description=None, dependsOn=None)

Update an existing project task's content. All fields are optional - only provided fields are updated.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `taskRef` | str | Yes | Task ref to update |
| `title` | str | No | New title |
| `description` | str | No | New description |
| `dependsOn` | array of str | No | Full list of dependency task refs (replaces existing) |

**Returns:** Dict with `taskRef`, `title`, `description`, `state`, `createdAt`, `updatedAt`

**Example:**

```javascript
await updateProjectTask({ taskRef: "#1", title: "Updated title" });
```

### markTaskInProgress(taskRef)

Resume work on an IMPLEMENTED task. Call this before making further changes to a task that was already marked complete.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `taskRef` | str | Yes | Task ref to resume |

**Returns:** Dict with `taskRef`, `title`, `description`, `state`, `createdAt`, `updatedAt`

**Example:**

```javascript
await markTaskInProgress({ taskRef: "#1" });
```

### searchProjectTasks(query, locale=None, limit=None)

Search project tasks by text query, ordered by relevance.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | str | Yes | Search query. Supports boolean syntax: `"exact phrase"`, `foo bar` (both words), `foo OR bar`, `-foo` (exclude) |
| `locale` | str | No | BCP 47 locale of the query (e.g. `"en"`, `"es"`, `"fr"`). Pass when the query is in a non-English language for better stemming. Omit for English. |
| `limit` | int | No | Maximum number of results (default: 20) |

**Returns:** List of dicts, each with `taskRef`, `title`, `description`, `state`, `score`, `matchType`, `createdAt`, `updatedAt`

**Example:**

```javascript
// Simple keyword search
const results = await searchProjectTasks({ query: "authentication" });

// Boolean syntax: find auth tasks that aren't about login
const results = await searchProjectTasks({ query: "authentication -login", limit: 5 });

// Exact phrase
const results = await searchProjectTasks({ query: '"payment integration"' });

// Non-English query — pass locale for better stemming
const results = await searchProjectTasks({ query: "autenticación", locale: "es" });

for (const r of results) {
    console.log(`${r.taskRef} (${r.title}) — score: ${r.score}`);
}
```

### listProjectTasks(state=None, taskRefs=None, includeDescription=False)

List project tasks, optionally filtered by state or specific task refs.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `state` | str | No | Filter by state (e.g., "IN_PROGRESS") |
| `taskRefs` | array of str | No | List of specific task refs to retrieve |
| `includeDescription` | bool | No | Whether to include the task description (default: false) |

**Returns:** List of dicts, each with `taskRef`, `title`, `state`, `dependsOn`, `createdAt`, `updatedAt` (plus `description` if `includeDescription` is true). `dependsOn` lists the task refs of dependency tasks that are also in the result set. When filtering by `taskRefs`, dependencies pointing outside the filter are omitted.

**Example:**

```javascript
const allTasks = await listProjectTasks();
for (const task of allTasks) {
    console.log(`  - Task ${task.taskRef} (${task.title})`);
}
```

### bulkCreateProjectTasks(tasks)

Create multiple tasks at once with dependency relationships. Each task is created in PROPOSED state. The plan file content becomes the task description.

By default, create one task per user request. Combine related work into a single plan rather than splitting into many tasks. Only create multiple tasks if the user explicitly asks for them or the request contains clearly independent, unrelated goals.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `tasks` | array | Yes | List of task objects (see below) |

Each task object:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | str | No | Alias for this task within the batch. Used by other tasks' `dependsOn` to declare dependencies. Auto-generated if omitted. |
| `title` | str | Yes | Short title for the task |
| `filePath` | str | Yes | Path to the plan file (e.g. `.local/tasks/payment-integration.md`). The file content becomes the task description. |
| `dependsOn` | array | No | List of `id` values from other tasks in this batch, or task refs (`"#1"`, `"#2"`) of already-existing accepted tasks. Never depend on existing PROPOSED tasks — only on tasks that are PENDING or later. Tasks within the same batch may depend on each other freely. |

**Returns:** List of created task dicts with `taskRef`, `title`, `description`, `state`, `dependsOn`, `createdAt`, `updatedAt`

**Examples:**

```javascript
// Single task (no dependencies)
const created = await bulkCreateProjectTasks({
    tasks: [
        {
            title: "Payment integration",
            filePath: ".local/tasks/payment-integration.md",
        },
    ]
});

// Multiple tasks with dependencies using id aliases
const created = await bulkCreateProjectTasks({
    tasks: [
        {
            id: "auth",
            title: "Add authentication",
            filePath: ".local/tasks/auth.md",
        },
        {
            id: "payments",
            title: "Payment integration",
            filePath: ".local/tasks/payments.md",
            dependsOn: ["auth"],
        },
    ]
});
```

## Plan File Format

Write each project-task plan file as a plain markdown document in
`.local/tasks/`. The file content becomes the task description.

By default, create one project task per user request. Combine related work
into a single plan rather than splitting into many tasks. Only create
multiple tasks if the user explicitly asks for them or the request contains
clearly independent, unrelated goals.

Dependencies are not declared in the plan file. Pass them via `dependsOn`
when creating or updating tasks.

### Plan body

The first line should be a short, descriptive title (3-6 words) prefixed
with `#`. Then include these sections:

- **What & Why** — Brief description of the feature/change and its purpose.
- **Done looks like** — Observable outcomes when complete (what the user
  sees, not code-level details).
- **Out of scope** — What is explicitly NOT included.
- **Tasks** — Numbered list of implementation steps within this plan. These
  are internal steps for the executor agent, not separate project tasks.
- **Relevant files** — Existing files discovered during investigation that
  the executor should start from. Use backtick-wrapped paths only, with no
  descriptions after them. Only list files you verified exist.
  - Whole file: `src/api/billing.ts`
  - Specific lines: `src/api/billing.ts:12-85`
  - Multiple ranges: `src/api/billing.ts:12-85,200-250`
  - WRONG: `src/api/billing.ts` — Billing API handlers (lines 12-85)

Assume features build on each other. If a new task depends on another task,
declare that dependency via `dependsOn` rather than in the plan body. You
may depend on existing tasks that are PENDING or later — never on existing
PROPOSED tasks. Tasks within the same batch may depend on each other freely.

Rules for the `## Tasks` section:

- Each task should be describable in 1-2 sentences.
- Focus on what to build, not how to build it.
- Do not include file paths, code snippets, CSS classes, or line-level edits
  in task bullets. Put file references in `## Relevant files` instead.
- Draw clean boundaries so parallel executors will not create conflicting
  changes. If two tasks would touch the same area, combine them into one
  project task.
- If there is a critical architectural constraint the executor must follow,
  add a short note.

### Example

```markdown
# Payment Integration

## What & Why
Add Stripe payment processing so users can upgrade to paid plans.

## Done looks like
- Users can enter payment info and subscribe to a plan
- Successful payments activate the paid tier immediately
- Failed payments show a clear error message

## Out of scope
- Invoicing and receipts (future work)
- Multiple payment methods (Stripe only for now)

## Tasks
1. **Stripe backend integration** — Set up Stripe SDK, create endpoints for creating checkout sessions and handling webhooks.

2. **Payment UI** — Build the checkout page with plan selection and Stripe Elements for card input.

3. **Tier activation** — On successful payment, upgrade the user's account to the paid tier and reflect it in the UI.

## Relevant files
- `src/api/billing.ts:12-85`
- `src/config/stripe.ts`
```

### proposeProjectTasks(taskRefs)

Propose existing tasks for user review and approval. This pauses the agent to wait for user approval.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `taskRefs` | array of str | Yes | Task refs to propose |

**Returns:** Dict with `proposed` list of `{ taskRef, title }` summaries

**Example:**

```javascript
await proposeProjectTasks({ taskRefs: created.map(t => t.taskRef) });
```

## Task States

| State | Description |
|-------|-------------|
| `PROPOSED` | Suggested but not yet accepted by the user. No implementation exists. |
| `PENDING` | Accepted, waiting to start. No implementation exists. |
| `IN_PROGRESS` | Being worked on by a task agent in a separate Repl. Changes are not visible in this Repl. |
| `IMPLEMENTED` | Work is done in a separate Repl, ready for merge. Changes are not visible in this Repl — do not search the codebase for them. |
| `MERGING` | Currently being merged. Do not duplicate. |
| `MERGED` | Finished and merged. Changes are now visible in this Repl. |
| `BLOCKED_BY_DRIFT` | Blocked because an upstream task diverged from its plan; needs replanning. |
| `CANCELLED` | Abandoned. |

## User Communication Rules

Task management is how you coordinate work with the user. Follow these rules strictly:

1. **Always describe tasks by ref and title**: When referring to tasks, always use their task ref and title, e.g. "Task #1 (Add authentication button)".
2. **Never use internal state names**: When talking to the user, use these display names instead:
   - PROPOSED → "Drafts"
   - PENDING → "Active"
   - IN_PROGRESS → "Active"
   - IMPLEMENTED → "Ready"
   - MERGING → "Merging"
   - MERGED → "Merged"
   - CANCELLED → "Archived"
   - BLOCKED_BY_DRIFT → "Affected by another task that changed"
3. **Never expose implementation details**: Do not reveal function names (`bulkCreateProjectTasks`, `updateProjectTask`, etc.), API surface, or internal task system mechanics to the user.

## Best Practices

1. **Prefer fewer tasks**: Default to one task per request unless the user explicitly asks for more
2. **Create tasks early**: Create the project task when you understand the user's goals
3. **Keep titles short**: Titles should be concise and descriptive
4. **Use descriptions for detail**: Put implementation details in the description field

## Example Workflow

```javascript
// 1. Write a plan file to .local/tasks/ (using write tool beforehand)

// 2. Create the task — file content becomes the description
const created = await bulkCreateProjectTasks({
    tasks: [
        {
            title: "Payment integration",
            filePath: ".local/tasks/payment-integration.md",
        },
    ]
});

// 3. Propose for user approval (pauses agent loop)
await proposeProjectTasks({
    taskRefs: created.map(t => t.taskRef),
});

// --- After user approves, the system handles scheduling ---

// 4. Check progress
const tasks = await listProjectTasks();
for (const task of tasks) {
    console.log(`Task ${task.taskRef} (${task.title}): ${task.state}`);
}
```

```

---

## Skill: query-integration-data

**Path:** `.local/skills/query-integration-data/SKILL.md`

```markdown
---
name: query-integration-data
description: Query and modify data in any connected integration (Linear, GitHub, HubSpot, Slack, Google services, etc.) or connected data warehouse (Databricks, Snowflake, BigQuery). Use listConnections() in the code_execution sandbox to get credentials, then call APIs directly. Supports read operations (queries, counts, exports) and write operations (create, update, delete).
---

# Query Integration Data Skill

Connect to any Replit-supported integration to read or write data — query issues, create tickets, send messages, update contacts, manage files, etc. This also includes querying supported data warehouse integrations like Databricks, Snowflake, and BigQuery.

All code runs inline in the `code_execution` sandbox — no script files needed.

## When to Use

Use this skill when the user asks you a **question in chat** that requires data from external services to answer, or when they need to perform data operations without building a visual interface.

- **Answer questions**: Query data to respond to user questions in the conversation (e.g., "How many issues were created this week?")
- **Fetch and export data**: Export data to CSV/JSON for later use or analysis
- **Write operations**: Create, update, delete, or modify data in a service
- **Ad-hoc queries**: One-time data lookups or investigations
- **Automate tasks**: Perform multi-step operations across the API

**Key point:** Use this skill when the output is an answer or data file, NOT when building a dashboard or visualization interface.

## When NOT to Use

- **The user wants to create a dashboard, visualization, or analytics interface** - use the `data-visualization` skill (it handles data fetching internally)
- **The user asks to "build", "create", or "make" a dashboard/app with data** - use the `data-visualization` skill
- The user needs to add an integration to their app (use the `integrations` skill)
- Production database operations (use the database pane directly)
- Asks to check deployment or server logs (use the `fetch-deployment-logs` skill)

## File Structure

```text
.agents/
└── outputs/         # Generated artifacts (CSV, JSON, etc.)
```

Code runs inline in the `code_execution` sandbox — no script files are needed.

## Workflow

```text
1. CHECK      → listConnections(connectorName) to get existing credentials
   ├─ connections exist → EXECUTE → OUTPUT
   └─ empty array      → SEARCH → LEARN → CLARIFY → setup via `integrations` skill → EXECUTE → OUTPUT
```

- **CHECK**: Call `listConnections(connectorName)` in the `code_execution` sandbox. If it returns connections, you already have credentials — skip straight to EXECUTE.
- **SEARCH → CONNECT** (only when no connections exist): Use `searchIntegrations`, `proposeIntegration`, and `addIntegration` to set up a new connection. See the `integrations` skill for the full lifecycle details.
- **EXECUTE**: Write and run code in the `code_execution` sandbox.
- **OUTPUT**: Return the answer or confirmation to the user.

## Getting Connection Credentials

### Primary: `listConnections(connectorName)`

This is the main way to get credentials. It's a pre-registered function in the `code_execution` sandbox.

```javascript
const conns = await listConnections('linear');
console.log(conns.map(c => ({ id: c.id, displayName: c.displayName, status: c.status })));
```

Each connection object has:

- `id`, `connectorConfigId`, `status`, `displayName`, `metadata`, `environment`
- `settings` — credentials dict (access tokens, API keys, etc.)
- `getClient()` — returns the `settings` object for constructing SDK clients

Returns an empty array when no connections are configured.

```javascript
const conns = await listConnections('linear');
if (conns.length > 0) {
  const token = conns[0].settings.access_token;
  const { LinearClient } = await import('@linear/sdk');
  const client = new LinearClient({ accessToken: token });
  // Ready to query
}
```

### Fallback: Setting Up a New Connection

If `listConnections` returns an empty array, the user hasn't connected the service yet. Use `searchIntegrations` to find the connector, then follow the `integrations` skill to walk the user through setup (`addIntegration` and `proposeIntegration` — order depends on integration type). After the connection is established, `listConnections` will return it.

### Browse the Documentation

**Always browse `public_documentation_link`** before writing code, especially for write operations. This helps you understand:

- Required vs optional fields for creating resources
- Valid values for enums (status, priority, type, etc.)
- Relationships between resources (e.g., issues belong to projects)
- Rate limits and best practices

## Clarifying Questions

**Before write operations, gather required information.** Many APIs require IDs or specific values that the user may not know.

### When to Ask

Ask clarifying questions when the user's request requires:

- **Entity selection**: "Which project should this issue be created in?"
- **User assignment**: "Who should be assigned? Let me list the team members..."
- **Required fields**: "What priority - urgent, high, medium, or low?"
- **Ambiguous references**: "I found 3 projects matching 'backend'. Which one?"

### Pattern: Fetch Options First

For write operations, often run a read query first to get valid options:

```javascript
// User says: "Create a Linear ticket assigned to John"
// Problem: Need John's user ID, not just name

const conns = await listConnections('linear');
const { LinearClient } = await import('@linear/sdk');
const client = new LinearClient({ accessToken: conns[0].settings.access_token });

// Step 1: List users to find John's ID
const users = await client.users();
const john = users.nodes.find(u => u.name.includes('John'));

// Step 2: If ambiguous, ASK the user
// "I found John Smith and John Doe. Which one?"

// Step 3: Create with correct ID
await client.createIssue({ assigneeId: john.id, ... });
```

### Common Multi-Step Patterns

| Action                     | First fetch...            |
| -------------------------- | ------------------------- |
| Create issue with assignee | List team members         |
| Create issue in project    | List projects             |
| Set status/priority        | Get valid workflow states |
| Add to channel             | List channels             |
| Assign to team             | List teams                |

## Running Code in the Sandbox

All code runs in the `code_execution` sandbox. State persists across calls (notebook-style), so variables from one call are available in subsequent calls.

### Read Operations

Query data and return results:

```javascript
const conns = await listConnections('linear');
const { LinearClient } = await import('@linear/sdk');
const client = new LinearClient({ accessToken: conns[0].settings.access_token });

const issues = await client.issues({ first: 10 });
console.log(`Found ${issues.nodes.length} issues`);
for (const issue of issues.nodes) {
  console.log(`${issue.identifier}: ${issue.title} [${issue.state?.name}]`);
}
```

### Write Operations

Create, update, or delete data:

```javascript
const conns = await listConnections('linear');
const { LinearClient } = await import('@linear/sdk');
const client = new LinearClient({ accessToken: conns[0].settings.access_token });

// Create
const created = await client.createIssue({ teamId: team.id, title: "Fix login bug" });
console.log(`Created: ${created.issue?.identifier}`);

// Update
await client.updateIssue(issueId, { stateId: doneState.id });
console.log(`Updated: ${issueId}`);

// Delete
await client.deleteIssue(issueId);
console.log(`Deleted: ${issueId}`);
```

### Multi-Step Operations

Variables persist across `code_execution` calls, enabling multi-step workflows:

```javascript
// Call 1: Get credentials and list teams
const conns = await listConnections('linear');
const { LinearClient } = await import('@linear/sdk');
const client = new LinearClient({ accessToken: conns[0].settings.access_token });

const teams = await client.teams();
const team = teams.nodes[0];
console.log(`Using team: ${team.name}`);

const users = await client.users();
const assignee = users.nodes.find(u => u.name === 'John');
console.log(`Found assignee: ${assignee?.name}`);
```

```javascript
// Call 2: Variables from Call 1 are still available
const issue = await client.createIssue({
  teamId: team.id,
  assigneeId: assignee?.id,
  title: 'New feature request',
  description: 'Details here...',
});
console.log(`Created ${issue.issue?.identifier}: New feature request`);
```

## Warehouse Data Exploration

When querying data warehouses (BigQuery, Snowflake, Databricks), large schemas can make serial exploration slow (7-10s per query round-trip). Use the parallel subagent pattern to explore schemas faster.

### When to Use Parallel Exploration

Use this pattern when ALL of the following are true:

- The target is a **warehouse** connection (`bigquery`, `snowflake`, or `databricks`)
- The initial INFORMATION_SCHEMA query returns **15+ tables**
- The user's question is **not about a specific known table** (e.g., they're asking a broad question like "what's our revenue trend?" or "show me customer data")

If the schema has fewer than 15 tables, serial exploration is fast enough — just query tables one-by-one.

### 4-Step Parallel Workflow

**Step 1: Schema Discovery** — Run a single `executeSql` call to get the full table list.

```javascript
// BigQuery
const tables = await executeSql({ sqlQuery: `SELECT table_schema, table_name, row_count FROM \`project.region-us\`.INFORMATION_SCHEMA.TABLES WHERE table_schema NOT IN ('INFORMATION_SCHEMA') ORDER BY table_schema, table_name`, target: "bigquery" });

// Snowflake
const tables = await executeSql({ sqlQuery: `SELECT TABLE_SCHEMA, TABLE_NAME, ROW_COUNT FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA NOT IN ('INFORMATION_SCHEMA') ORDER BY TABLE_SCHEMA, TABLE_NAME`, target: "snowflake" });

// Databricks
const tables = await executeSql({ sqlQuery: `SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema') ORDER BY table_schema, table_name`, target: "databricks" });
```

**Step 2: Group Tables** — Partition the table list into 2-4 clusters:

- By schema/dataset name (e.g., `analytics.*`, `sales.*`, `marketing.*`)
- By name prefix (e.g., `dim_*`, `fact_*`, `stg_*`)
- By estimated relevance to the user's question (most-likely-relevant tables first)

**Step 3: Launch Parallel Subagents** — Start one `SMALL_TASK` subagent per group:

```javascript
const group1 = await startAsyncSubagent({
  task: `Explore these warehouse tables to answer: "${userQuestion}"

Connection: Use executeSql({ sqlQuery: "...", target: "bigquery" }) — always pass target.
Dialect: BigQuery (use backtick quoting for project.dataset.table)

Tables to explore:
- analytics.events
- analytics.sessions
- analytics.conversions

For each table:
1. Run: SELECT column_name, data_type FROM \`project.dataset\`.INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'TABLE_NAME'
2. Run: SELECT * FROM \`project.dataset.TABLE_NAME\` LIMIT 5

Return your findings in this exact format:

## Table Relevance
| Table | Relevant? | Why |
|-------|-----------|-----|
| ... | Yes/No | Brief reason |

## Column Details (relevant tables only)
| Table | Column | Type | Notes |
|-------|--------|------|-------|
| ... | ... | ... | Key field, foreign key, metric, etc. |

## Suggested Join Conditions
- table_a.id = table_b.a_id (describe relationship)

## Key Findings
- Bullet points about data patterns, date ranges, notable values`,
  specialization: 'SMALL_TASK',
  relevantFiles: ['.local/skills/database/SKILL.md']
});

// Launch additional subagents for other groups (2-4 total)
const group2 = await startAsyncSubagent({ /* same pattern, different tables */ });
```

**Step 4: Synthesize and Query** — Wait for all subagents, then write the final query:

```javascript
await waitForBackgroundTasks();
// Read subagent outputs, combine relevant tables/columns, write the final SQL query
```

### Dialect-Specific Notes

| Dialect | Table Quoting | INFORMATION_SCHEMA Path | Sample Query |
|---------|--------------|------------------------|--------------|
| BigQuery | `` `project.dataset.table` `` | `` `project.dataset`.INFORMATION_SCHEMA.COLUMNS `` | `SELECT * FROM \`p.d.t\` LIMIT 5` |
| Snowflake | `"DATABASE"."SCHEMA"."TABLE"` | `DATABASE.INFORMATION_SCHEMA.COLUMNS` | `SELECT * FROM "DB"."SCH"."TBL" LIMIT 5` |
| Databricks | `` `catalog.schema.table` `` | `catalog.information_schema.columns` | `SELECT * FROM \`c.s.t\` LIMIT 5` |

### Tips

- Each subagent should run 3-6 SQL queries (column metadata + sample data per table)
- Keep subagent count to 2-4 — more than 4 has diminishing returns
- The structured markdown output format ensures consistent, scannable results
- After synthesis, write a single well-commented SQL query that answers the user's question

## Output Guidelines

- **Simple answers** (counts, scalar values, short lists of < 20 records): Print directly with `console.log()`
- **Complex results** (tabular results): Write to `.agents/outputs/<filename>.csv` and summarize
- **Write confirmations**: Print what was created/updated/deleted with IDs
- **Errors**: Print clear error messages

```javascript
const fs = await import('fs');

// Simple
console.log(`Answer: 42 issues created this week`);

// Tabular results - write CSV to .agents/outputs/
fs.mkdirSync('.agents/outputs', { recursive: true });
fs.writeFileSync('.agents/outputs/results.csv', csvContent);
console.log(`Exported 500 records to .agents/outputs/results.csv`);

// Write
console.log(`Created issue ENG-123: "Fix login bug"`);
console.log(`Updated 5 contacts`);
console.log(`Deleted message ID abc123`);
```

## Key Points

- **Use `listConnections(connectorName)`** as the primary way to get credentials
- **Fall back to search → propose → add** when no connections exist (see `integrations` skill)
- **All code runs in the `code_execution` sandbox** — no script files needed
- **Use `console.log()`** to see output — functions execute silently without it (but never log credentials)
- **Use `await import(...)`** for packages (dynamic imports only)
- **State persists** across `code_execution` calls — reuse `conns`, clients, and extracted credentials instead of re-fetching (unless expired).
- **Browse `public_documentation_link`** to understand the API before coding
- **Ask clarifying questions** before write operations that need specific IDs or values
- **Fetch options first** when the user references something by name (users, projects, etc.)
- **Don't cache clients** — access tokens expire; re-create clients from `listConnections` when needed
- **Write large outputs to `.agents/outputs/`** as CSV or JSON

```

---

## Skill: remove-image-background

**Path:** `.local/skills/remove-image-background/SKILL.md`

```markdown
---
name: remove-image-background
description: Remove backgrounds from existing images, producing transparent PNG files.
---

# Remove Image Background Skill

Remove the background from an existing image file in the project, producing a transparent PNG.

## Available Functions

### removeImageBackground(imagePath, ...)

Remove the background from an existing image file.

**Parameters:**

- `imagePath` (str, required): Path to the input image file
- `outputPath` (str, optional): Path to save the result PNG. Defaults to replacing the extension with `_no_bg.png`

**Returns:** Dict with `outputPath` key containing the path to the saved result

**Example:**

```javascript
const result = await removeImageBackground({
    imagePath: "attached_assets/photo.jpg",
    outputPath: "attached_assets/photo_no_bg.png"
});
console.log(`Result saved to: ${result.outputPath}`);
```

## When to Use

- User has an existing image and wants its background removed
- User uploads a photo and asks to make the background transparent
- Creating transparent versions of logos, product photos, or portraits
- Preparing images for compositing or overlay on other backgrounds

## Best Practices

1. **Output must be PNG**: The output file must have a `.png` extension since transparency requires PNG format
2. **Use default output path when possible**: Omit `outputPath` to automatically save as `<original_name>_no_bg.png`
3. **Supported input formats**: Works with common image formats (PNG, JPG, JPEG, WebP, etc.)

## Output Location

- Default output: Same directory as input, with `_no_bg.png` suffix
- Custom output: Any path ending in `.png`

## Limitations

- Output format is always PNG (required for transparency)
- Very complex backgrounds or low-contrast edges may not be perfectly removed
- Works best with clear foreground subjects (people, objects, logos)

```

---

## Skill: repl_setup

**Path:** `.local/skills/repl_setup/SKILL.md`

```markdown
---
name: repl_setup
description: Setup and configure web applications in the Replit environment. Covers host configuration, frontend/backend connectivity, cache control, and framework-specific setup for Angular, React, Vite, and Vue.
---

# Repl Setup

Guidelines for setting up and configuring web applications to work correctly in the Replit environment. Users see your application through a proxy (iframe), which requires specific configuration.

## When to Use

Use this skill when:

- Setting up a new web application or frontend framework
- The user cannot see your frontend changes
- Configuring host settings for development servers
- Connecting frontend code to backend APIs
- Debugging visibility issues with the user's preview

## When NOT to Use

- For non-web applications (CLI tools, scripts, etc.)
- When the application is already working correctly
- For deployment/publishing issues (use the deployment skill)

## Critical Replit Environment Rules

### Host Configuration

The user sees your frontend through a proxy within an iframe. **You must configure your development server to allow all hosts**, otherwise the user will never see your frontend.

Every web framework needs its development configuration set to allow all hosts. If you don't know the specific configuration for a framework, use web search to find it.

### Frontend Server Port

Bind frontend servers to **0.0.0.0:5000**. Never bind anything else to port 5000.

### No Docker or Virtual Environments

Never use Docker, virtual environments, or containerization. Replit uses a Nix environment that doesn't support nested virtualization.

## Stack-Specific Setup

For framework-specific configuration, refer to these guides:

- `references/angular.md` - Angular setup with allowedHosts and CLI flags
- `references/react_vite.md` - React and Vite configuration
- `references/vue.md` - Vue.js setup

## Frontend-Backend Connectivity

When your frontend calls a local backend API:

1. **Get the public domain**: Run `env | grep DOMAIN` in the shell to get the website's public URL
2. **Use the public URL**: Replace any `localhost` references with the public domain
3. **Never use localhost**: You're in a cloud environment - the user cannot access your localhost

```bash
# Get the public domain for API calls
env | grep DOMAIN
```

## Debugging Visibility Issues

If the user reports they cannot see your changes:

1. **Check workflow status**: Ensure the workflow is running and has been restarted after changes
2. **Read console logs**: Check for errors and follow any instructions in the logs
3. **Verify host configuration**: Confirm the framework's dev config allows all hosts (most common issue)
4. **Cache control** (rare): If above checks pass, the issue may be caching
   - Modify webserver code to disable cache storage
   - Instruct user to use "empty cache and hard refresh" in developer tools

## Workflow Setup Order

Always set up frontend workflows first, then backend services. After completing any task:

1. Re-run the workflows to ensure they're running
2. Read the console logs to verify no errors
3. Take a screenshot to confirm the frontend is visible

## Best Practices

1. **Verify host config early**: Check framework-specific allowedHosts before writing any code
2. **Test visibility immediately**: After setup, verify the user can see the preview
3. **Use public URLs**: Never hardcode localhost in frontend code
4. **Restart after changes**: Server-side changes require workflow restart
5. **Check logs first**: Console logs often reveal the root cause of issues

```

---

## Skill: replit-docs

**Path:** `.local/skills/replit-docs/SKILL.md`

```markdown
---
name: replit-docs
description: Search Replit documentation for platform features, pricing, deployments, and capabilities.
---

# Replit Docs Skill

Search Replit documentation to find information about features, pricing, deployments, and platform capabilities.

## When to Use

Use this skill when:

- You need information about Replit platform features
- Looking up pricing details for plans and services
- Getting deployment guidance for applications
- Understanding platform capabilities and limitations
- Finding solutions to common platform issues
- Learning best practices for development on Replit

## When NOT to Use

- Integration setup (use integrations skill first, then docs for additional context)
- Code debugging (use code analysis tools)
- Real-time status or outages (documentation may be outdated)
- Account-specific issues
- General programming questions not related to Replit

## Available Functions

### searchReplitDocs(query)

Search Replit documentation for platform information.

**Parameters:**

- `query` (str, required): Natural language question about Replit features, pricing, or capabilities

**Returns:** Dict with `response` and `relevantPages` (list of title/url dicts)

**Example:**

```javascript
// Get pricing information
const result = await searchReplitDocs({ query: "How much does Core cost?" });
console.log(result.response);
for (const page of result.relevantPages) {
    console.log(`${page.title}: ${page.url}`);
}

// Learn about deployments
const result = await searchReplitDocs({ query: "How do I deploy a web app?" });
console.log(result.response);
```

## Best Practices

1. **Use natural language**: Write queries as complete questions with context
2. **Be specific**: Include specific feature names or topics in queries
3. **Check integrations first**: For setup instructions, search integrations first, then use docs for additional context
4. **Verify with sources**: Check the relevant pages returned for authoritative information

## Example Workflow

```javascript
// User asks about object storage pricing
const result = await searchReplitDocs({ query: "How much does Replit object storage cost?" });
console.log(result.response);

// Provide relevant documentation links
for (const page of result.relevantPages) {
    console.log(`- ${page.title}: ${page.url}`);
}
```

## Limitations

- Documentation may not reflect real-time service status
- Cannot answer account-specific questions
- For integration setup, prefer the integrations skill
- General programming questions should use web search instead

```

---

## Skill: revenuecat

**Path:** `.local/skills/revenuecat/SKILL.md`

```markdown
---
name: revenuecat
description: Guidelines for using RevenueCat to integrate payments in mobile apps and any subsequent CRUD operations related to any RevenueCat entities

# Note: ./references/replit-revenuecat-v2-docs.md is copy-pasted manually from https://github.com/replit/replit-revenuecat-v2/blob/main/docs/SDK.ts and was last updated: 2026-03-18 for version 3.0.0
---


## Introduction

- RevenueCat lets users monetize their native mobile apps on Replit.
- The RevenueCat integration is only intended to be used for the Expo/mobile stack on Replit.
- If the stack used is *not* Expo/mobile, do not use RevenueCat, and instead suggest the Stripe integration.
- The package used in the React Native client code is `react-native-purchases`. Always download the version that is compatible with the version of React Native/Expo used in the app.

## Prerequisites

1. These packages must be installed in the workspace root package.json:
    - `react-native-purchases` - Official client-side SDK for React Native. This should be used on the client.
    - `replit-revenuecat-v2` - SDK for RevenueCat's REST API. This should NEVER be used on the client, only for server-side scripts.

    If they are not installed, use npm to install them: `$ cd /home/runner/workspace && npm install <packages>`


2. The RevenueCat integration must be connected to the repl. This is necessary as the integration creates an authenticated client for RevenueCat accessible via a function `getUncachableRevenueCatClient`. You can do this by proposing the integration. Reference the `integrations` skill if necessary.

You are required to ensure these requirements are met before setting up or using RevenueCat.

## Project Structure

- **Scripts directory**: `scripts/` at the workspace root (e.g., `scripts/seedRevenueCat.ts`)
- **Run a script**: `npx tsx scripts/<script>.ts`
- **Client app directory**: `client/`

Reference files use these terms. Map them to these concrete paths.

## Essential Clarifications -- Critical

- RevenueCat DOES work in Expo Go and DOES NOT require a native build. In Expo Go, the SDK automatically runs in Preview API Mode, replacing native calls with JavaScript mocks so your app loads without errors.
- RevenueCat DOES work on the web out of the box without any additional configuration.
- RevenueCat's Test Store DOES work out of the box and DOES NOT require additional code checks.

## RevenueCat Architecture

- **Projects:** A RevenueCat project is the top-level entity for RevenueCat - it's like a container for your apps, products, entitlements, and integrations.
  - Each project comes with a Test Store where you can create products, configure offerings, and test the complete purchase flow—without connecting to any app store or payment provider.
- **Apps:** An app in RevenueCat is a platform-specific configuration that connects your project to a store (e.g., an iOS app connected to Apple App Store, an Android app connected to Google Play Store, or a web app connected to Stripe/Paddle).
- **Products:** The individual items users purchase (e.g., "Monthly Premium")
- **Entitlements:** The access level users receive (e.g., "premium"). Most apps use a single entitlement (e.g., "pro"). They are linked to products: when a product is purchased, its associated entitlements become active.
  - The flow: User purchases a Product -> which then unlocks an Entitlement -> You check the entitlement to grant access.
- **Offerings:** The set of products available to a user. Allow you to change available products without app updates. Access via `offerings.current` on the client for the default offering.
  - The client side code always queries the current offering as a source of truth to get the products and packages available to the user. Therefore, it is critical that this be always up to date.
- **Packages:** Containers for products within an offering.
- **CustomerInfo**: The central object containing all subscription and purchase data for a user

## Storing Data

Do NOT Create Product Tables or Maintain Any Other Source of Truth for In-App Purchases

**Bad** — creates duplicate product storage:

```ts
export const products = pgTable("products", {
  id: varchar("id").primaryKey(),
  name: text("name"),
  price: integer("price"),
  // ... custom fields
});
```

Correct Approach:

- NO product tables needed!
- Query directly from RevenueCat SDK

Key Principle
"If it exists in RevenueCat, it belongs in RevenueCat"

- Don't duplicate RevenueCat data in your own tables.
- Don't create parallel storage systems.
- RevenueCat + metadata = your complete product catalog.
- Your tables should only store data that RevenueCat doesn't manage.

## Free Trials

- Free trials are not supported in the test store due to a RevenueCat limitation.
- Free trials can be configured directly in App Store Connect and the Google Play Console.
- If a user asks about adding free trials:
  - Inform them of this limitation and note that the client can automatically detect and display free trials via RevenueCat once enabled in production.
  - RevenueCat reads store product metadata, including trial details, in the package object.

## Working with Prices

- Never hardcode prices in the client code; always derive them from the subscription context.
- Prices in the test store are immutable; production store prices are configured in App Store Connect and the Google Play Console.

## References

Before writing code, identify whether any reference below applies to the task. If it does, read it first.

- ./references/initial-setup.md -- Step-by-step guide for setting up RevenueCat from scratch in a project that doesn't already have it configured
- ./references/replit-revenuecat-v2-docs.md -- SDK Reference for the `replit-revenuecat-v2` package
- ./references/subsequent-management.md -- Querying RevenueCat data (e.g. fetching customers, entitlements) and managing resources (creating, updating, deleting products, offerings, prices, etc.) after initial setup

```

---

## Skill: skill-authoring

**Path:** `.local/skills/skill-authoring/SKILL.md`

```markdown
---
name: skill-authoring
description: Create reusable skills that extend agent capabilities. Use when the user asks to create a skill, teach you something reusable, or save instructions for future tasks.
---

# Skill Authoring

Create skills to save reusable knowledge, procedures, and workflows that persist across sessions. Skills are instructions for future versions of yourself—write them as if teaching a fresh instance how to handle a task.

## When to Use

- User asks to "create a skill" or "teach you how to do X"
- User wants to save instructions for repeated future use
- A workflow should be reusable across sessions

## How to Create a Skill

1. Choose a skill name (lowercase, hyphens only, e.g., `code-review`)
2. Write the SKILL.md file to `.agents/skills/SKILLNAME/SKILL.md`

## SKILL.md Format

```markdown
---
name: skill-name
description: What this skill does. When to use it.
---

# Skill Title

Instructions, examples, and workflows go here.
```

### Frontmatter Requirements

- `name`: Max 64 chars, lowercase letters/numbers/hyphens only
- `description`: Max 1024 chars, include WHAT it does and WHEN to use it

## Writing Tips

- **Be concise**: Only include info you don't already know
- **Match specificity to fragility**: Exact commands for fragile ops, general guidance for flexible tasks
- **Include examples**: Input/output pairs help with output quality
- **Keep under 500 lines**: For longer skills, reference separate files

## Skill Locations

- **`.agents/skills/`** - User and agent-editable skills. Create new skills here. These can be freely modified, updated, and deleted.
- **`~/.local/skills/`** - Replit-provided skills. These are read-only and managed by the platform.

## Key Considerations

- **Description is critical for discovery**: The description determines when you'll use this skill in the future. Be specific about triggers:
  - Bad: `description: Processes documents` (too vague)
  - Good: `description: Extracts text and images from PDF files. Use when the user asks to read, parse, or convert PDF documents.`
- **Collaborate with the user**: Ask what they want included. Don't guess—the user knows what's important to them
- **Include project-specific context**: File paths, naming conventions, API endpoints, preferred libraries—things unique to this user's workflow
- **Use separate files for large content**: Organize reference material in folders (e.g., `.agents/skills/SKILLNAME/reference/api.md`) and link to it from SKILL.md
- **Skills can be updated**: Skills in `.agents/skills/` are mutable. Update them as you discover better patterns—don't treat them as permanent. Iterate as the user's needs evolve
- **Skills can reference other skills**: A skill can invoke or build upon other skills. Use this to compose complex workflows from simpler building blocks

## Complete Example

```markdown
---
name: pr-review
description: Reviews pull requests for code quality and security. Use when the user asks to review a PR or check code changes.
---

# PR Review

## Process

1. Read the PR description and linked issues
2. Review each file for issues
3. Check for test coverage
4. Look for security vulnerabilities
5. Summarize findings with line references

## What to Check

- Logic errors and edge cases
- Security issues (injection, XSS, auth bypass)
- Performance concerns
- Missing error handling

## Output Format

\`\`\`markdown
## Summary
[1-2 sentence overview]

## Issues Found
- **[severity]** file:line - description

## Verdict
[Approve / Request Changes / Comment]
\`\`\`
```

```

---

## Skill: streamlit

**Path:** `.local/skills/streamlit/SKILL.md`

```markdown
---
name: streamlit
description: Guidelines for developing interactive Streamlit web applications, covering configuration, UI, and workflow.
---

Always follow these guidelines when building a Streamlit web application:

This stack establishes a complete environment for developing interactive Streamlit web applications.
Streamlit enables rapid development and deployment of data-driven web applications with Python.

## Configuration

- Server configurations is already set in the `.streamlit/config.toml` file do not change it.
- Add custom theme configurations to the same file if needed but only if the user requests it.

## UI Guidelines

- Maintain default font settings (family, size, colors) unless specifically requested
- Focus on content organization and interactive elements
- Utilize Streamlit's built-in components for consistent UI
- IMPORTANT: Do not use any custom styling/CSS for the application unless explicitly requested. Use Streamlit's default styling and built-in components.

## Technical Considerations

- The `experimental_rerun` function is not supported in this environment instead use the `st.rerun()` function.
- Use standard Streamlit functions for application flow control

## Workflow

- Use the following workflow command to run the application:

  ```bash
  streamlit run app.py --server.port 5000
  ```

```

---

## Skill: stripe

**Path:** `.local/skills/stripe/SKILL.md`

```markdown
---
name: stripe
description: Guidelines for using Stripe to integrate payments in mobile apps and any subsequent CRUD operations related to any Stripe entities
---

## Introduction

Replit offers a native integration with Stripe that allows users to implement payments in their applications

## Prerequisites

1. These packages must be installed in the workspace root package.json:
    - `stripe` - Official Stripe SDK for API operations
    - `stripe-replit-sync` - Handles webhook processing and database sync. Documentation: https://www.npmjs.com/package/stripe-replit-sync

    If they are not installed, use npm to install them: `$ cd /home/runner/workspace && npm install <packages>`


2. The Stripe integration must be connected to the repl. You can do this by proposing the integration. Reference the `integrations` skill if necessary.
    Once connected, create `stripeClient.ts` using the template from the code-templates reference -- this file fetches Stripe credentials from the Replit connection API and provides the authenticated client via `getUncachableStripeClient()`.

    Create it in the `server/` directory.


3. Ensure a PostgreSQL database exists. If you don't have one yet, use the tool to create a PostgreSQL database. Never use memory database for storing Stripe data.

You are required to ensure these requirements are met before setting up or using Stripe.

## Project Structure

- **Scripts directory**: `scripts/` at the workspace root (e.g., `scripts/seed-products.ts`)
- **Run a script**: `npx tsx scripts/<script>.ts`
- **API server directory**: `server/`
- **Client app directory**: `client/`

Reference files use these terms. Map them to these concrete paths.

## Initial Setup: Step-by-Step Implementation

Ensure prerequisites are met. Do not proceed until you have done so.

Follow these steps in order when implementing Stripe integration for the user. Create a task list to track implementation progress.

Read the code-templates reference file for full code file templates to use during these steps.

1. Set Up Database

    Create the users table with Stripe ID references:

    ```sql
    CREATE TABLE users (
      id TEXT PRIMARY KEY,
      email TEXT,
      stripe_customer_id TEXT,
      stripe_subscription_id TEXT,
      created_at TIMESTAMP DEFAULT NOW()
    );
    ```

    **Important**: stripe-replit-sync creates the `stripe` schema automatically. Create application tables (users, orders, etc.) in the public schema, not in the stripe schema.

2. Create Webhook Handler

    In the API server create `webhookHandlers.ts` - use the template provided in the code-templates reference. It handles webhook processing by calling `getStripeSync()` from stripeClient.

3. Initialize Stripe on Startup

    Add this initialization function to the API server's index.ts. **Important order:**

    1. Run migrations to create schema
    2. Get StripeSync instance
    3. Set up managed webhook (uses StripeSync)
    4. Sync existing data with syncBackfill()

    ```typescript
    import { runMigrations } from 'stripe-replit-sync';
    import { getStripeSync } from './stripeClient';

    async function initStripe() {
      const databaseUrl = process.env.DATABASE_URL;
      if (!databaseUrl) throw new Error('DATABASE_URL required');

      // 1. Create stripe schema and tables
      await runMigrations({ databaseUrl });

      // 2. Get StripeSync instance (needed for webhook setup and backfill)
      const stripeSync = await getStripeSync();

      // 3. Set up managed webhook
      const webhookBaseUrl = `https://${process.env.REPLIT_DOMAINS?.split(',')[0]}`;
      const { webhook } = await stripeSync.findOrCreateManagedWebhook(
        `${webhookBaseUrl}/api/stripe/webhook`
      );

      // 4. Sync all existing Stripe data
      await stripeSync.syncBackfill();
    }

    await initStripe();
    ```

4. Register Webhook Route in index.ts

    **Critical:** Register the webhook route BEFORE `express.json()` middleware. See the indexTemplate for the correct pattern:

    1. Route path is `/api/stripe/webhook`
    2. Webhook route uses `express.raw()` to get Buffer in `req.body`
    3. Webhook route is registered BEFORE `app.use(express.json())`
    4. Other routes registered after get parsed JSON automatically

    ```typescript
    app.post(
      '/api/stripe/webhook',
      express.raw({ type: 'application/json' }),
      async (req, res) => {
        const signature = req.headers['stripe-signature'];
        if (!signature) return res.status(400).json({ error: 'Missing signature' });

        const sig = Array.isArray(signature) ? signature[0] : signature;

        await WebhookHandlers.processWebhook(req.body as Buffer, sig);
        res.status(200).json({ received: true });
      }
    );

    app.use(express.json()); // Now apply to other routes
    ```

5. Create Storage Layer

    Create `storage.ts` - use the template provided in the code-templates reference. Query Stripe data from PostgreSQL `stripe` schema using standard SQL queries.

6. Set Up Other Routes

    Create `routes.ts` - use the template provided in the code-templates reference for products, prices, checkout, etc. These routes are registered AFTER `express.json()` so they get parsed JSON.

7. Create Products Script (Recommended)

    Create `seed-products.ts` - a script to add products and prices to Stripe via the API. **This is the recommended way to create products. Run it manually when creating products.**

    Use the seed-products template from the code-templates reference as a starting point:

    - Modify the script to create the specific products needed
    - Run it manually when adding products: `node seed-products.js`
    - Webhooks automatically sync created products to the database
    - Stripe handles test vs live mode based on API keys

    ```typescript
    import { getUncachableStripeClient } from './stripeClient';

    async function createProducts() {
      const stripe = await getUncachableStripeClient();

      // Create product
      const product = await stripe.products.create({
        name: 'Pro Plan',
        description: 'Professional subscription',
      });

      // Create prices for the product
      const monthlyPrice = await stripe.prices.create({
        product: product.id,
        unit_amount: 2900, // $29.00
        currency: 'usd',
        recurring: { interval: 'month' },
      });

      console.log('Created:', product.id, monthlyPrice.id);
    }

    createProducts();
    ```

    **Usage:**
    Run this script in development when you need to create or add products.

    **Optional idempotency:**
    To make the script safe to run multiple times, check if specific products exist first:

    ```typescript
    const products = await stripe.products.search({ query: "name:'Pro Plan'" });
    if (products.data.length > 0) {
      console.log('Pro Plan already exists');
      return;
    }
    ```

## Database Architecture

1. **stripe-replit-sync creates and manages the `stripe` schema automatically** - DO NOT create any tables in the stripe schema
2. The stripe schema contains tables for: products, prices, customers, subscriptions, payment_intents, etc.
3. **Application tables are created in the public schema (or other schemas)** - e.g., users, orders, etc.
4. Application tables store Stripe IDs as TEXT columns (e.g., `stripe_customer_id TEXT`, `stripe_subscription_id TEXT`)
5. Replit automatically handles deployment and Stripe data migration moving from sandbox to live.

## Synchronization Flow

1. Stripe credentials are fetched from Replit connection API
2. **`runMigrations()`** creates the stripe schema and all Stripe tables (idempotent, safe to run on every startup)
3. **`syncBackfill()`** syncs ALL existing Stripe data from Stripe API to the local PostgreSQL database on startup
4. **Managed webhooks** are automatically configured by `stripe-replit-sync`
5. **Webhooks** keep data up-to-date when changes occur in Stripe after startup
6. Application queries Stripe data from PostgreSQL `stripe` schema (fast, no API calls needed)

## Storing Data

Do NOT Create Product Tables or Maintain Any Other Source of Truth for Stripe Data

**Bad** -- creates duplicate product storage:

```ts
export const products = pgTable("products", {
  id: varchar("id").primaryKey(),
  name: text("name"),
  price: integer("price"),
  // ... custom fields
});
```

Correct Approach:

- NO product tables needed!
- Query directly from `stripe.products` and `stripe.prices`
- Use Stripe's metadata field for ALL custom attributes

### Creating Products and Prices

**NEVER insert data directly into the stripe schema tables.** Instead:
- Create products via Stripe API (using scripts)
- Stripe webhooks managed by stripe-replit-sync automatically sync the data to the stripe schema in the local database
- Query the synced data from the `stripe` schema tables using standard SQL queries

Create products in Stripe with metadata (use API or script):

```ts
await stripe.products.create({
  name: "Product Name",
  description: "...",
  images: ["https://..."],
  metadata: {
    category: "electronics",
    customField1: "value1",
    featured: "true",
  }
});
await stripe.prices.create({
  product: product.id,
  unit_amount: 9999,
  currency: 'usd',
});
```

Query from synced stripe tables:

```ts
const result = await db.execute(sql`
  SELECT
    p.id,
    p.name,
    p.metadata,
    pr.id as price_id,
    pr.unit_amount
  FROM stripe.products p
  JOIN stripe.prices pr ON pr.product = p.id
  WHERE p.active = true
`);
```

Use real Stripe price IDs in checkout:

```ts
// CORRECT
{ price: "price_1ABC...", quantity: 1 }
// WRONG - Never use price_data
{
  price_data: {
    unit_amount: 9999,
    currency: 'usd',
    product_data: { name: "..." }
  }
}
```

### Decision Tree: When to Create Tables

- Products/Prices? -- NO, use `stripe.products`/`stripe.prices`
- Customers? -- NO, use `stripe.customers`
- Subscriptions? -- NO, use `stripe.subscriptions`
- Orders/Cart/User preferences? -- YES, these aren't in Stripe
- Relationships to Stripe data? -- YES, store Stripe IDs as foreign keys

**Key Principle: "If it exists in Stripe, it belongs in Stripe"**

- Don't duplicate Stripe data in your own tables
- Don't create parallel storage systems
- Stripe + metadata = your complete product catalog
- Your tables should only store data that Stripe doesn't manage

**Creating products:**
Write a seed script that calls Stripe API (`stripe.products.create()`, `stripe.prices.create()`). Run this script in development to create your products. Webhooks automatically sync them to the database. Replit handles deployment automatically.

**Workflow:**

```bash
# Development:
# - Run seed script to create products in Stripe (test mode)
# - syncBackfill() syncs them to local database

# Deployment (handled by Replit):
# - Replit copies products/prices from dev Stripe to prod Stripe
# - Your code runs unchanged, syncBackfill() syncs prod database

# Production:
# - Modify products via Stripe Dashboard (scripts can't run in deployments)
# - Webhooks automatically sync changes to database
```

## Publishing with Stripe

To publish the app with working Stripe payments:

1. Go to the Stripe Dashboard (https://dashboard.stripe.com/apikeys)
2. Get live API keys (starts with `pk_live_` and `sk_live_`)
3. Open the Publish pane in the Workspace
4. Enter the live Publishable Key and Secret Key
5. Publish the app

**Placeholder Keys (User-Requested Only):**

Only offer placeholder keys if the user explicitly asks to publish without live Stripe keys and understands the consequences. Do NOT use these for any other purpose.

If the user confirms they want to proceed without live keys, suggest the following values to them:
- **Publishable Key:** `pk_live_abcdef`
- **Secret Key:** `sk_live_abcdef`

**Consequences the user must understand:**
- Placeholder keys will NOT process real payments
- The product catalog and checkout will not function on the published URL
- Real Stripe keys must be added later for payments to work

## Deleting Stripe Integration

To remove the Stripe integration from the project:

1. In the project, open the "Integrations" tab
2. Go to "Stripe" and click "Manage"
3. Select "Edit" then "Delete"

## Secrets and Environment Variables

**NEVER write secrets or environment variables directly to the `.replit` file.** This includes Stripe API keys, webhook signing secrets, database URLs, and any other sensitive configuration. Instead, reference the `environment-secrets` skill for the correct way to manage secrets and environment variables.

## Key Rules

**DO:**
- Create products via Stripe API using scripts (never with SQL INSERT)
- Query Stripe data from PostgreSQL `stripe` schema tables (products, prices, customers, subscriptions, etc.)
- Store Stripe IDs in application tables as TEXT (e.g., `stripe_customer_id TEXT`)
- Keep webhook handler minimal (just call `processWebhook` with payload and signature)
- Let `syncBackfill()` sync existing Stripe data on startup
- Let managed webhooks handle webhook configuration automatically
- Register webhook route BEFORE `express.json()` middleware

**ABSOLUTELY DO NOT:**
- Create any tables in the `stripe` schema - stripe-replit-sync manages this automatically
- Insert, update, or delete data in `stripe` schema tables - only query from them
- Use SQL INSERT for products, prices, customers, subscriptions - use Stripe API instead
- Manually copy database data between environments - Replit handles Stripe product/price copying during deployment
- Add custom logic in webhook handler beyond calling `processWebhook`
- Skip running `runMigrations()` or `syncBackfill()`
- Create StripeSync instance before calling `runMigrations()`

## Common Mistakes

**Database - DO NOT create Stripe tables:**

```sql
-- WRONG - Creating Stripe tables manually
CREATE TABLE products (
  id TEXT PRIMARY KEY,
  name TEXT,
  price INTEGER
);

-- CORRECT - Create application tables, store Stripe IDs
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  stripe_customer_id TEXT
);
-- stripe-replit-sync creates stripe.products, stripe.prices, etc. automatically
```

**Data Creation - Use Stripe API Scripts, NOT SQL:**

```sql
-- WRONG - Inserting Stripe data with SQL
INSERT INTO stripe.products (id, name, description)
VALUES ('prod_123', 'Pro Plan', 'Professional subscription');
```

```typescript
// CORRECT - Use Stripe API in a script
const stripe = await getUncachableStripeClient();
const product = await stripe.products.create({
  name: 'Pro Plan',
  description: 'Professional subscription',
});
// Webhook syncs this to stripe.products automatically
```

**Initialization Order:**

```typescript
// WRONG - Creating StripeSync before migrations
const stripeSync = await getStripeSync();
await runMigrations({ databaseUrl });

// CORRECT - Migrations first, then StripeSync
await runMigrations({ databaseUrl });
const stripeSync = await getStripeSync();
await stripeSync.findOrCreateManagedWebhook(...);
await stripeSync.syncBackfill();
```

**Frontend - Must parse JSON responses:**

```typescript
// WRONG - returns Response object
const response = await apiRequest('POST', '/api/checkout', { priceId });
return response;

// CORRECT - parse to get data
const response = await apiRequest('POST', '/api/checkout', { priceId });
return await response.json();
```

**Backend - Webhook route ordering:**

```typescript
// WRONG - Webhook after express.json()
app.use(express.json());
app.post('/api/stripe/webhook', ...);  // Too late! Body already parsed

// CORRECT - Webhook BEFORE express.json()
app.post('/api/stripe/webhook', express.raw({ type: 'application/json' }),
  async (req, res) => {
    await WebhookHandlers.processWebhook(req.body, sig);
  }
);
app.use(express.json());  // Now apply to other routes
```

## References

- ./references/code-templates.md -- Code file templates for initial Stripe setup. ONLY read this reference when performing initial setup of Stripe in a project that does not already have it configured. Do not read for subsequent modifications, queries, or other Stripe operations.

```

---

## Skill: suggest-new-project

**Path:** `.local/skills/suggest-new-project/SKILL.md`

```markdown
---
name: suggest-new-project
description: This project only supports a single artifact type. If the user asks to create slides, a mobile app, an animation, or a separate website, you MUST read this skill before attempting anything. Do not try to build a different artifact type in this project — read this skill for what to do instead."
---

# Redirect Unsupported Artifact Requests

Agent 4 introduced multi-artifact support, allowing users to build websites, mobile apps, slides, and animations side-by-side in a single project. This project was created before that release and currently supports only one artifact. Multi-artifact support is being brought to existing projects soon, but is not available yet.

## When to Use

When the user asks you to create a **new artifact** that is a different type from the current application. The artifact types are:

- Website (a second, separate web app)
- Mobile app (e.g. an Expo app in a web project)
- Slides (a slide deck / presentation)
- Animation / video

Examples of requests that should trigger this skill:

- "Build me a mobile app" (when the current project is not a mobile app)
- "Create a slide deck"
- "Make me an animation" (when the current project is not an animation)
- "I want to start a new website" (a second, separate site)

## When NOT to Use

- The user wants to add a feature to the existing application (e.g. "add a settings page", "add an admin dashboard", "add dark mode"). These are normal feature requests — implement them.
- The user wants to modify or extend the current app (e.g. "add an API endpoint", "change the landing page"). This is not a new artifact.
- The project is a PNPM workspace or multi-artifact workspace — those support multiple artifacts natively. (This skill is not loaded on those stacks.)

## What to Do

1. Do not attempt to build the new artifact in this project.
2. Explain to the user that multi-artifact support is coming to existing projects soon, and that for now, creating a new project will give them the best experience. Suggested phrasing:
   - "Multi-artifact support is coming to existing projects soon — for now, I'd recommend creating a new project for your [mobile app / slides / etc.] so everything works smoothly."
   - "This project currently supports one artifact. We're working on bringing multi-artifact support to existing projects, but for the best experience right now, let's set up a new project."
3. Generate a clear, descriptive prompt summarizing what the user wants to build. This prompt will be pre-loaded into the new project's creation flow.
4. Call `suggestNewProject({ prompt })` from the code execution sandbox:

   ```javascript
   const result = await suggestNewProject({
     prompt: "Build a mobile workout tracking app with exercise logging, progress charts, and workout history"
   });
   ```

5. If the user dismisses the suggestion: Ask if they'd like to continue working on their existing application. Do not re-suggest unless the user brings it up again.

## If the User Insists

If the user dismisses the suggestion and insists on building the new artifact in this project anyway, do not call `suggestNewProject` again. Instead, warn them in your response that the experience may not work well since this project wasn't set up for multiple artifacts, then attempt their request. Suggested phrasing:

- "I can try, but since this project wasn't set up for multiple artifacts, some things may not work as expected. For the best results, I'd still recommend a new project — but let's give it a shot."

## Important

- Only call `suggestNewProject` once per user request. If they dismiss, do not call it again.
- The prompt you generate should be self-contained — it will be used to bootstrap a brand-new project with no context from this one.
- Keep your explanation concise and forward-looking. Do not call the project "old" or "legacy" to the user.

```

---

## Skill: testing

**Path:** `.local/skills/testing/SKILL.md`

```markdown
---
name: testing
description: Run automated UI tests against your application using a Playwright-based testing subagent. Use after implementing features to verify they work correctly.
---

# Testing Skill

The `runTest` function launches a specialized Playwright-based testing subagent that:

- Interacts with your application in a real browser
- Analyzes both browser and backend logs
- Provides detailed feedback including screenshots and technical diagnostics

End-to-end testing with `runTest()` can uncover bugs not discoverable through conventional testing methods like `curl` or unit tests.

## Building Context for Testing

A good test plan derives from a good contextual understanding of the application. Before writing your test plan:

1. **Understand application context**: Know both the frontend and backend code relevant to your changes
2. **Update documentation**: If you made significant changes, update replit.md to reflect them (the testing subagent has access to it for general context)
3. **Know the navigation**: Understand how to reach the feature you're testing
4. **Identify specifics**: Note relevant UI elements (selectors, labels) and API endpoints involved

If you just implemented a feature, you already have most of this context — use it immediately. If a test fails due to insufficient context, iterate and add more details. If stuck after multiple attempts, stop and ask the user for help.

## When to Use

- You have implemented or modified a feature and want to verify it works
- User flows through the application (login, forms, navigation, modals)
- UI components render and behave correctly, including visual changes (layout, styling)
- Frontend features that depend on JavaScript execution
- End-to-end flows spanning multiple pages or components
- Integrations like Stripe payments or authentication flows

## When NOT to Use

- Unit testing code logic — use standard test frameworks instead. Reserve `runTest()` for e2e validation; reserve unit tests for regressions and backend logic.
- API-only testing without a UI component — use `curl` or standard HTTP clients instead
- When the application is not running or accessible
- Load testing or performance testing

## Available Functions

### runTest

Run UI tests against the application using an automated Playwright-based testing subagent.

**Parameters:**

- `testPlan` (str, required): Description of what to test, including specific steps and expected outcomes
- `relevantTechnicalDocumentation` (str, optional): Technical context like database schema, API routes, or component details
- `defaultScreenWidth` (int, default 1280): Browser viewport width. For mobile, use 400 (Replit mobile webview compatible, only suggested).
- `defaultScreenHeight` (int, default 720): Browser viewport height. For mobile, use 720 (suggested).

**Returns:** Dict with:

- `status`: One of "success", "failure", "unable", "skipped", "blocked", or "error"
- `testOutput`: Detailed test output and observations
- `subagentId`: ID of the testing subagent (for reference)
- `screenshotPaths`: List of local screenshot file paths (e.g. `/tmp/testing-screenshots/<id>.jpeg`)

**Example:**

```javascript
const result = await runTest({
    testPlan: `
        Test the user login flow:
        1. [New Context] Create a new browser context
        2. [Browser] Navigate to the login page (path: /login)
        3. [Browser] Enter "test@example.com" in the email field
        4. [Browser] Enter "password123" in the password field
        5. [Browser] Click the "Sign In" button
        6. [Verify]
            - Assert redirect to the dashboard (path: /dashboard)
            - Assert user name appears in the header
    `,
    relevantTechnicalDocumentation: `
        - Login endpoint: POST /api/auth/login
        - Dashboard route: /dashboard
        - User name displayed in #user-header element
    `
});

if (result.status === 'success') {
    console.log("All tests passed!");
} else if (result.status === 'failure') {
    console.log("Tests failed");
    console.log(result.testOutput);
    for (const screenshotPath of result.screenshotPaths) {
        console.log(`See screenshot: ${screenshotPath}`);
    }
}
```

## Writing Effective Test Plans

Batch multiple `[Verify]` checks on the same page together when no actions occur between them. But if `[Browser]`, `[API]`, or `[DB]` steps occur between verifications, keep them in separate `[Verify]` blocks — verifications should be read-only blocks without side effects.

For UI testing, explicitly include interactions like hover effects, dialogs, modals, tooltips, dropdowns, and animations — the testing agent sometimes needs special handling for these (e.g., being told to dismiss a dialog before clicking).

### Best Practices

1. **Test one flow at a time**: Keep test plans focused on a single user journey
2. **Include expected outcomes**: Specify what success looks like — "A success toast should appear with message 'Saved!'"
3. **Provide technical context**: Include relevant DB schemas, API endpoints, CSS selectors, and auth requirements in `relevantTechnicalDocumentation`
4. **Specify test data**: Provide actual values to use, not placeholders
5. **Handle authentication**: If the app requires login, include login steps first
6. **Include setup steps**: If the test needs data to exist, explain how to create it

## Application State

The testing environment uses the **same development database** as you and the user. The application is not in a fresh state — it may contain existing data from prior usage.

- **Don't assume specific counts** — tests that assert "there are exactly 3 products" will break if other data exists
- **Don't test empty states** or rely on data you didn't create as part of the test plan
- **Generate unique values** for usernames, emails, titles, etc. using `nanoid` to avoid conflicts across test runs and with user data

## Limitations

- The testing subagent has a maximum number of steps before it needs to report results
- Some complex interactions (drag-and-drop, canvas operations) may be challenging
- Tests cannot access the file system directly
- If the application is not accessible or crashes, tests will report as "unable"

## Example Test Plans

```text
1. [New Context] Create a new browser context
2. [Browser] Navigate to the product page (path: /products)
3. [Browser] Click on the first product link
4. [Verify] Assert redirect to the product page (path: /product/${product1Id})
5. [Verify]
   - Ensure the product title is not too big
   - Ensure the overall color scheme is consistent with the rest of the page
   - Assert there are more than one products
   - Make sure the add to cart button is not hidden behind another element
   - Assert the product name is "Product 1"
6. [Browser] For the next dialog, accept the dialog.
7. [Browser] Click add to cart
8. [Browser] Click on cart
9. [Verify] Assert redirect to the cart page (path: /cart)
10. [Verify] Assert cart has the product displayed
```

```text
1. [New Context] Create a new browser context
2. [API] Create a new product by POST to the /api/products endpoint with a randomly generated product name (say ${product_name}), and price 100. Note the name and the id of the created product.
3. [Browser] Navigate to the product page (path: /products)
4. [Verify]
   - Ensure there is at least one product displayed
   - Assert the product name is "${product_name}"
   - Assert the product price is 100
```

```text
1. [New Context] Create a new browser context
2. [Browser] Navigate to the homepage (path: /)
3. [Browser] Enter a TODO list item with a randomly generated title ${nanoid(6)}. Note the title (say ${todo_title}) for future use.
4. [Browser] Click the add todo button
5. [Verify] Assert that the TODO list item is displayed with the title ${todo_title}
```

## Database Testing

If the application uses a database and you need to inject data, set roles, or verify DB state during tests, see `database-testing.md` for how to use `[DB]` steps in test plans.

## External Services

If the application connects to external services, be mindful of side effects. Clean up resources created during tests, and limit notifications sent to third parties. Balance thorough testing with responsible use of external services.

## Replit Auth

If the application uses Replit's OIDC auth — typically indicated by `javascript_log_in_with_replit` or `python_log_in_with_replit` in `.replit`, the presence of `replitAuth.ts` / `replit_auth.py`, `@workspace/replit-auth-web`, references to `replit.com/oidc`, or any other use of Replit's OIDC service — you *must* read `replit-auth.md` (in the same directory as this file) for how to handle programmatic login in test plans. Failing to do so when Replit Auth is part of the test flow will cause auth-related test failures and user frustration.


```

---

## Skill: validation

**Path:** `.local/skills/validation/SKILL.md`

```markdown
---
name: validation
description: Register shell commands as named validation steps (like CI checks) that can be triggered and monitored to verify code quality.
---

# Validation Skill

Set up named validation commands (lint, test, typecheck, etc.) that act as repeatable CI-style checks for the project, then run and monitor them.

## When to Use

- After building new functionality or making significant changes
- When setting up a project's quality gates for the first time
- When the validation command for a check needs to change (e.g., new test framework)
- To run validation commands and check their results
- To monitor the status of ongoing or past validation runs

## When NOT to Use

- For one-off test runs — use the shell directly
- For deploy workflows — use the deployment skill

## Available Functions

### setValidationCommand(name, command)

Create or update a named validation command. If a validation with the same name already exists, it is silently updated (upsert behavior).

**Parameters:**

| Parameter | Type   | Description                                           |
|-----------|--------|-------------------------------------------------------|
| `name`    | string | Short lowercase identifier (e.g., `lint`, `test`)     |
| `command` | string | Shell command to run for this validation               |

**Returns:** `{ success: true, name: string, command: string }`

**Example:**

```javascript
await setValidationCommand({ name: "lint", command: "npm run lint" });
await setValidationCommand({ name: "test", command: "npm test" });
```

### clearValidationCommand(name)

Remove a previously registered validation command.

**Parameters:**

| Parameter | Type   | Description                                      |
|-----------|--------|--------------------------------------------------|
| `name`    | string | Name of the validation command to remove          |

**Returns:** `{ success: true, name: string }`

**Example:**

```javascript
await clearValidationCommand({ name: "lint" });
```

### getValidationCommands()

List all registered validation commands.

**Parameters:** None

**Returns:** `{ workflows: [{ name: string, tasks: [...], ... }] }`

**Example:**

```javascript
const commands = await getValidationCommands();
```

### startValidationRun(commandIds)

Start a validation run that executes one or more registered validation commands.

**Parameters:**

| Parameter    | Type     | Description                                          |
|--------------|----------|------------------------------------------------------|
| `commandIds` | string[] | List of validation command IDs to run                 |

**Returns:**

```json
{
  "runId": "run-abc123",
  "status": "FAILED",
  "commands": [
    {
      "commandId": "lint",
      "shell": "npm run lint",
      "status": "FAILED",
      "exitCode": 1,
      "errorMessage": "Exited with: 1",
      "executionId": "exec-1",
      "durationMs": 3200,
      "logFilePath": "/tmp/validation/lint.log"
    },
    {
      "commandId": "test",
      "shell": "npm test",
      "status": "PASSED",
      "exitCode": 0,
      "errorMessage": "",
      "executionId": "exec-2",
      "durationMs": 5100,
      "logFilePath": "/tmp/validation/test.log"
    }
  ],
  "durationMs": 8300,
  "errorMessage": "",
  "runSummary": "- `npm run lint` FAILED (exit code 1): ESLint reported ..."
}
```

- `status` is one of: `"RUNNING"`, `"PASSED"`, `"FAILED"`, `"STOPPED"`, `"ERROR"`, `"TIMED_OUT"`
- `runSummary` is an LLM-generated breakdown of the results with log line citations. Use it to understand what failed without reading full logs.
- Each command includes `logFilePath` pointing to the full output log.

**Example:**

```javascript
await setValidationCommand({ name: "lint", command: "npm run lint" });
await setValidationCommand({ name: "test", command: "npm test" });
const run = await startValidationRun({ commandIds: ["lint", "test"] });

if (run.status !== "PASSED") {
  // run.runSummary explains what failed and cites log lines
  console.log(run.runSummary);

  // Inspect individual commands
  for (const cmd of run.commands) {
    if (cmd.status !== "PASSED") {
      console.log(`${cmd.shell} failed (exit ${cmd.exitCode}): ${cmd.errorMessage}`);
      console.log(`Full log: ${cmd.logFilePath}`);
    }
  }
}
```

### stopValidationRun(runId, graceful?)

Stop a running validation run.

**Parameters:**

| Parameter  | Type    | Description                                       |
|------------|---------|---------------------------------------------------|
| `runId`    | string  | ID of the validation run to stop                   |
| `graceful` | boolean | Whether to stop gracefully (default: `true`)       |

**Returns:** `{ success: true, runId: string }`

**Example:**

```javascript
await stopValidationRun({ runId: "run-abc123" });
await stopValidationRun({ runId: "run-abc123", graceful: false });
```

### getValidationRun(runId)

Get the status and details of a specific validation run, including per-command results.

**Parameters:**

| Parameter | Type   | Description                                      |
|-----------|--------|--------------------------------------------------|
| `runId`   | string | ID of the validation run to retrieve              |

**Returns:** `{ validationRun: { id, status, startedAt, durationMs, commands: [...] } }`

**Example:**

```javascript
const run = await getValidationRun({ runId: "run-abc123" });
// run.validationRun.status is one of: "RUNNING", "PASSED", "FAILED", "STOPPED", "ERROR"
```

### getValidationRuns()

Get all validation runs.

**Parameters:** None

**Returns:** `{ validationRuns: [{ id, status, startedAt, durationMs, commands: [...] }] }`

**Example:**

```javascript
const runs = await getValidationRuns();
```

## Conventional Names and Commands

Use short, lowercase names. Here are common conventions by stack:

| Name        | Node.js              | Python                    | Go                  |
|-------------|----------------------|---------------------------|---------------------|
| `lint`      | `npm run lint`       | `ruff check .`            | `golangci-lint run` |
| `test`      | `npm test`           | `pytest`                  | `go test ./...`     |
| `typecheck` | `npx tsc --noEmit`   | `mypy .`                  | `go vet ./...`      |
| `format`    | `npx prettier --check .` | `ruff format --check .` | `gofmt -l .`       |

## Example Workflow

After implementing a feature in a Node.js project:

```javascript
// Set up validation commands for the project
await setValidationCommand({ name: "lint", command: "npm run lint" });
await setValidationCommand({ name: "test", command: "npm test" });
await setValidationCommand({ name: "typecheck", command: "npx tsc --noEmit" });

// Run all validations (blocks until complete)
const run = await startValidationRun({ commandIds: ["lint", "test", "typecheck"] });

if (run.status !== "PASSED") {
  // runSummary explains failures with log line citations
  console.log(run.runSummary);

  for (const cmd of run.commands) {
    if (cmd.status !== "PASSED") {
      console.log(`${cmd.shell} failed (exit ${cmd.exitCode}): ${cmd.errorMessage}`);
      console.log(`Full log: ${cmd.logFilePath}`);
    }
  }
}

// Or fetch it again later by ID
const result = await getValidationRun({ runId: run.runId });
```

```

---

## Skill: web-search

**Path:** `.local/skills/web-search/SKILL.md`

```markdown
---
name: web-search
description: Search the web and fetch content from URLs. Use for real-time information, API documentation, and current events.
---

# Web Search Skill

Search the web and retrieve content from URLs for current information.

## When to Use

Use this skill when:

- You need real-time information (news, prices, events)
- Looking up API documentation or SDK guides
- Accessing current technical information beyond training data
- Verifying facts from authoritative sources

## When NOT to Use

- Replit-specific features (use the replit-docs skill)
- Image/media downloads (use media-generation skill)
- Code search within the project (use grep/glob tools)

## Available Functions

### webSearch(query)

Search the web for current information.

**Parameters:**

- `query` (str, required): Natural language search query phrased as a complete question

**Returns:** Dict with `searchAnswer` and `resultPages` (list of title/url dicts)

**Example:**

```javascript
const results = await webSearch({ query: "OpenAI API rate limits 2026" });
console.log(results.searchAnswer);
for (const page of results.resultPages) {
    console.log(`${page.title}: ${page.url}`);
}
```

### webFetch(url)

Fetch and extract content from a URL as markdown.

**Parameters:**

- `url` (str, required): Full HTTPS URL to fetch

**Returns:** Dict with `markdown` key containing page content

**Example:**

```javascript
const content = await webFetch({ url: "https://platform.openai.com/docs/guides/rate-limits" });
console.log(content.markdown.slice(0, 1000));
```

## Best Practices

1. **Use natural language queries**: Write queries as complete questions with context
2. **Chain search and fetch**: Search first, then fetch specific pages for details
3. **Be specific**: Include dates, versions, or other specifics in queries
4. **Verify with fetch**: Don't rely only on search snippets for critical information

## Example Workflow

```javascript
// Find information about a topic
const searchResults = await webSearch({ query: "FastAPI dependency injection tutorial 2026" });

// Get full content from the most relevant result
if (searchResults.resultPages.length > 0) {
    const bestUrl = searchResults.resultPages[0].url;
    const fullContent = await webFetch({ url: bestUrl });
    console.log(fullContent.markdown);
}
```

## Limitations

- Cannot access social media platforms (LinkedIn, Twitter, Instagram, Facebook, Reddit, YouTube)
- Cannot download media files (images, videos, audio)
- Paywalled or authenticated content may be inaccessible

## Copyright

- Respect copyright for media content from websites
- You can reference or link to public content
- Do not copy media files (images, videos, audio) directly from websites
- Use the media-generation skill for images and videos instead

```

---

## Skill: workflows

**Path:** `.local/skills/workflows/SKILL.md`

```markdown
---
name: workflows
description: Manage application workflows including configuration, restart, and removal.
---

## Overview

A workflow binds a shell command (e.g., `npm run dev`, `python run.py`, `cargo run`) to a long-running task managed by Replit. Workflows are used to run webservers, background services, TUIs, and other persistent processes.

**Key characteristics:**

- Workflows run until explicitly stopped
- The system tracks workflows automatically — no separate configuration file is required
- Workflows auto-restart after package installation and module installation
- You can only get console logs from a workflow if it is running

## Setup Tips

1. **Keep workflows minimal**: One workflow per project is usually sufficient. Use the main frontend server or TUI as your primary workflow.

2. **Choose the right workflow**: If your project has a frontend or TUI, set the workflow to the process that updates what the user sees.

3. **Clean up unused workflows**: When adding new workflows, remove any existing workflows that are no longer needed.

4. **Always restart after changes**: Restart workflows after making server-side code changes to ensure updates are visible to the user. Verify they run without errors before returning to the user.

5. **Use bash for one-off commands**: Workflows are for persistent processes. Use bash for build scripts, testing, or commands that don't need to keep running.

## When to Use

Use this skill when:

- You need to create or configure a workflow (background process)
- You need to restart the application after making code changes
- The application needs to be restarted to pick up new environment variables
- You need to remove a workflow that's no longer needed
- The user asks to start, stop, or restart the application
- You need to check what workflows are configured
- You need to check workflow status, output, or open ports

## When NOT to Use

- For debugging runtime errors (fix the code first, then restart)
- When the application is already running and changes are hot-reloaded
- One-off commands (use bash for commands that don't need to persist)
- Build scripts (use bash for npm build, webpack, etc.)
- Testing commands (use bash or runTest callback)
- More than 10 workflows (keep workflows minimal; combine services if needed)

## Available Functions

### listWorkflows()

List all configured workflows with their current state.

**Parameters:** None

**Returns:** List of workflow info dicts with `name` (str), `command` (str), and `state` ("not_started", "running", "finished", "failed").

**Example:**

```javascript
const workflows = await listWorkflows();
for (const w of workflows) {
    console.log(`${w.name}: ${w.state}`);
}
```

### getWorkflowStatus(name, maxScrollbackLines)

Get detailed status of a specific workflow including output logs and open ports.

**Parameters:**

- `name` (str, required): Name of the workflow to check
- `maxScrollbackLines` (int, default 100): Number of output lines to include

**Returns:** Dict with `name`, `command`, `state`, `output` (recent terminal output), `openPorts` (list of listening ports), and `waitForPort`.

**Example:**

```javascript
// Check if the server is running and see its output
const status = await getWorkflowStatus({ name: "Start application" });
console.log(`State: ${status.state}`);
if (status.output) {
    console.log(`Output:\n${status.output}`);
}
if (status.openPorts) {
    console.log(`Listening on ports: ${status.openPorts}`);
}
```

### configureWorkflow({ name, command, waitForPort, outputType, autoStart, isCanvasWorkflow })

Configure or create a workflow. This is the primary way to set up background processes.

**Parameters:**

- `name` (str, default "Start application"): Unique workflow identifier
- `command` (str, required): Shell command to execute
- `waitForPort` (int, optional): Port the process listens on
- `outputType` (str, default "webview"): "webview", "console", or "vnc"
- `autoStart` (bool, default True): Auto-start after configuration
- `isCanvasWorkflow` (bool, default false): Whether this workflow serves canvas iframe content

**Output Type Rules:**

- **webview** - For web applications. MUST use port 5000.
- **console** - For backend services, CLIs, TUIs. Can use any supported port.
- **vnc** - For desktop/GUI apps (Electron, PyQt, etc.). No port needed.

**Supported Ports:** 3000, 3001, 3002, 3003, 4200, 5000 (webview only), 5173, 6000, 6800, 8000, 8008, 8080, 8099, 9000

**Examples:**

```javascript
// Web application (React, Next.js, etc.)
await configureWorkflow({
    name: "Start application",
    command: "npm run dev",
    waitForPort: 5000,
    outputType: "webview"
});

// Backend API
await configureWorkflow({
    name: "Backend API",
    command: "python api.py",
    waitForPort: 8000,
    outputType: "console"
});

// Desktop application
await configureWorkflow({
    name: "Desktop App",
    command: "python gui_app.py",
    outputType: "vnc"
});
```


### removeWorkflow(name)

Remove a workflow by name. Automatically stops it if running.

**Parameters:**

- `name` (str, required): Name of the workflow to remove

**Returns:** Dict with `success`, `message`, `workflowName`, and `wasRunning`

**Example:**

```javascript
await removeWorkflow({ name: "Backend API" });
```

### restartWorkflow(workflowName, timeout)

Restart a workflow by name.

**Parameters:**

- `workflowName` (str, required): Name of the workflow (e.g., "Start application")
- `timeout` (int, default 30): Timeout in seconds to wait for restart

**Returns:** Dict with restart status and optional screenshot URL

**Example:**

```javascript
// Restart the main application
const result = await restartWorkflow({ workflowName: "Start application" });
console.log(result.message);

// Restart with custom timeout
const result2 = await restartWorkflow({
    workflowName: "Start application",
    timeout: 60
});
```

## Best Practices

1. **Restart after code changes**: Always restart workflows after modifying server-side code
2. **Use appropriate timeouts**: Increase timeout for applications with slow startup
3. **Check logs on failure**: If restart fails, check workflow logs for error details
4. **One restart at a time**: Avoid parallel restarts of the same workflow

5. **Port 5000 for web apps**: Always use port 5000 with webview output type


## Common Workflow Names

- `Start application` - Main application workflow
- `Start Backend` - Backend server (in Expo/mobile apps)
- `Project` - Parent workflow for multi-service apps

## Error Handling

The workflow functions may raise errors in these cases:

- **Workflow not found**: The specified workflow name doesn't exist
- **Port not opened**: The application didn't start listening on expected port
- **Preview not available**: The application endpoint isn't responding with HTTP 200
- **Workflow limit exceeded**: Maximum of 10 workflows reached

- **Port/output type mismatch**: Port 5000 requires webview, webview requires port 5000


When errors occur, check:

1. Workflow logs for error details
2. Application code for startup issues
3. Port configuration in the workflow settings

## Example Workflow

```javascript
// Create a web application workflow
await configureWorkflow({
    name: "Start application",
    command: "npm run dev",

    waitForPort: 5000,

    outputType: "webview"
});

// After making code changes, restart the application
const result = await restartWorkflow({ workflowName: "Start application" });

if (result.success) {
    console.log("Application restarted successfully");
    if (result.screenshotUrl) {
        console.log(`Screenshot: ${result.screenshotUrl}`);
    }
} else {
    console.log(`Restart failed: ${result.message}`);
}

// Clean up unused workflows
await removeWorkflow({ name: "Old Backend" });
```

```

---

