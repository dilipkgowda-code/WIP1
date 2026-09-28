// Static smoke checks for the local WIP HTML prototype flow.
// Run from the project directory: node test_wip_flow.cjs
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');

const root = __dirname;
const read = (file) => fs.readFileSync(path.join(root, file), 'utf8');
const hub = read('wip_app.html');
const hiring = read('wip_hiring_jobs.html');
const learning = read('wip_learning_portal.html');

// Every relative HTML link exposed by the hub must resolve to a file.
const links = [...hub.matchAll(/href="([^"]+\.html)(?:\?[^"]*)?"/g)].map((m) => decodeURIComponent(m[1]));
assert.ok(links.length >= 8, `Expected the role routes and prototype links; found ${links.length}`);
for (const link of links) assert.ok(fs.existsSync(path.join(root, link)), `Missing linked page: ${link}`);

// The three primary role cards must lead to their expected screens.
assert.match(hub, /href="wip_hiring_jobs\.html"/);
assert.match(hub, /href="wip_learning_portal\.html\?launch=candidate"/);
assert.match(hub, /href="wip_learning_portal\.html\?launch=assessor"/);
assert.match(hiring, /id="job-list"/);
assert.match(learning, /const launchRole=new URLSearchParams\(location\.search\)\.get\("launch"\)/);
assert.match(learning, /if\(launchRole==="candidate"\|\|launchRole==="assessor"\)/);
assert.match(learning, /location\.href="wip_app\.html"/);

// Parse each inline script without running it or touching browser state.
for (const file of ['wip_app.html', 'wip_hiring_jobs.html', 'wip_learning_portal.html']) {
  const html = read(file);
  const scripts = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)];
  for (const [index, match] of scripts.entries()) {
    try {
      new Function(match[1]);
    } catch (error) {
      throw new Error(`${file} inline script ${index + 1} has a syntax error: ${error.message}`);
    }
  }
}

console.log(`WIP flow smoke checks passed (${links.length} hub links, role routing, inline JavaScript syntax).`);
