from __future__ import annotations

import subprocess

from rich.markdown import Markdown
from rich.prompt import Prompt

import coiled

from ..utils import PRIMARY_COLOR, Panel, console, log_interactions

NTASKS = 10


def hello_world(first_time=False) -> bool | None:
    panel_kwargs = {}
    if first_time:
        panel_kwargs = {
            "title": "[white]Step 2: Hello, world[/white]",
            "border_style": PRIMARY_COLOR,
        }
    console.print(
        Panel(
            Markdown(
                f"""
{"## Example: Hello, world" if not first_time else ""}

Let's start easy by running `echo Hello, world` on {NTASKS} cloud VMs.
This will cost about $0.01.

We'll run the following commands:

```bash
$ coiled batch run \\             # Submit 10 'Hello, world' jobs
    --container ubuntu:latest \\
    --n-tasks {NTASKS} \\
    echo Hello world
$ coiled batch wait              # Monitor progress while jobs run
$ coiled logs | grep Hello       # Grep through logs
```

which submit the jobs, monitors their progress, and searches through
their logs after they're done.

I'll do this for you here, but you can also do this yourself in another terminal.
""".strip()  # noqa: W291
            ),
            **panel_kwargs,
        ),
    )

    try:
        choice = Prompt.ask(
            "Ready to launch some cloud instances?",
            choices=["y", "n"],
            default="y",
            show_choices=True,
            show_default=True,
        )
        coiled.add_interaction("cli-hello:run-hello-world", success=True, choice=choice)
    except KeyboardInterrupt:
        coiled.add_interaction("cli-hello:KeyboardInterrupt", success=False)
        return False

    if choice == "y":
        with log_interactions("example-hello-world"):
            info = coiled.batch.run(["echo", "Hello world"], container="ubuntu:latest", ntasks=NTASKS)
            subprocess.run(["coiled", "batch", "wait", str(info["cluster_id"])], check=True)
            # Sometimes it takes a second for all the logs to show up.
            # Let's try a few times if they're not there initially.
            count = 0
            while count <= 2:
                logs = subprocess.run(["coiled", "logs", str(info["cluster_id"])], check=True, capture_output=True)
                grep = subprocess.run(["grep", "Hello"], check=True, capture_output=True, input=logs.stdout)
                out = grep.stdout.decode().strip()
                if len(out.split("\n")) == NTASKS:
                    print(out)
                    break
                else:
                    count += 1
        return True
    else:
        console.print("On to bigger examples then! :rocket:")
        return None
