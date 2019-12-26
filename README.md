LDS Callings
============

**Archived: No active development planned for the near future.**

Setup (Ubuntu 17)
-----------------

In the root of the project directory...

```bash
sudo ./bootstrap.sh
```

Environment variables
---------------------

For deployment to Heroku, you need to set SECRET_KEY to a random value,
which can be done with the Dashboard or using `heroku config:set`.

When running in a debugger, set these environment variables:

web

    DATABASE_URL=postgres:///lds-callings
    PORT=5000
    SECRET_KEY=whatever

worker

    DATABASE_URL=postgres:///lds-callings
