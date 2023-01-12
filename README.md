# A Superset of Quartz

Based on the [quartz](https://github.com/jackyzha0/quartz) hugo theme by jackyzha0. 

Existing features:

1. Extremely fast natural-language search
2. Customizable and hackable design based on Hugo
3. Automatically generated backlinks, link previews, and local graph
4. Built-in CJK + Latex Support and Admonition-style callouts
5. Support for both Markdown Links and Wikilinks

Added features:

1. Preprocessing script for better Obsidian valut integration and publishing control (use "publish: true" in yaml frontmatter to whitelist files)
2. Copying attachments from Obsidian to the right place (thereby supporting wikilink without leading folder path)
4. Support wikilink media embed like Obsidian does
5. Some makefile changes for easier testing
6. Updated theme
7. Uses first h1 in markdown as hugo title
8. Postprocessing script to clean up graph so that non-existent links or nodes don't show up

Roadmap:

- [ ] Excalidraw support
- [x] Mermaid support (implemented by [this PR](https://github.com/jackyzha0/quartz/pull/244))
- [x] Fix broken links
- [x] Title generation
- [x] Publishing control
- [x] Fix media embed
- [ ] Fix orphan not showing up (partially fixed)
- [x] Fix Callout behaviour consistency with Obsidian (https://github.com/jackyzha0/quartz/pull/268)
- [x] Don't draw/Draw muted node if file does not exist
- [ ] Custom home page
- [ ] Nav bar
- [ ] Sidenotes
- [x] Table of content on sidebar
- [ ] Obsidian inline tag support
- [x] Pretty calendar embed support
- [ ] Footnotes as sidenotes (inspiration -> https://github.com/capnfabs/paperesque)

---

> “[One] who works with the door open gets all kinds of interruptions, but [they] also occasionally gets clues as to what the world is and what might be important.” — Richard Hamming