<img src="apps/web/public/ad3oni-banner.png" alt="Ad3oni" />

<br/>

# Ad3oni 🙏

Ad3oni is an open-source Islamic system designed to help you stay connected with your daily prayers. It provides prayer reminders through various platforms, including Twitter, a website, and upcoming iOS and Android applications. You can also invite the Ad3oni Discord bot to your server for personalized prayer reminders.

This repository is a Turborepo monorepo that houses the Ad3oni platform: a Next.js web app and a FastAPI backend.

## Table of Contents

- [Tech Stack](#tech-stack-️)
- [Project Structure](#project-structure-)
- [Getting Started](#getting-started-)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the apps](#running-the-apps)
  - [Endpoints](#endpoints)
- [Links](#links-)
- [Developers](#developers-)
- [Contributing](#contributing-)

---

## Tech Stack 🛠️

- **Monorepo**: Turborepo
- **Web**: Next.js (App Router) + TypeScript + Tailwind CSS
- **API**: FastAPI + Uvicorn (Python)
- **Package managers**: Bun (JavaScript) and uv (Python)
- **Dev orchestration**: mprocs

---

## Project Structure 📁

```
ad3oni/
├── apps/
│   ├── web/      Next.js app (App Router, TypeScript, Tailwind)
│   └── api/      FastAPI service (managed with uv)
├── mprocs.yaml   Runs web and api together in development
├── turbo.json    Turborepo task pipeline
└── package.json  Workspaces and root scripts
```

---

## Getting Started 🚀

### Prerequisites

- [Bun](https://bun.sh) (JavaScript runtime and package manager)
- [uv](https://docs.astral.sh/uv/) (Python package and project manager)

### Installation

Clone the repository and install the JavaScript dependencies from the root:

```bash
git clone https://github.com/MajidRaimi/ad3oni.git
cd ad3oni
bun install
```

The Python dependencies are installed automatically by uv the first time the API runs. To set them up ahead of time:

```bash
cd apps/api && uv sync
```

### Running the apps

Start the entire stack (web + api) from the repository root with a single command:

```bash
bun run dev
```

This launches mprocs, which runs both processes side by side:

- **Web**: http://localhost:3000
- **API**: http://localhost:8000

You can also run each app on its own:

```bash
cd apps/web && bun run dev
cd apps/api && uv run uvicorn src.main:app --reload --port 8000
```

### Endpoints

| App | Method | Path        | Response |
| --- | ------ | ----------- | -------- |
| API | GET    | `/ping`     | `pong`   |
| Web | GET    | `/api/ping` | `pong`   |

The API also exposes interactive docs at http://localhost:8000/docs.

---

## Links 🔗

- 🐦 [Twitter Account](https://twitter.com/ad3oni_) for daily prayer reminders and updates.
- 🌐 [Ad3oni Website](https://www.ad3oni.com) for prayer times and personalized reminders.
- 🤖 [Invite the Ad3oni Discord Bot](https://discord.com/api/oauth2/authorize?client_id=1159198588782518292&permissions=26624&scope=bot%20applications.commands) to your server.
- 📱 iOS and Android applications are coming soon.

---

## Developers 👥

| Developer        | Email                                                |
| ---------------- | ---------------------------------------------------- |
| Majid Al-Raimi   | [majidsraimi@gmail.com](mailto:majidsraimi@gmail.com) |
| Rakkan Al-Yaqout | [rakanyaqoot@hotmail.com](mailto:rakanyaqoot@hotmail.com) |

---

## Contributing 🤝

Feel free to contribute to the Ad3oni project or provide feedback to help us improve this Islamic prayer reminder system. May it enhance your connection with Allah (SWT) and your daily prayers. 🙏✨

For any inquiries or support, please contact [majidsraimi@gmail.com](mailto:majidsraimi@gmail.com).

---

**Note:** The project's tech stack and features may evolve over time, so be sure to check the official Ad3oni website and Twitter account for the latest updates.
