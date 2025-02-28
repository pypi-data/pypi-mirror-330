import subprocess

from rich.markdown import Markdown

import coiled

from ..utils import Panel, console, log_interactions


def hello_world() -> bool:
    console.print(
        Panel(
            Markdown(
                """
## Example: Hello, world

Let's launch 10 VMs, and run the program `echo "Hello, world"`.  
This will cost about $0.01.

We'll run the following commands:

```bash
# Submit 10 'Hello, world' jobs
coiled batch run \\
    --container ubuntu:latest \\
    --n-tasks 10 \\
    echo 'Hello, world'
# Monitor progress while jobs run
coiled batch wait
# Grep through logs
coiled logs | grep Hello
```

which submit the jobs, monitors their progress, and searches through
their logs after they're done.

I'll do this here, but you can also do this in another terminal.
""".strip()  # noqa: W291
            )
        )
    )

    with log_interactions("example-hello-world"):
        info = coiled.batch.run(["echo", "'Hello, world'"], container="ubuntu:latest", ntasks=10)
        subprocess.run(["coiled", "batch", "wait", str(info["cluster_id"])], check=True)
        logs = subprocess.run(["coiled", "logs", str(info["cluster_id"])], check=True, capture_output=True)
        grep = subprocess.run(["grep", "Hello"], check=True, capture_output=True, input=logs.stdout)
        print(grep.stdout.decode().strip())

    return True
