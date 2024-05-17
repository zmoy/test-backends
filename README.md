Here are two back-ends, one made with raw python (no framework) and the other one with Flask.

- "no-framework" branch: raw Python back-end
- "flask" branch: Flask back-end

Both of them are doing the same thing: display a json file on the "/mockfile" page , and on the "/mockfile_by_proxy" page
the server is going to the first page ("/mockfile") to load the json file and displays it on "/mockfile_by_proxy" as well
as the duration of the request & response.

Those two simple back-ends were made to compare the performance and use complexity of a framework-less python server with
a server with a framework.



HOW TO LAUNCH THEM:

- Flask back-end: go on the project folder and execute the "flask run --debug" command.

- Raw Python back-end: firstly make the Flask server run (if you want to try the "/mockfile_by_proxy" route), and then open
another terminal and execute the following command "py app.py".
