# UI
To enable the UI, it has to be configured and built. Then, the resulting files must be moved to the appropriate path.

Change directory to the `ui` sub-folder, then run the following to install the necessary modules (may take several minutes):
```
npm install
```

Duplicate the `.env.template` file and rename the new one to simply `.env`. Inside is the configuration of the UI:
* `REACT_APP_BACKEND_ADDRESS`: The address of the backend. Make sure the port corresponds to the same as the value indicated in `application.yml` under `server.port`.

Next, run the following command. It will create a new folder named `build`.
```
npm run-script build
```

Move the `build` folder you just obtained to the server, under `validation-framework\server\src\main\resources`. Once it's there, rename `build` to `public`.

When the server is run, the UI will be available at `localhost:8200`.
