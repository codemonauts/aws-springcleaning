# AWS SpringCleaning

**WARNING**
```
This is under heavy development and will change a lot!
All of this code is just pushed to the repo without proper testing of corner cases or a code review. Use at your own risk and only use a read-only IAM user to start to prevent major damage!
```

Set of small scripts that find unused or old resources in your account. Cleaning
your account regulary results in a smaller AWS bill and in better security.

## Why I created this

For most things AWS won't show you if they are in use or not and will first
complain when you try to delete them. Therefore these scripts find resources
that are not used by anything else and gives you a list. Later versions will
maybe clean them up for you.

## Requirements
  * Python3
    * boto3
    * crayons
    * arrow
  * IAM user which can use `Describe`

## Usage
  1. Configure your AWS credentials with `awscli`
  2. Install the Python requirements with `pipenv install`
  3. Create `config.py` from `config.py.example` and adapt to your likeing
  3. Run `pipenv run python full_scan.py`
  4. Clean up your account ;)