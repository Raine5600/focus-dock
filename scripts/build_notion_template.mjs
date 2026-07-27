#!/usr/bin/env node
/**
 * Builds the Focus Dock Notion template via the Notion API.
 *
 * Creates the 3-database system from the guide inside a page you share
 * with your integration: Brain Dump, Projects, Tasks — including the
 * self-relation, rollups, and Hide/Hide Sequence formulas, plus sample
 * content so buyers see a working system on first open.
 *
 * Usage:
 *   NOTION_TOKEN=secret_xxx NOTION_PAGE_ID=xxxx node scripts/build_notion_template.mjs
 *
 * Setup (one time, ~2 min):
 *   1. notion.so/profile/integrations → New integration → copy the secret
 *   2. Create a blank page in Notion called "Focus Dock"
 *   3. On that page: ••• menu → Connections → add your integration
 *   4. Copy the page ID from the URL (the 32-char hex after the page name)
 *
 * The API cannot create database views. After this script runs, add the
 * "Do This Next" view by hand — the script prints the 4-step checklist.
 */

const TOKEN = process.env.NOTION_TOKEN;
const PAGE_ID = process.env.NOTION_PAGE_ID;

if (!TOKEN || !PAGE_ID) {
  console.error("Set NOTION_TOKEN and NOTION_PAGE_ID env vars. See header comment for setup.");
  process.exit(1);
}

const API = "https://api.notion.com/v1";
const HEADERS = {
  Authorization: `Bearer ${TOKEN}`,
  "Notion-Version": "2022-06-28",
  "Content-Type": "application/json",
};

async function notion(method, path, body) {
  const res = await fetch(`${API}${path}`, {
    method,
    headers: HEADERS,
    body: body ? JSON.stringify(body) : undefined,
  });
  const json = await res.json();
  if (!res.ok) {
    throw new Error(`${method} ${path} → ${res.status}: ${json.message ?? JSON.stringify(json)}`);
  }
  return json;
}

const title = (text) => [{ type: "text", text: { content: text } }];

async function main() {
  console.log("Building Focus Dock template…\n");

  // ---- 1. Projects -------------------------------------------------------
  const projects = await notion("POST", "/databases", {
    parent: { type: "page_id", page_id: PAGE_ID },
    title: title("Projects"),
    icon: { type: "emoji", emoji: "🗂️" },
    properties: {
      Name: { title: {} },
      Status: {
        select: {
          options: [
            { name: "Active", color: "green" },
            { name: "Someday", color: "yellow" },
            { name: "Done", color: "gray" },
          ],
        },
      },
      Notes: { rich_text: {} },
    },
  });
  console.log("✓ Projects database");

  // ---- 2. Brain Dump -----------------------------------------------------
  const brainDump = await notion("POST", "/databases", {
    parent: { type: "page_id", page_id: PAGE_ID },
    title: title("Brain Dump"),
    icon: { type: "emoji", emoji: "🧠" },
    properties: {
      Name: { title: {} },
      Status: {
        select: {
          options: [
            { name: "To Sort", color: "orange" },
            { name: "Sorted", color: "gray" },
          ],
        },
      },
      Added: { created_time: {} },
    },
  });
  console.log("✓ Brain Dump database");

  // ---- 3. Tasks (base properties first) ----------------------------------
  const tasks = await notion("POST", "/databases", {
    parent: { type: "page_id", page_id: PAGE_ID },
    title: title("Tasks"),
    icon: { type: "emoji", emoji: "✅" },
    properties: {
      Name: { title: {} },
      Done: { checkbox: {} },
      Due: { date: {} },
      Project: {
        relation: { database_id: projects.id, single_property: {} },
      },
    },
  });
  console.log("✓ Tasks database (base properties)");

  // ---- 4. Self-relation: Task Before -------------------------------------
  await notion("PATCH", `/databases/${tasks.id}`, {
    properties: {
      "Task Before": {
        relation: { database_id: tasks.id, single_property: {} },
      },
    },
  });
  console.log("✓ Task Before self-relation");

  // ---- 5. Rollups (must exist before the formulas that read them) --------
  await notion("PATCH", `/databases/${tasks.id}`, {
    properties: {
      "Before Done": {
        rollup: {
          relation_property_name: "Task Before",
          rollup_property_name: "Done",
          function: "checked",
        },
      },
      "Before Due": {
        rollup: {
          relation_property_name: "Task Before",
          rollup_property_name: "Due",
          function: "latest_date",
        },
      },
    },
  });
  console.log("✓ Before Done / Before Due rollups");

  // ---- 6. Formulas (exact text from Focus_Dock_Formulas.txt) -------------
  // Note: rollups need a moment to register before formulas can reference
  // them, and the API rejects formulas that reference other formula
  // properties — so Hide repeats the full expression instead of the
  // guide's prop("Hide Sequence") pass-through. Behavior is identical.
  const HIDE_EXPR =
    'if(empty(prop("Task Before")), false, if(prop("Before Done") > 0, false, if(prop("Due") < prop("Before Due"), false, true)))';

  async function patchFormulaWithRetry(name, expression) {
    for (let attempt = 1; attempt <= 5; attempt++) {
      try {
        await notion("PATCH", `/databases/${tasks.id}`, {
          properties: { [name]: { formula: { expression } } },
        });
        return;
      } catch (err) {
        if (attempt === 5 || !err.message.includes("Type error")) throw err;
        await new Promise((r) => setTimeout(r, 2000));
      }
    }
  }

  await patchFormulaWithRetry("Hide Sequence", HIDE_EXPR);
  await patchFormulaWithRetry("Hide", HIDE_EXPR);
  console.log("✓ Hide Sequence / Hide formulas");

  // ---- 7. Sample content --------------------------------------------------
  const sampleProject = await notion("POST", "/pages", {
    parent: { database_id: projects.id },
    properties: {
      Name: { title: title("Clean kitchen") },
      Status: { select: { name: "Active" } },
      Notes: { rich_text: title("Sample project — replace with your own.") },
    },
  });

  const today = new Date().toISOString().slice(0, 10);
  const tomorrow = new Date(Date.now() + 86400000).toISOString().slice(0, 10);

  const firstTask = await notion("POST", "/pages", {
    parent: { database_id: tasks.id },
    properties: {
      Name: { title: title("Put 3 dishes in the sink") },
      Due: { date: { start: today } },
      Project: { relation: [{ id: sampleProject.id }] },
    },
  });

  await notion("POST", "/pages", {
    parent: { database_id: tasks.id },
    properties: {
      Name: { title: title("Wipe the counter") },
      Due: { date: { start: tomorrow } },
      Project: { relation: [{ id: sampleProject.id }] },
      "Task Before": { relation: [{ id: firstTask.id }] },
    },
  });

  for (const item of ["call dentist", "email boss", "buy milk"]) {
    await notion("POST", "/pages", {
      parent: { database_id: brainDump.id },
      properties: {
        Name: { title: title(item) },
        Status: { select: { name: "To Sort" } },
      },
    });
  }
  console.log("✓ Sample content (1 project, 2 sequenced tasks, 3 brain dump items)");

  // ---- Done ---------------------------------------------------------------
  console.log(`
Done! Open the page in Notion. Remaining manual steps (~2 min):

  1. Open the Tasks database → click "+ Add a view" → Table
  2. Name it "Do This Next"
  3. Filter: Hide is unchecked  AND  Done is unchecked
  4. Sort: Due ascending

Then hide the helper columns in that view (Hide, Hide Sequence,
Before Done, Before Due) so buyers see a clean board.

To sell it: Share → Publish → tick "Allow duplicate as template".
That published URL is your product link.
`);
}

main().catch((err) => {
  console.error("\n✗ " + err.message);
  process.exit(1);
});
