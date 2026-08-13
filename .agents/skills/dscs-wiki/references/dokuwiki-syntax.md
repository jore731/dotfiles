# DokuWiki Markup Syntax Reference

DokuWiki uses its own markup syntax — **not Markdown**. When creating or editing wiki pages via the API, content must be in DokuWiki syntax.

> If the task is **converting** DokuWiki markup to Markdown, use the **doku-to-md** skill instead of doing it manually.

## Headings

```
====== Level 1 (H1) ======
===== Level 2 (H2) =====
==== Level 3 (H3) ====
=== Level 4 (H4) ===
== Level 5 (H5) ==
```

The number of `=` signs **decreases** for deeper headings (opposite of Markdown's `#`). Headings must be the only thing on the line (optional trailing `=` signs are cosmetic).

## Text Formatting

```
**bold**
//italic//
__underlined__
''monospaced''
<del>strikethrough</del>
<sub>subscript</sub>
<sup>superscript</sup>
```

Formatting can be combined: `**__//''bold underlined italic monospaced''//__**`

### Paragraphs and Line Breaks

Blank lines create paragraphs. To force a newline without a paragraph, use two backslashes `\\` followed by a whitespace or end of line:

```
This is some text with some linebreaks\\ Note that the
two backslashes are only recognized at the end of a line\\
or followed by\\ a whitespace \\this happens without it.
```

Use forced newlines sparingly.

## Links

### External Links

URLs are auto-linked. Custom text uses double brackets:

```
http://www.google.com
www.google.com
[[http://www.google.com|This Link points to google]]
```

### Email Links

```
<andi@splitbrain.org>
[[andi@splitbrain.org|Mail me]]
```

### Internal Links

```
[[pagename]]
[[pagename|Link Text]]
[[namespace:pagename]]
[[namespace:pagename|Link Text]]
```

Page names are auto-lowercased; special characters are not allowed.

### Section Links

Link to a specific heading by appending `#section_name`:

```
[[syntax#internal|this Section]]
[[wiki:syntax#tables|Table docs]]
```

### Namespaces in Links

Use colons to navigate namespaces:

```
[[some:namespaces]]            page in a namespace
[[:top-level-page]]            absolute link from root
[[..:sibling-namespace:page]]  relative navigation
```

### Interwiki Links

```
[[wp>DokuWiki]]          Wikipedia
[[doku>syntax]]          DokuWiki.org
```

### Windows Share Links

```
[[\\server\share|this]]
```

### Image Links

Combine link and image syntax to use an image as a link:

```
[[http://php.net|{{wiki:dokuwiki-128.png}}]]
```

Image formatting is the **only** formatting allowed in link names.

## Images and Media

```
{{namespace:image.png}}                       Simple image
{{namespace:image.png|Alt text}}              With alt/caption text
{{namespace:image.png?50}}                    Width 50px
{{namespace:image.png?200x100}}               Width × Height
{{https://example.com/image.png?200x50}}      External image resized
```

### Alignment (controlled by spaces inside braces)

```
{{ image.png}}           Left-aligned  (space before)
{{image.png }}           Right-aligned (space after)
{{ image.png }}          Centered      (spaces both sides)
```

### Link-only (no inline display)

```
{{wiki:dokuwiki-128.png?linkonly}}
```

### Supported Formats

| Type  | Extensions            |
|-------|-----------------------|
| Image | `gif`, `jpg`, `png`   |
| Video | `webm`, `ogv`, `mp4`  |
| Audio | `ogg`, `mp3`, `wav`   |
| Flash | `swf`                 |

Unsupported extensions render as download links. Videos support poster images (same filename, `.jpg` or `.png`).

## Lists

Lines must start with **at least two spaces** followed by `*` (unordered) or `-` (ordered). Deeper nesting uses additional 2-space indents:

```
  * Item 1
  * Item 2
    * Sub-item
  * Item 3

  - First
  - Second
    - Sub-item
  - Third
```

## Tables

### Basic Tables

Headers use `^`, data cells use `|`:

```
^ Heading 1    ^ Heading 2    ^ Heading 3    ^
| Row 1 Col 1  | Row 1 Col 2  | Row 1 Col 3  |
| Row 2 Col 1  | Row 2 Col 2  | Row 2 Col 3  |
```

### Vertical Headers

The cell separator **before** a cell determines its type:

```
|              ^ Heading 1     ^ Heading 2     ^
^ Heading 3    | Row 1 Col 2   | Row 1 Col 3   |
^ Heading 4    | Row 2 Col 2   | Row 2 Col 3   |
```

### Column Span

Leave the next cell empty (but keep the separator):

```
| Spans two columns              || Single col |
```

### Row Span

Use `:::` in cells below the one they should merge into:

```
^ Heading 1    ^ Heading 2                    ^ Heading 3    ^
| Row 1 Col 1  | this cell spans vertically   | Row 1 Col 3  |
| Row 2 Col 1  | :::                          | Row 2 Col 3  |
| Row 3 Col 1  | :::                          | Row 3 Col 3  |
```

### Cell Alignment

Controlled by whitespace — add ≥2 spaces on the opposite side of text:

```
^           Table with alignment           ^^^
|         right|    center    |left          |
|left          |         right|    center    |
```

## Code Blocks

### Inline Code

Use double backticks:

```
This has ``inline code`` in it.
```

### Block Code

```
<code>
Plain code block (no highlighting)
</code>

<code python>
# Syntax-highlighted block (language after tag)
def hello():
    print("Hello!")
</code>
```

Indenting text by ≥2 spaces also creates a code block.

### Downloadable Code Blocks

Add a filename after the language to make blocks downloadable:

```
<file php myexample.php>
<?php echo "hello world!"; ?>
</file>
```

Use a dash for no highlighting: `<code - myfile.foo>`.

## Blockquotes

```
> This is a quote
>> Nested quote
>>> Even deeper
```

## Horizontal Rule

Four or more dashes on their own line:

```
----
```

## Footnotes

```
You can add footnotes ((This is the footnote text)) by using double parentheses.
```

## No-Wiki / Escape Formatting

Prevent DokuWiki from interpreting markup:

```
<nowiki>This **won't** be //formatted//</nowiki>
%%This **also** won't be //formatted//%%
```

## Namespaces

DokuWiki organizes pages into namespaces (like directories):

- `dscs:onboarding` — page `onboarding` in namespace `dscs`
- `dscs:guides:kubernetes` — page `kubernetes` in `dscs:guides`
- Separator is `:` (colon)
- The root namespace is empty string `""`

## Control Macros

```
~~NOTOC~~         Suppress table of contents
~~NOCACHE~~       Disable page caching
```

A TOC is auto-generated when a page has 3+ headings.

## RSS/ATOM Feed Aggregation

Embed external feeds inline:

```
{{rss>http://example.com/feed.rss 5 author date 1h}}
```

Parameters (space-separated after URL): any number (max items, default 8), `reverse`, `author`, `date`, `description`, `nosort`, refresh period (`12h`, `1d`, `30m` — minimum 10m, default 4h).

## Typography Conversions

DokuWiki auto-converts certain character sequences when rendering:

| Source  | Rendered |
|---------|----------|
| `->` | → |
| `<-` | ← |
| `<->` | ↔ |
| `=>` | ⇒ |
| `<=` | ⇐ |
| `<=>` | ⇔ |
| `>>` | » |
| `<<` | « |
| `--` | – (en dash) |
| `---` | — (em dash) |
| `640x480` | 640×480 |
| `(c)` | © |
| `(tm)` | ™ |
| `(r)` | ® |
