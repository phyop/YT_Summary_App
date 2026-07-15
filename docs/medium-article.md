# Medium publishing package

## Title options

1. Removing the API Key Barrier: Rebuilding a YouTube Summarizer Around Codex CLI
2. From API Keys to ChatGPT Login: A More Human Onboarding Flow for an AI App
3. What It Took to Make an AI YouTube Summarizer Reproducible After Git Clone
4. Building a Keyless Traditional Chinese YouTube Summarizer with Codex CLI
5. The Hard Part Wasn't Summarization: It Was Authentication, Windows, and Reproducibility

## SEO

- **SEO title:** Build a Keyless YouTube Summarizer with ChatGPT and Codex CLI
- **Meta description:** A practical engineering story about replacing OpenAI API-key onboarding with ChatGPT-authenticated Codex CLI, handling Windows executable conflicts, securing transcript input, and validating a clean-clone setup.
- **URL slug:** `keyless-youtube-summarizer-codex-cli`
- **Tags:** Artificial Intelligence, Python, OpenAI, YouTube, Developer Experience

---

# Removing the API Key Barrier: Rebuilding a YouTube Summarizer Around Codex CLI

The first version of my YouTube summary app worked. A user could paste a video, playlist, or channel URL, press Enter, and receive a well-structured Traditional Chinese summary. The application discovered videos, skipped live streams, retrieved public transcripts, sent them to a model, and displayed the result in a reading-focused interface.

Then I looked at the first-run experience through a non-developer's eyes.

The page asked for an OpenAI API key.

For an engineer who already uses the API platform, that request is ordinary. For a ChatGPT Plus user, it creates an immediate wall. A ChatGPT subscription and API billing are separate products. Someone may have full access to Codex through ChatGPT while having no API key, no API billing setup, and no reason to understand either one. The app had reduced a long video into a short summary, but it had replaced that complexity with an authentication lesson.

I decided to build a second edition around Codex CLI. The goal was not merely to remove a text field. The goal was to make a public repository that another person could clone, launch, authenticate with a ChatGPT account, and use without copying secrets or learning an elaborate setup ritual.

## Start with the official authentication contract

Before changing code, I verified the current Codex behavior against OpenAI's documentation. Codex CLI supports browser-based ChatGPT sign-in through `codex login`. After login, the CLI caches and reuses the session. Non-interactive tasks run through `codex exec`, which prints progress to stderr and the final answer to stdout. A fixed prompt can be supplied as an argument while piped stdin becomes additional context.

That last detail shaped the architecture. The application could keep its summarization instruction under developer control and send transcript JSON through stdin. The user's ChatGPT-managed Codex entitlement would handle model access. No API key would pass through the browser, Flask process, environment file, or Git repository.

This is not offline inference. Transcript text still goes to Codex and OpenAI. The improvement is an authentication and onboarding improvement, not a claim that data never leaves the machine.

## Preserve the working version before replacing anything

The original API implementation had value. Some users prefer explicit API billing, service accounts, or programmatic deployment. Deleting it would turn a product improvement into a compatibility break.

I reorganized the repository into two complete folders. The recommended `codex-cli` folder contains the new ChatGPT-authenticated workflow. The `legacy-api` folder preserves the original implementation. A root README explains the difference before users choose a path.

This structure also improves support. When someone reports a problem, the first question is no longer, "Which authentication method did you configure inside the same code path?" Each edition has a clear contract and independent launcher.

## The Windows executable trap

The first local test exposed a problem that a unit test would not have predicted. The command `codex` existed on the machine, but running it from an external process returned Access Denied. Windows had resolved it to an executable inside the packaged Codex desktop app under WindowsApps. The desktop app could use that binary internally, but a separate Flask application could not assume permission to execute it.

Installing the official npm package produced a working CLI shim under the user's npm directory. Unfortunately, the inaccessible WindowsApps entry still appeared earlier in command discovery. A naive `shutil.which("codex")` implementation would keep selecting the wrong file.

The fix was capability-based discovery rather than path-based trust. The application builds an ordered list of candidates: an explicit `CODEX_CLI_PATH`, the npm shim under the user's application-data directory, the normal PATH result, and finally an `npx` fallback. It executes `--version` on each candidate with a short timeout. Access errors and nonzero exits are skipped. The first candidate that proves it can run becomes the selected CLI.

This small loop is one of the most important pieces of the project. It converts a machine-specific failure into a predictable fallback.

## A launcher should be an onboarding product

The Windows `start.cmd` file now does more than run Python. It checks for Python, creates an isolated virtual environment, installs pinned dependencies, finds a usable Codex CLI, and installs the official `@openai/codex` package when needed. It then runs `codex login status`. If no valid session exists, it starts `codex login` and lets the official browser flow handle credentials.

Only after those steps succeed does the launcher start Flask and open the local page.

Failures are expressed as actions. Missing Python points to the Python download. Missing npm points to Node.js LTS. An interrupted installation asks the user to run the launcher again. The application never asks the user to locate, paste, or save an access token.

There is still a prerequisite boundary. A launcher cannot legally or reliably install every system dependency without consent. Users need Python, internet access, and a ChatGPT workspace with Codex access. Node.js is necessary only when a usable Codex CLI is unavailable. The difference is that these requirements are now detected in sequence instead of being scattered across documentation.

## Treat transcripts as untrusted input

YouTube transcripts are external content. A video could contain sentences that look like instructions to an agent. The transcript should influence the summary, but it should never override the application's task.

The new runner passes a fixed prompt as the `codex exec` argument. That prompt explicitly labels stdin JSON as untrusted material and forbids following instructions found inside transcripts. The transcript bundle is piped separately through stdin.

Codex runs with a read-only sandbox and an ephemeral session. User configuration and project execution rules are ignored for this controlled summarization call. A JSON Schema constrains the final response to an overview and a list of videos, each with a title, summary, three to six points, and a takeaway.

The model handles semantic compression. Ordinary Python code remains responsible for trusted metadata such as original URLs, duration, upload date, and view count. This separation prevents the model from inventing fields the extractor already knows.

## Reproducing the app from a clean clone

Testing the existing development folder is not enough. It may contain a virtual environment, cached packages, CLI credentials, or ignored files that silently make the app work.

I therefore treated clean-clone reproduction as a product requirement. The simulation starts from a new clone, verifies that no `.env`, API key, virtual environment, cache, or credential file is tracked, and builds a fresh Python environment. It installs dependencies from the committed requirements file, runs unit tests and compilation checks, then verifies real YouTube channel discovery and public transcript retrieval.

The test suite mocks model work where appropriate, but a separate authenticated integration test runs a minimal schema-constrained `codex exec` request. That catches command-line flags, login reuse, encoding, output-file handling, and JSON parsing problems that mocks cannot see.

The clean environment also revealed why executable discovery had to test candidates. Reproduction is not just a release ceremony; it is a debugging technique for hidden assumptions.

## Keeping the interface focused

Removing the API key field simplified the page. A status banner now tells the user whether Codex CLI is signed in with ChatGPT. The rest of the interaction stays deliberately small: paste a URL, click the button or press Enter, and read.

The output preserves the editorial hierarchy from the first version: a cross-video overview, numbered video sections, source links, metadata, key points, and a highlighted one-sentence takeaway. The layout remains responsive at mobile width and avoids horizontal overflow.

Good developer experience and good reading experience are related. Both reduce the number of decisions a person must make before reaching value.

## What changed in my view of AI application architecture

This rebuild reinforced several lessons.

First, product access is part of architecture. API keys, subscription entitlements, browser login, and enterprise access tokens are not interchangeable details. Choosing the wrong authentication surface can make a technically correct app unusable for its intended audience.

Second, detect capabilities rather than assuming installation paths. A file can exist and still be unusable. A command can resolve and still fail. Run the smallest safe proof, handle the result, and keep a fallback.

Third, external text is an input security boundary. Prompt injection is not limited to chatbots browsing suspicious websites. A transcript, document, log file, or issue description can contain imperative language. Separate trusted instructions from untrusted context and minimize agent permissions.

Fourth, schema-constrained output is a contract between AI and software. It makes rendering predictable, testing meaningful, and failure visible.

Finally, a public repository is not reproducible because its author can run it. It is reproducible when a new directory, a new environment, and a documented user can reach the same behavior without access to the author's hidden state.

## Remaining limitations and next steps

The app depends on public transcripts. Private videos, regional restrictions, missing captions, and YouTube extraction changes can still block a summary. Codex usage is subject to the signed-in user's plan, workspace policy, and rate limits. Large channels or long transcripts take time.

The next improvements are timestamp citations, transcript caching, Markdown and PDF export, macOS and Linux launchers, and an optional local-model backend. A stronger evaluation set could compare summaries against human-written references and verify that numbers and uncertainty survive compression.

## Conclusion

The visible change was the disappearance of an API key field. The real work happened underneath: choosing the correct authentication surface, preserving the legacy path, handling Windows executable conflicts, constraining an agent, and reproducing the experience from a clean clone.

The resulting application is not configuration-free. No useful local AI tool truly is. It is configuration-light in the places that matter: one launcher, one official browser login, one URL field, and no secret copied into a public project.

That is a better definition of user-friendly AI software than simply making the model call succeed.
