# Robbie

> Run experiments on the Robbie Cloud

## Installation

Install the package from PyPi:

```bash
pip install robbie
```

## Getting Started

Log in to your account

```sh
robbie login
```

Create a python file and decorate it.

```python
from robbie import remote

@remote(
    funding_group_id ='44d273ad-75b4-4af4-8a33-0ab652c2c315',
    environment_id = 'c2fab2e7-7e1c-4180-8d77-53ddbe2af281',
    image = 'pytorch-training:2.2.0-cpu-py310-ubuntu20.04-ec2',
)
def main():
    print("Running my function")

if __name__ == "__main__":
    main()
```

Deploy the job

```sh
python main.py
```

## Positron CLI Usage

Explore the help dialogs.

```sh
robbie --help

robbie run --help
```

## Job Types

### Generic Job

Defined in `job_config.yaml` as a `commands` block.

Example at `test/cli`.

Run with `robbie run`

### Decorator Job

Defined as a python native decorator.

Example at `test/decorator/test.py`.

Run with `python test.py`

Rather than specify configuration options in the src code, you can put them in `job_config.yaml`.

Example at `test/decorator/with_config/main.py`.

## Positron Job Runner

Located at `app/positron_job_runner`, this gets deployed as `positron-job-runner` and is used in the deployed container to launch the user's project.

## License

This project is licensed under the Apache 2 License. See the [LICENSE](LICENSE) file for details.
