import { app } from "/scripts/app.js"; // important: absolute from ComfyUI web root [web:39][web:26]

const BASE_INPUTS = 2;
const PREFIX = "text_";

function isTextInputName(name) {
  return typeof name === "string" && name.startsWith(PREFIX);
}

function getTextInputs(node) {
  return (node.inputs || []).filter(i => isTextInputName(i.name));
}

function hasLink(input) {
  return input && input.link != null;
}

function ensureAtLeastOneFreeTextSlot(node) {
  const textInputs = getTextInputs(node);
  if (!textInputs.length) return;

  const allConnected = textInputs.every(inp => hasLink(inp));
  if (!allConnected) return;

  const nextIndex = textInputs.length + 1;
  node.addInput(`${PREFIX}${nextIndex}`, "STRING");
}

app.registerExtension({
  name: "zveroboy.text_join.dynamic_inputs",

  async nodeCreated(node) {
    if (node.comfyClass !== "TextJoinZveroboy") return;

    // safety: ensure at least base inputs exist
    const existing = new Set((node.inputs || []).map(i => i.name));
    for (let i = 1; i <= BASE_INPUTS; i++) {
      const nm = `${PREFIX}${i}`;
      if (!existing.has(nm)) node.addInput(nm, "STRING");
    }

    const old = node.onConnectionsChange;
    node.onConnectionsChange = function () {
      if (old) old.apply(this, arguments);
      ensureAtLeastOneFreeTextSlot(this);
    };

    ensureAtLeastOneFreeTextSlot(node);
  },
});
