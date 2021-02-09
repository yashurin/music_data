# Music Data Demo Application

Music Data Demo is a simple application to aggregate and reconcile the metadata for musical works.
It is created with `Django`, `Docker` and `PostgreSQL`.

To run the application, Docker and git are needed.

Music Works metadata is taken from `.csv` files located in the `uploads` directory.
After parsing of a file, it is marked as `processed` and is excluded from further processing.

After Music Works metadata is processed, it can be obtained via URLs or API calls (if the Django server is running).

## Building and Running the Application

1. After downloading application from github or unpacking the `.zip` archive, go to the `music_data` folder in terminal. The folder should contain, along with other files, `Dockerfile` and `manage.py`. 

`cd music_data`

2. Build the Docker container:

`docker-compose build`

3. Start the application in the Docker container: 

`docker-compose up`

If successful, you will see the message similar to `Starting development server at http://0.0.0.0:8000/`

4. Open a separate terminal window, without stopping the container. Execute the command to create the database for Django models:

`docker-compose exec web python manage.py migrate` 

5. Process the `.csv` file with music works metadata located in the `uploads` directory. Execute the command:

`docker-compose exec web python manage.py process_files` 

If successful, you will see the message `1 CSV file(s) with music works were processed.` 

## Getting Music Works Metadata

To get metadata (in JSON) for all available music works from the database, use any one of those methods:

- Go to the URL http://localhost:8000/musicworks/

- Send a GET request to http://localhost:8000/musicworks/ in the Postman client.

- Execute the `curl 'http://localhost:8000/musicworks/'` command in terminal.

To get metadata (in JSON) for a single music work, replace `musicworks` with a valid `iswc` code. If there is no record with such code in the database, error message will be returned. Valid examples:

- Go to the URL http://localhost:8000/T9214745718/

- Send a GET request to http://localhost:8000/T9214745718/ in the Postman client.

- Execute the `curl 'http://localhost:8000/T9214745718/'` command in terminal.

## Music Works Reconciliation

Reading and processing of a `.csv` file is handled by the `pandas` library. It involves several steps.

- As the file is read, the `contributors` string for each row is split into a list.

- Invalid row with insufficient data are dropped.

- Data is aggregated by `title` and `iswc` with `groupby`. The list of contributors now includes the sum of all mentioned contributors.  

- Duplicates are removed from the list of contributors.

- Rows are ordered by `iswc`, `NaN`s (if any) are replaced by empty strings.

- DB records with the reconciled data are created with the `MusicWork` model.

### A lot of other things could be added or improved for a real project - but it is just a demo. 

(c) by Andrey Yashurin, 2021 - yashurin@gmail.com