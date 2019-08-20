## Dash app template for EDA Miner

### Project directory structure

Follow this directory structure. The app is expected to be run from the top-level directory, in a file like `demo_app.py`. The logic of the app will be inside 1 directory with the name of the app, e.g. `demo`. The `demo` folder can contain either an `app.py` if the app is small, or a `server.py`, an `app.py` and as many others as needed. Optionally, add a `requirements.txt` (preferably with the name of the app prepended) or any other files (e.g. `README.md`, `Dockerfile`, docs).

This simple example defines the main logic in `app.py` and uses two additional files, one for each `dcc.Tab` of the app. These are `upload.py` (upload a CSV file) and `view.py` (view your data with a `dash_table.DataTable`). Note that since the main script resides in the top-level you can asses sibling apps and top-level modules. This also means that you need to use relative imports where possible (see the demo files). Also note that `demo_server.py` imports the app from `demo/app.py`, not `server.py`.

```
├── demo
│   ├── assets
│   │   ├── images
│   │   └── favicon.ico
│   ├── app.py
│   ├── __init__.py
│   ├── README.md
│   ├── server.py
│   ├── upload.py
│   └── view.py
├── demo_server.py
└── demo_requirements.txt
```
 
 ### Integrating into EDA_miner
 
 After finishing up with your stand-alone app there are several ways you can integrate it into the main app. Currently only one is supported, but the individual configurations are up to you. Here are the main steps:
 
 1. Copy the `demo` folder and the rest of your files in the `/EDA_miner` folder (where the rest of the apps are).
 2. Go to `/EDA_miner/wsgi.py` and import your app, e.g.: `from demo_server import app as demo_app`.
 3. Initialize any Flask extensions you want, as per the instructions, e.g.: `login_manager.init_app(demo_app.server)`, and with the default or a custom index string, e.g.: `demo_app.index_string = base_dash.dash_appstring`.
 4. Give a URL path to your app as in the examples in `wsgi.py`, e.g.: `"/demo": demo_app.server,`
 
 Of course, instead of step 3 above you can use your own extensions or databases. In that case, add any configurations to your `/demo/server.py` file.
 
 ### GOTCHAs
 
- Your app works fine as standalone but doesn't even load after integrating it. Try:
  - When initializing the Dash app, pass in the parameters: `requests_pathname_prefix="/demo/"` and `assets_external_path="/static/"`.
  - The login manager might cause issues. Sharing the database (e.g. via symlinks or an abspath in the `.env` file) could solve the problem.
- Your CSS does not display correctly. Try:
  - Add the CSS files to the top-level `/static` folder and/or modify `base_dash.dash_appstring` to include your CSS manually.
- Non-authenticated users can still access the app. Try:
  - Use the `@login_required` on a callback that triggers directly when your app loads. It will redirect to the main app's login page.
  - Protect data by storing them on Redis with keys that include their username, and access them only with `flask_login.current_user.username`. e.g.: `redis_conn.set(f"{current_user.username}_data_iris")`.
- The sidemenu is not working properly?
  - Import the `interactive_menu` from the top-level `utils.py`, and add this line to your first layout: `*interactive_menu(output_elem_id="sidenav2_contents"),`. It adds an extra menu and a bit of JavaScript to make closing/opening it interactive.


*There is a chance that the structure will change and instead of connecting the apps at the WSGI level they will be deployed independently and connected via proxy. This will mostly affect Dash distribution of static files, but nothing that you need to worry about, as the changes will most likely not be breaking.
