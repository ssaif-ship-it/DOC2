# Setup, step by step

Written for your actual repo, so you can copy and paste rather than substitute.

| Thing | Your value |
|---|---|
| GitHub repo | `ssaif-ship-it/DOC2` |
| Branch | `main` |
| `index.html` sits at | the repo root |
| Your Pages URL will be | `https://ssaif-ship-it.github.io/DOC2/` |
| Path prefix needed | none, leave it blank |

There is no Cloudflare account, no Worker, and no server of any kind in this version. The page itself talks straight to GitHub. A GitHub token lives inside `index.html`, locked with a password only your team knows. Total time: about 10 minutes.

---

# Part 1: push what is on your Mac (about 3 minutes)

### Step 1. Clean up the leftovers

Two folders are safe to remove, they only hold superseded files: `_to_delete` at the top of the DOC2 folder, and `upi_docs/_to_delete`. Drag both to the Trash in Finder, or from Terminal after Step 2:

```bash
rm -rf _to_delete upi_docs/_to_delete
```

Keep `upi_docs/_archive`. That one is your old drafts, indexed in `_archive/README.md`.

### Step 2. Open Terminal in the folder

```bash
cd "$HOME/Desktop/Cashfree Docs Update/Docs2/DOC2"
```

Check you are in the right place:

```bash
ls
```

You should see: `SETUP.md  build.py  data.csv  index.html  upi_docs`

### Step 3. Commit and push

```bash
git add -A
git commit -m "Renumber sections, add editor with comments and publishing"
git push origin main
```

If `git push` asks for a password, GitHub no longer accepts your account password. Either install [GitHub Desktop](https://desktop.github.com) and push from there, or create the token in Step 7 first and paste that as the password.

### Step 4. Confirm it landed

Open `https://github.com/ssaif-ship-it/DOC2` in your browser. You should see `index.html`, `SETUP.md`, `build.py` and the `upi_docs` folder, with your commit message at the top.

---

# Part 2: turn on GitHub Pages (about 2 minutes)

### Step 5. Enable it

1. Go to `https://github.com/ssaif-ship-it/DOC2/settings/pages`
2. Under **Build and deployment > Source**, choose **Deploy from a branch**
3. Under **Branch**, set the dropdown to **main** and the folder to **/ (root)**
4. Click **Save**

### Step 6. Wait, then open it

Give it 60 to 90 seconds. You can watch progress on the **Actions** tab of the repo. When it is done, open:

```
https://ssaif-ship-it.github.io/DOC2/
```

You should see the docs with the sidebar and a blue **Published copy** badge in the header.

> There is a `.nojekyll` file in the repo. Do not delete it. Without it GitHub tries to run Jekyll over the folder, which hides anything starting with an underscore and can rewrite your `.md` files.

**At this point anybody with that link can read the docs. Nobody can edit. That is correct so far.**

---

# Part 3: turn on editing (about 5 minutes)

This is the only part that used to involve Cloudflare. Now it all happens on the page.

### Step 7. Create a GitHub token

This token is what lets the page save edits. It only ever reaches this one repo, and it lives encrypted inside `index.html`, not on any server.

1. Go to `https://github.com/settings/personal-access-tokens/new`
   (that is Settings > Developer settings > Personal access tokens > Fine-grained tokens > Generate new token)
2. **Token name:** `cashfree-docs-page`
3. **Expiration:** pick the longest your policy allows. Set a calendar reminder to redo this step before it expires, or publishing will start failing.
4. **Resource owner:** leave as your own account, `ssaif-ship-it`
5. **Repository access:** select **Only select repositories**, then in the dropdown pick **DOC2**
6. **Permissions:** expand **Repository permissions**, find **Contents**, and set it to **Read and write**

   Leave every other permission on "No access". Contents is the only one needed.
7. Scroll down, click **Generate token**
8. **Copy the token now.** It starts with `github_pat_`. GitHub shows it exactly once. Paste it somewhere temporary, you need it in the next step.

### Step 8. Encrypt it into the page

1. Open `https://ssaif-ship-it.github.io/DOC2/`
2. Click **Unlock to edit**. Since nothing is set up yet, this opens the **Set up publishing** screen instead.
3. Owner, repository and branch are already filled in correctly. Leave the path prefix blank.
4. Paste the token from Step 7 into **GitHub token**.
5. Type a team password twice. This is what you will give everyone who should be able to edit. Something like `upi-docs-review-2026` rather than a single word. Write it down somewhere you will not lose it.
6. Click **Encrypt and activate**.

The page checks the token against GitHub right there, then encrypts it with your password using your browser's own crypto, nothing sent anywhere else. You are unlocked immediately on this device. A green box appears with one line:

```js
const VAULT = 'v1.600000.....';
```

### Step 9. Make it work for everyone else

Right now only your browser has the encrypted token. Bake it into the file so anyone with the link and the password gets it too.

1. Click **Copy** next to that line.
2. Open `index.html` from your DOC2 folder in a text editor.
3. Search for `const VAULT = '';`. It is near the top of the long script.
4. Replace that whole line with the one you copied.
5. Save, then in Terminal:

   ```bash
   cd "$HOME/Desktop/Cashfree Docs Update/Docs2/DOC2"
   git add index.html
   git commit -m "Turn on editing for the team"
   git push origin main
   ```

6. Wait about a minute for GitHub Pages to rebuild, then reload the page in a private window and confirm **Unlock to edit** now asks for the password instead of reopening setup.

Now everyone who opens the link only needs the password, never a token, never a GitHub account.

---

# Part 4: verify the whole thing (about 2 minutes)

1. Open `https://ssaif-ship-it.github.io/DOC2/` in a **private window**. You should see the docs, a blue **Published copy** badge, and no Edit button. This is what a reader sees.
2. Click **Unlock to edit**, type a name and the password, tick **Stay unlocked on this device**, click **Unlock**. The badge turns green and says **Live**, the button shows your name, and an **Edit Section** button appears.
3. Click **2.1 UPI Intent**, then **Edit Section**. Type a word at the end of the first paragraph.
4. Click **Review & publish**. The diff should show one green `+` line and one red `-` line, and nothing else.
5. Click **Publish**. You should get "Published. Anyone with the link sees this within a minute."
6. Reload the private window after a minute. Your word should be there.

Then undo your test edit the same way, or leave it.

To test comments: select any sentence in the reader, a black **Comment** button appears above it, click it, write something, Post. It shows in the right rail under **Comments** and the sentence turns yellow.

---

# Day to day

**Editing.** Open the link, unlock (once, if you ticked "stay unlocked on this device"), pick a section, **Edit Section**, make changes, **Review & publish**, **Publish**. Live for everyone in under a minute.

If the diff step annoys you, tick **Publish future edits without review** in the review screen. For the rest of that browser tab, the Publish button in the editor commits straight away with no review screen.

**Getting a review.** Send someone this:

> Docs are here: https://ssaif-ship-it.github.io/DOC2/
> To comment, click "Unlock to edit" top right, put your name in and use the password: `<your password>`
> Then just select any text and a Comment button appears. If you want to propose exact wording, tick "Suggest replacement text" and type it. I will apply it from my side.

**Acting on comments.** Open the **Comments** tab in the right rail. Click a comment to jump to the highlighted text. If it has a suggestion, **Apply this change** drops it into the diff and you publish. **Resolve** when done.

**Asking me for changes.** Tell me what you want changed and I will edit the markdown files here and hand them back, same as I have been doing. You commit and push, or I write them to your folder and you push.

---

# Reference

### Changing the password

Open the page while unlocked, click the gear icon, and run through Step 7 and Step 8 again with a new password (you can reuse the same token). Then repeat Step 9 to bake the new line into `index.html` and push. The old password stops working the moment the new line is live. Do this whenever someone leaves the review group.

### Rotating the token

Same as above: generate a fresh token in Step 7, encrypt it with the gear icon, copy the new `VAULT` line into `index.html`, commit and push. Revoke the old token at `https://github.com/settings/tokens?type=beta` once the new one is live.

### Where things are stored

| What | Where |
|---|---|
| Section content | `upi_docs/section_X_Y.md`, one file per section |
| Section order and titles | the `docsState` array inside `index.html` |
| Comments | `upi_docs/_feedback/comments.json`, created on the first comment |
| Old drafts | `upi_docs/_archive/`, not shown anywhere |
| The encrypted token | the `const VAULT = '...';` line inside `index.html` |

Comments are committed to your repo, so they are versioned and survive anyone clearing their browser. Each comment, reply and resolve is one small commit.

### What the password does and does not protect

Be clear eyed about this, since it is the whole trade against the old Cloudflare version. Anyone who has the link and the password can read and write everything the token can reach, which is the `upi_docs` folder and the comments file in this one repo, nothing else on your GitHub account. The password itself is never sent anywhere, it only unlocks the token that is already sitting in the page, so there is nothing for anyone to intercept over the network. The real exposure is the page itself: anyone who saves a copy of `index.html`, or who is handed the password, holds enough to try decrypting the token offline for as long as they like. That is an acceptable trade for an internal testing phase among a small trusted group, and a bad one for anything public or long lived. If this ever needs to be locked down properly, the Cloudflare Worker version keeps the token off the page entirely and is worth revisiting then.

Everything is in git history, so a bad edit is one `git revert` away regardless.

### Adding or reordering sections

Open `index.html`, find the `docsState` array, and add an entry:

```js
{ title: "2.7 Something New", id: "doc-2-7", file: "upi_docs/section_2_7.md" }
```

Keep the three consistent: heading number `2.7`, id `doc-2-7`, filename `section_2_7.md`. Then create the file, commit, push. Or just ask me.

### Editing markdown files by hand

If you edit the `.md` files directly on your Mac rather than through the editor, run this before committing:

```bash
cd "$HOME/Desktop/Cashfree Docs Update/Docs2/DOC2"
python3 build.py
```

That refreshes the offline copy baked into `index.html`, which is only used when someone opens the file straight from Finder with no internet. Skipping it is harmless for the live site.

---

# If something breaks

**Setup says "GitHub rejected the token. It may have expired or been revoked."**
The token is wrong, was revoked, or does not have Contents read and write access to `DOC2`. Generate a new one from Step 7 and try again.

**"Wrong password" and you are certain it is right**
Check for a trailing space when you typed it into the setup screen. If someone changed the password since you last saved the `VAULT` line, you need the latest line from Step 9.

**Unlock keeps asking for setup instead of a password**
That means `const VAULT = '';` in `index.html` is still empty, or the copy on the live Pages site is older than the one you generated. Confirm you pushed and Pages finished rebuilding.

**"Refusing to write ..."**
Working as designed. The page only writes inside `upi_docs/` and the comments file.

**Published, but the public page still shows the old text**
GitHub Pages takes up to a minute to rebuild. While you are unlocked your page reads straight from GitHub so you see changes instantly, readers wait for Pages. Check the repo's **Actions** tab if it takes much longer.

**A comment shows "Text has changed since this comment"**
The sentence it was attached to has been edited or removed, so it cannot be highlighted in place. The comment itself is still in the panel.

**Publish failed and I do not want to lose my work**
You have not lost it. A failed publish saves your edit as a local draft, and the section shows a blue "uncommitted draft" bar. Fix the cause, open the editor again, and publish.

**"Could not save the comment, the file kept changing underneath"**
Two people commented at almost the same second. The page retries automatically a few times; if you still see this, just try the action again.

**"fatal: Unable to create ... .git/index.lock: File exists"**

A stale lock file. Git writes `.git/index.lock` while it works and deletes it when done; if a git process was interrupted, the lock is left behind and blocks every later command. This is a plain Terminal fix on your own Mac, nothing to do with GitHub or the docs page.

First confirm nothing is genuinely running:

```bash
cd "$HOME/Desktop/Cashfree Docs Update/Docs2/DOC2"
ps aux | grep '[g]it ' || echo "No git process running, safe to continue"
```

If that only prints the "safe to continue" message, clear the lock and carry on:

```bash
rm -f .git/index.lock
git status
```

If it does list a git process, close the editor or Git GUI that started it before deleting anything.

**Everything is broken and I want the last good version**
Every publish is a git commit. `https://github.com/ssaif-ship-it/DOC2/commits/main` lists them all, and any one can be reverted from the GitHub UI.
