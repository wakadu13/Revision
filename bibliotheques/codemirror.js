// Bibliothèques de l'éditeur de pages (CodeMirror 6), exposées dans la variable
// globale « CM » et utilisées par wiki/static/wiki/editor.js.
//
// Après une modification de ce fichier ou une mise à jour des paquets :
//   cd bibliotheques && npm ci && npm run build
// puis committer wiki/static/wiki/vendor/codemirror.min.js.

import { StreamLanguage } from "@codemirror/language";
import { javascriptLanguage, typescriptLanguage } from "@codemirror/lang-javascript";
import { cssLanguage } from "@codemirror/lang-css";
import { htmlLanguage } from "@codemirror/lang-html";
import { shell } from "@codemirror/legacy-modes/mode/shell";
import { powerShell } from "@codemirror/legacy-modes/mode/powershell";
import { python } from "@codemirror/legacy-modes/mode/python";
import { standardSQL } from "@codemirror/legacy-modes/mode/sql";
import { yaml } from "@codemirror/legacy-modes/mode/yaml";
import { ruby } from "@codemirror/legacy-modes/mode/ruby";
import { properties } from "@codemirror/legacy-modes/mode/properties";
import { toml } from "@codemirror/legacy-modes/mode/toml";
import { dockerFile } from "@codemirror/legacy-modes/mode/dockerfile";
import { http } from "@codemirror/legacy-modes/mode/http";
import { perl } from "@codemirror/legacy-modes/mode/perl";
import { octave } from "@codemirror/legacy-modes/mode/octave";
import { diff } from "@codemirror/legacy-modes/mode/diff";
import { json } from "@codemirror/legacy-modes/mode/javascript";
import { c, cpp, java, csharp } from "@codemirror/legacy-modes/mode/clike";

export {
  EditorState, EditorSelection, Compartment, Prec, Transaction,
} from "@codemirror/state";
export {
  EditorView, ViewPlugin, Decoration, WidgetType, keymap, drawSelection, dropCursor, placeholder,
} from "@codemirror/view";
export {
  history, historyKeymap, defaultKeymap, indentWithTab, undo, redo,
} from "@codemirror/commands";
export {
  syntaxTree, syntaxHighlighting, HighlightStyle, indentOnInput,
} from "@codemirror/language";
export { markdown, markdownLanguage } from "@codemirror/lang-markdown";
export {
  autocompletion, completionKeymap, closeBrackets, closeBracketsKeymap, startCompletion,
} from "@codemirror/autocomplete";
export {
  search, searchKeymap, highlightSelectionMatches, openSearchPanel,
} from "@codemirror/search";
export { tags, Tag } from "@lezer/highlight";

// Coloration des blocs de code (```bash, ```python...) : langages courants du coffre.
const MODES = {
  shell: [shell, "bash", "sh", "shell", "zsh", "console", "terminal"],
  powershell: [powerShell, "powershell", "ps", "ps1", "pwsh"],
  python: [python, "python", "py", "python3"],
  sql: [standardSQL, "sql", "mysql", "postgresql", "sqlite", "plsql"],
  yaml: [yaml, "yaml", "yml"],
  ruby: [ruby, "ruby", "rb"],
  ini: [properties, "ini", "properties", "conf", "cfg", "apache"],
  toml: [toml, "toml"],
  dockerfile: [dockerFile, "dockerfile", "docker"],
  http: [http, "http"],
  perl: [perl, "perl", "pl"],
  matlab: [octave, "matlab", "octave"],
  diff: [diff, "diff", "patch"],
  json: [json, "json"],
  c: [c, "c", "h"],
  cpp: [cpp, "cpp", "c++", "hpp"],
  java: [java, "java"],
  csharp: [csharp, "csharp", "cs", "c#"],
};
const NATIVE = {
  javascript: javascriptLanguage, js: javascriptLanguage, jsx: javascriptLanguage,
  typescript: typescriptLanguage, ts: typescriptLanguage,
  css: cssLanguage, html: htmlLanguage, xml: htmlLanguage, svg: htmlLanguage, php: htmlLanguage,
};
const cache = {};

export function codeLanguage(info) {
  const name = String(info || "").trim().toLowerCase().split(/[\s{]/)[0];
  if (NATIVE[name]) return NATIVE[name];
  for (const [key, [mode, ...aliases]] of Object.entries(MODES)) {
    if (aliases.includes(name)) return (cache[key] ||= StreamLanguage.define(mode));
  }
  return null;
}
