---
description: "Smart intake for the Obsidian vault — captures memory dumps, content ideas, wins, finance entries, crypto transactions, or raw articles. Asks clarifying questions to determine the right folder and frontmatter, then optionally triggers wiki ingest. Use when user says /addToVault, 'add to vault', 'log this', 'capture this', 'save this to vault', or wants to quickly add something to their Obsidian vault."
argument-hint: "[description of what to add]"
allowed-tools: ["Read", "Write", "Edit", "Glob", "Bash"]
---

# Add to Vault

Smart intake skill for the Obsidian vault. Determines what type of content the user wants to capture, asks clarifying questions, creates the note in the right location with proper frontmatter, and optionally triggers wiki ingest.

## Vault Location

`~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Obsidian Vault/`

## Step 1: Determine Content Type

If the user provides a description, classify it. If unclear, ask:

> "What are you capturing?"
> 1. **Memory dump** — braindump about work, ideas, decisions
> 2. **Content idea** — YouTube/Instagram/LinkedIn content
> 3. **Win** — achievement worth logging for social proof
> 4. **Finance** — income, expense, or donation
> 5. **Crypto transaction** — on-chain transaction
> 6. **Raw article/resource** — external content to save
> 7. **Something else** — describe it

## Step 2: Ask Type-Specific Questions

### Memory Dump
- **Required:** Topic/title
- **Ask if unclear:** Related project? (Agape/Pebbo/general)
- **Tags?**
- **Destination:** `06-Logs/Memory Dumps/YYYY-MM-DD {Topic}.md`
- **Frontmatter:**
  ```yaml
  type: memory_dump
  date: YYYY-MM-DD
  created: YYYY-MM-DD
  tags: [project, topic]
  ```

### Content Idea
- **Required:** The idea/hook
- **Ask:** Platform? (youtube/instagram/linkedin/multi)
- **Ask:** Status? (idea/draft/ready) — default: idea
- **Tags?**
- **Destination:** `06-Logs/Content/YYYY-MM-DD {Description}.md`
- **Frontmatter:**
  ```yaml
  type: content_idea
  date: YYYY-MM-DD
  platform: youtube | instagram | linkedin | multi
  status: idea | draft | ready | posted
  tags: [topic1, topic2]
  ```

### Win
- **Required:** What was the win?
- **Ask:** Context/details?
- **Ask:** Social hook (one-liner for posts)?
- **Action:** Append row to `06-Logs/Wins log.md`:
  `| YYYY-MM-DD | {win} | {context} | {hook} | — |`
- **No separate file needed** unless user wants a detailed note (use `02-Templates/Win.md` pattern)

### Finance (Income/Expense/Donation)
- **Required:** Amount, currency
- **Ask:** Direction? (in/out)
- **Ask:** Source/recipient?
- **Ask if income:** Channel? (bank/crypto), Source? (Agape/Pebbo/Wasiu)
- **Ask if donation:** Type? (relative/charity/zakat)
- **Follow the 3-step sync** from CLAUDE.md:
  1. Add to Income log
  2. If USD/crypto → Payment and income summary
  3. If Agape → Agape income (INR)
- **For donations:** Append to `06-Logs/Finance/Donations log.md`
- **For expenses:** Create note in `06-Logs/Finance/` with finance_tx frontmatter

### Crypto Transaction
- **Required:** Chain, amount, direction (in/out/swap)
- **Ask:** Wallet? (show list from `08-Wallets/`)
- **Ask:** Tx hash?
- **Ask:** Purpose/counterparty?
- **Destination:** `06-Logs/Crypto/YYYY-MM-DD {Description}.md`
- **Frontmatter:**
  ```yaml
  type: crypto_tx
  date: YYYY-MM-DD
  chain: ethereum | solana | tron | bsc | sui
  direction: in | out | swap
  asset: USDT | ETH | SOL | etc
  amount: number
  wallet: "[[08-Wallets/wallet-name]]"
  tx_hash: "0x..."
  ```
- **If income:** Also trigger the finance 3-step sync

### Raw Article/Resource
- **Required:** Content or URL
- **Ask:** Category? (article/research/data)
- **Destination:** `raw/articles/YYYY-MM-DD {Title}.md` or `raw/research/` or `raw/data/`
- **No frontmatter required** — raw sources are immutable

### Something Else
- Ask what it is and where it should go
- Create in `00-Inbox/` if unsure — user can move it later

## Step 3: Create the Note

- Use the Write tool to create the file
- Use proper YYYY-MM-DD naming convention
- Include all determined frontmatter
- Write the content

## Step 4: Offer Wiki Ingest

After creating the note, ask:

> "Note saved to `{path}`. Want me to ingest this into the wiki?"

If yes:
- Read the note
- Create/update relevant wiki pages in `10-Wiki/`
- Update `10-Wiki/index.md`
- Append to `10-Wiki/log.md`

If no:
- Done. Note is saved and can be ingested later.

## Important Rules

- **Indian Financial Year:** April 1 – March 31. For Jan-Mar dates, FY = previous-current year.
- **Finance 3-step sync** is mandatory for income logging. See CLAUDE.md.
- **Never modify dashboard files** — they're Dataview-powered.
- **Use Indian format** in prose (₹12,55,000); raw numbers in tables.
- **Date format:** Always YYYY-MM-DD.
- **Do not delete files** without explicit confirmation.
