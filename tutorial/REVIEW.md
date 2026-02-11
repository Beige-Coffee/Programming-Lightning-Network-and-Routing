# Tutorial Review: Programming Lightning — Noise Protocol

## 1. Do You Introduce the Essence of the Noise Protocol and ECDH?

### What You Do Well

The overall arc of the tutorial is strong. The progression from TCP/IP foundations through crypto primitives to the Noise handshake acts is logical and well-paced. The dual-perspective approach (showing Alice's steps then Bob's steps) is pedagogically excellent and helps readers internalize why the protocol works. The embedded questions with collapsible answers force active engagement, and the visual diagrams at every step are a major asset.

Your ECDH explanation in `1.4-crypto-review.md` is particularly well done — the historical narrative about Diffie and Hellman gives readers emotional context, and the math (`a × B = a × (b × G)`) is clear and accessible.

### Three Gaps That Should Be Addressed

**Gap 1: Why ECDH? (No Comparative Context)**

You explain *how* ECDH works but never explain *why it was chosen* over alternatives. A student might reasonably ask: "Why not RSA key exchange? Why not just use pre-shared keys?" Consider adding a short paragraph in `1.4-crypto-review.md` after the ECDH explanation covering:

- ECDH is more computationally efficient than RSA for equivalent security levels (smaller keys, faster operations).
- Unlike static Diffie-Hellman, ECDH can be combined with ephemeral key material to provide forward secrecy — each session gets unique keys.
- Unlike pre-shared keys, no out-of-band key distribution is needed.

This doesn't need to be long — just a few sentences comparing alternatives so the reader understands the design choice.

**Gap 2: Why Three ECDH Operations?**

Each individual ECDH operation (`es`, `ee`, `se`) is well-explained within its respective Act, but you never explain the *cumulative* design philosophy — why all three are needed together. Consider adding a preview section in `1.5-noise-overview.md` (before the handshake pattern tables) titled something like "The Three ECDH Operations":

- `es` (ephemeral-static, Act 1): Proves Alice knows Bob's public key. Provides initial key agreement but no forward secrecy on its own — if Bob's static key is later compromised, an attacker could recompute this.
- `ee` (ephemeral-ephemeral, Act 2): Both parties contribute fresh randomness. This is what provides **forward secrecy** — since both ephemeral private keys are deleted after the handshake, no future key compromise can retroactively break this session.
- `se` (static-ephemeral, Act 3): Proves Alice possesses her Static Private Key, completing **mutual authentication**.

By mixing all three into the Chaining Key, the final encryption keys inherit both authentication (from `es` and `se`) and forward secrecy (from `ee`). If any one operation were removed, a security property would be lost.

This "preview" would help readers understand what they're building toward before they encounter each Act in isolation.

**Gap 3: The Handshake Hash / Transcript Is Underexplained Upfront**

You introduce the Handshake Hash in `1.6-noise-setup.md` and call it an "accumulator," which is good. However, the *security purpose* of the transcript isn't made clear until readers encounter it being used as associated data in Act 1. Consider adding a brief "Why the Handshake Hash Matters" explanation in `1.6` (after Step 2) covering:

1. **Synchronization**: If Alice and Bob's hashes diverge at any point (wrong ephemeral key, wrong Noise variant, wrong static key), the MAC verification will fail and the connection is rejected.
2. **Tampering Detection**: The hash is included as associated data in every MAC. If an attacker modifies any message or any prior step, the hash will differ, the MAC will fail, and the connection is rejected.

A concrete failure example would help: "If an attacker intercepted Act 1 and swapped Alice's ephemeral public key for their own, Bob's hash would differ from Alice's, and the MAC verification would fail."

Additionally, you use the word "transcript" for the first time in `1.8-noise-act-2.md` Step 2 ("the handshake hash acts as a **transcript**"), but the concept is already being relied upon in Act 1. Introduce the term "transcript" earlier — in `1.6-noise-setup.md` — so readers have the mental model before they need it.

### Minor Conceptual Suggestions

- In `1.3-authenticated-communication.md`, forward secrecy is introduced only in the context of key ratcheting (every ~1,000 messages). The handshake itself also provides forward secrecy through the `ee` operation, but this isn't mentioned until Act 2. A sentence in `1.3` noting that forward secrecy starts at the handshake level would help.
- In `1.5-noise-overview.md`, the sentence ending "If your bummed that we just glanced over most of the cryptography - don" is incomplete/truncated. This needs to be finished.
- In `1.6-noise-setup.md` Step 4, you explain that Bob's static key is mixed in because "the responder's static key is known ahead of time," but you could strengthen this by adding: this also ensures Alice doesn't accidentally connect to the wrong node, since an incorrect key would cause the hash to diverge.


---

## 2. Formatting Consistency

### Encryption/ChaCha20-Poly1305 Inputs — Inconsistent Bullet vs. Prose

When describing ChaCha20-Poly1305 inputs, some steps use bullet-point lists for the parameters while others use inline prose. For consistency, I'd recommend picking one approach and sticking with it. Given that the tutorial already has detailed visuals, the bullet-point format is clearer for parameter lists.

Files that use **bullet-point lists** for encryption inputs:
- `1.7-noise-act-1.md` Step 5 (Alice Creates MAC): Plaintext, Associated Data, Key, Nonce as bullets
- `1.10-sending-messages.md` Steps 3 & 4: sk, nonce, ad, plaintext as bullets
- `1.11-receiving-messages.md` Step 2: rk, nonce, ad, ciphertext, MAC as bullets

Files that use **inline prose** instead (should be updated to match):
- `1.9-noise-act-3.md` Step 1 (Alice Encrypts Static Public Key): "she will use the ChaCha20-Poly1305 algorithm with `temp_k2`... nonce=1, and the handshake hash as associated data" — all in one sentence, no bullets.
- `1.9-noise-act-3.md` Step 5 (Alice Creates Authentication MAC): Same — prose only.
- `1.11-receiving-messages.md` Step 4 (Decrypt Message): Prose description without parameter bullets.

**Recommendation**: Add bullet-point input lists to the three steps above, matching the format used in `1.7` Step 5 and `1.10` Steps 3-4.

### Act Summary Formatting

- `1.7-noise-act-1.md` and `1.8-noise-act-2.md` use **prose paragraphs** for their Act summaries.
- `1.9-noise-act-3.md` uses a **bullet-point list** for its summary.

**Recommendation**: Make Act 3's summary a prose paragraph to match Acts 1 and 2, or convert Acts 1 and 2 to bullet lists to match Act 3. Since Act 3 covers the most ground, bullet points are arguably the better choice for all three.

### Message Byte Structure Descriptions

The "send" steps are consistent across Acts 1-3 (bullet lists with byte ranges), which is good. However:
- `1.10-sending-messages.md` Step 5 adds a **code block** for the wire format (`lc || MAC1 || c || MAC2`) before the bullet list. The receiving counterpart (`1.11-receiving-messages.md`) does **not** have an equivalent code block showing the expected wire format — it just describes it in prose across Steps 1 and 3.

**Recommendation**: Add a matching wire format code block at the top of `1.11-receiving-messages.md` showing the expected incoming format, so the reader sees the same diagram from the receiver's perspective.

### Bob's Receive Step Formatting (Act 3 vs. Acts 1-2)

In Act 3, the receive step (`1.9` Step 1, Bob Receives 66 Bytes) uses **semantic names** with byte counts in parentheses: "Version (1 byte)", "Encrypted Static Public Key (49 bytes)". Meanwhile, the corresponding send step (`1.9` Step 8) uses **ordinal byte ranges**: "Byte 1", "Bytes 2-50", "Bytes 51-66". Acts 1-2 are more consistent between send/receive. Consider standardizing Act 3 to use the same format for both send and receive.


---

## 3. Cryptographic Terminology Consistency

Below are the terms with inconsistent usage across the tutorial. For each, I recommend a standard form.

### Terms to Standardize

| Term | Variants Found | Recommended Standard |
|------|---------------|---------------------|
| Algorithm name | "ChaCha20-Poly1305" (most files), "ChaCha20Poly-1305" (`1.5`) | **ChaCha20-Poly1305** (hyphenated). Fix the `1.5` instance. |
| Full algorithm name | "Elliptic Curve Diffie-Hellman" (`1.4`), "Elliptic Curve Diffie Hellman" (`1.7`, no hyphen) | **Elliptic Curve Diffie-Hellman** (with hyphen) |
| Associated data | "associated data" (lowercase, most files), "Associated Data" (capitalized, `1.3`, `1.9`) | **associated data** (lowercase) in general usage. Only capitalize when part of the full acronym expansion: "Authenticated Encryption with Associated Data (AEAD)". |
| Auth tag naming | "authentication tag" / "Message Authentication Code" / "MAC" / "authentication tag MAC" / "message authentication code" — used interchangeably | Introduce as **"Message Authentication Code (MAC)"** in `1.4`. After that, use **"MAC"** consistently. Separately, use **"authentication tag"** (lowercase) when referring to the output bytes specifically. Avoid the hybrid "authentication tag MAC". |
| Ephemeral keys | "Ephemeral Public Key" (capitalized in step titles), "ephemeral public key" (lowercase in prose) | **Ephemeral Public Key** / **Ephemeral Private Key** (capitalized) when referring to specific protocol objects. Lowercase "ephemeral key pair" when used conceptually. |
| Static keys | "Static Public Key" (capitalized, most Act files), "static key" (lowercase, `1.5` tables) | **Static Public Key** / **Static Private Key** (capitalized) throughout. Update the `1.5` table entries. |
| Chaining Key | "Chaining Key" (capitalized, most files), occasional "chaining key" (lowercase) | **Chaining Key** (capitalized). Always introduce with variable: "Chaining Key (`ck`)". |
| Handshake Hash | "Handshake Hash" (capitalized in step titles), "handshake hash" (lowercase in prose), generic "hash" | **Handshake Hash** (capitalized) when referring to the state variable. Use "hash" (lowercase) only for generic hash function operations. Introduce with variable: "Handshake Hash (`h`)". |
| Temporary Key | "Temporary Key" / "temporary key" / "temporary encryption key" | **Temporary Key** (capitalized). Reference as "Temporary Key 1 (`temp_k1`)", etc. Avoid "temporary encryption key" variant. |
| Redundant phrasing | "encrypted ciphertext" (`1.9`, Steps 2 and 4) | Just **"ciphertext"** — ciphertext is by definition encrypted, so "encrypted ciphertext" is redundant. |


---

## 4. Code Snippet Consistency

### The Problem

Act 3 (`1.9-noise-act-3.md`) includes inline pseudocode snippets for cryptographic operations, like:

> `se = ECDH(bob_ephemeral_priv, alice_static_pub)`
> `ck, temp_k3 = HKDF(ck, se)`
> `sk, rk = HKDF(ck, "")`

Acts 1 and 2 describe the **same types of operations** purely in prose — no pseudocode at all. For example, Act 1 Step 3 says: "Alice will create an Elliptic Curve Diffie Hellman (ECDH) shared secret using *her* **Ephemeral Private Key** and *Bob's* **Static Public Key**." The reader has to mentally assemble which variables go where.

### Where to Add Snippets

Since the tutorial already has visual diagrams at every step, the inline pseudocode snippets serve as a **quick-reference complement** — they show the "what" in precise terms while the prose explains the "why." I recommend adding them to Acts 1 and 2 for consistency with Act 3.

**Act 1 (`1.7-noise-act-1.md`) — Add snippets to these steps:**

| Step | Operation | Snippet to Add |
|------|-----------|---------------|
| Alice Step 3 | ECDH | `es = ECDH(alice_ephemeral_priv, bob_static_pub)` |
| Alice Step 4 | HKDF | `ck, temp_k1 = HKDF(ck, es)` |
| Bob Step 4 | ECDH | `es = ECDH(bob_static_priv, alice_ephemeral_pub)` |
| Bob Step 5 | HKDF | `ck, temp_k1 = HKDF(ck, es)` |

**Act 2 (`1.8-noise-act-2.md`) — Add snippets to these steps:**

| Step | Operation | Snippet to Add |
|------|-----------|---------------|
| Bob Step 3 | ECDH | `ee = ECDH(bob_ephemeral_priv, alice_ephemeral_pub)` |
| Bob Step 4 | HKDF | `ck, temp_k2 = HKDF(ck, ee)` |
| Alice Step 4 | ECDH | `ee = ECDH(alice_ephemeral_priv, bob_ephemeral_pub)` |
| Alice Step 5 | HKDF | `ck, temp_k2 = HKDF(ck, ee)` |

Use the same inline backtick format that Act 3 uses (not fenced code blocks). This keeps them lightweight and consistent.


---

## 5. Spelling and Typos

Here are all the errors I found across the tutorial files.

### `1.2-network-addresses.md` (referenced as such in file; content is in `1.2`)
| Error | Fix |
|-------|-----|
| "they are actually communication with each other" | "communicating" |
| "Certificate Authority dilema" | "dilemma" |
| "Lightnign developers" | "Lightning" |
| "she has no guarentee" | "guarantee" |
| "Internet Service Provide (ISP)" | "Provider" |
| "authenticate, themselves" (extra comma) | "authenticate themselves" |
| "Since IP address can change" | "IP addresses" (plural) |

### `1.3-authenticated-communication.md`
| Error | Fix |
|-------|-----|
| "By staring with the larger picture" | "starting" |
| "in the propper context" | "proper" |
| "particpants are able to" | "participants" |
| "only the intiator and responder" | "initiator" |
| "identity implicity using" | "implicitly" |
| "providing two critical guarentees" | "guarantees" |

### `1.5-noise-overview.md`
| Error | Fix |
|-------|-----|
| "we revieweved secp256k1" | "reviewed" |
| "it support multiple handshake" | "supports" |
| "To idenfify which flavor" | "identify" |
| "Alice - the initator of this connection" | "initiator" |
| "which effecitvely allow" | "effectively" |
| "If your bummed that..." | "you're" (also sentence is truncated/incomplete) |
| "This handshake patter, known as" | "pattern" |

### `1.7-noise-act-1.md`
| Error | Fix |
|-------|-----|
| "Chaining Key is, as the name suggests, will be a chain" | "The Chaining Key will be a chain" (remove "is, as the name suggests,") |
| "derive the cnryption keys" | "encryption" |
| "the cihertext (`c`)" | "ciphertext" |
| "syncronizing his handshake hash" | "synchronizing" |
| "without publically revealing" | "publicly" |
| "once the comlpete the handshake" | "once they complete the handshake" |

### `1.8-noise-act-2.md`
| Error | Fix |
|-------|-----|
| "Bob will the mix the MAC" | "Bob will mix the MAC" (remove extra "the") |

### `1.9-noise-act-3.md`
| Error | Fix |
|-------|-----|
| "all three ECDH oeprations" | "operations" |
| "handshake state is synconized" | "synchronized" |
| "he can't be sure he actually talking" | "he is actually talking" |
| "someone who know's her Static Private Key" | "knows" (no apostrophe) |

### `1.10-sending-messages.md`
| Error | Fix |
|-------|-----|
| "Alice will calcualte the length" | "calculate" |
| "the encrytpted length" | "encrypted" |

### `1.11-receiving-messages.md`
| Error | Fix |
|-------|-----|
| "Bob is now equiped with" | "equipped" |
| "Bob aborts the connection immedieately" | "immediately" |

### `1.12-rotating-keys.md`
| Error | Fix |
|-------|-----|
| "steps that were take to establish" | "taken" |
| "Once Alice is equpred with" | "equipped" |

### `1.1-lightning-network-graph.md`
| Error | Fix |
|-------|-----|
| "todo?" (line 17) | Placeholder — needs content or removal |
| Bonus question answer: "#### Todo!" | Placeholder — needs content or removal |

### `1.4-crypto-review.md`
| Error | Fix |
|-------|-----|
| "Whitt had an insight" | "Whit" (one 't', matching earlier usage) |


---

## Summary of Priorities

**High Priority (conceptual gaps that affect learning):**
1. Add "Why ECDH?" comparative context in `1.4`
2. Add "Three ECDH Operations" preview in `1.5` explaining what each achieves and why all three are needed
3. Add "Why the Handshake Hash Matters" explanation in `1.6` before the steps
4. Fix the truncated sentence in `1.5`
5. Fix all spelling errors (35 total across all files)

**Medium Priority (consistency issues):**
6. Standardize encryption input formatting (bullet lists everywhere)
7. Standardize terminology per the table above
8. Add inline pseudocode snippets to Acts 1 and 2 matching Act 3's style
9. Standardize Act summary formatting

**Low Priority (polish):**
10. Add wire format code block to `1.11` (receiving) to match `1.10` (sending)
11. Standardize byte-structure formatting between send/receive steps in Act 3
12. Fill in the two "Todo" placeholders in `1.1`
