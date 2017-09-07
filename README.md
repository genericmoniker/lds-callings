LDS Callings
============

Setup (Ubuntu 17)
-----------------

In the root of the project directory...

```bash
sudo ./bootstrap.sh
```

Environment variables
---------------------

When running in a debugger, set these environment variables:

web

    DATABASE_URL=postgres:///lds-callings
    PORT=5000

worker

    DATABASE_URL=postgres:///lds-callings
