from twisted.web.static import File
from twisted.web.template import Element, XMLString, renderer, XMLFile
from twisted.python.filepath import FilePath
from jinja2 import Environment, FileSystemLoader

from klein import run, route

import os
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import markdown

directory_to_watch = 'data'
template_path = 'templates/template.html'
output_file_path = 'static'

env = Environment(loader=FileSystemLoader('templates'))


# Create a custom event handler that responds to file system events.
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            # Handle file modification events here.
            print(f'File modified: {event.src_path}')
            file_path = event.src_path
            with open(file_path, 'r') as file:
                # Read the entire contents of the file into a string
                file_contents = file.read()
                print(file_contents)

            html = markdown.markdown(file_contents)
            print(html)
            filename, file_extension = os.path.splitext(os.path.basename(file_path))
            print("Filename without extension:", filename)
            print("File extension:", file_extension)
            template = env.get_template('template.html')
            template_data = {
                    'editURL': "/_" + filename,
                    'content': html,
            }
            rendered_template = template.render(template_data)

            output = output_file_path + '/' + filename + '.html'
            with open(output, 'w') as output_file:
                output_file.write(rendered_template)

@route('/', branch=True)
def home(request):
    return File("./static")

@route('/_<string:name>', methods=['GET'])
def edit(request, name='world'):
    template = env.get_template('edit.html')
    file_path = 'data/' + name + '.md'
    with open(file_path, 'r') as file:
        # Read the entire contents of the file into a string
        file_contents = file.read()
    # Define data to be inserted into the template
    template_data = {
        'title': 'My Page',
        'page': name,
        'username': 'John',
        'content': file_contents,
    }
    rendered_template = template.render(template_data)
    return rendered_template.encode('utf-8')

@route('/_<string:name>', methods=['POST'])
def editDone(request, name):
    print(name)
    content = request.content.read()
    try:
        json_data = json.loads(content)
        # Now, you have a Python dictionary with the parsed JSON data
        print("Received JSON data:", json_data['content'])
        file_path = 'data/' + name + '.md'
        with open(file_path, 'w') as file:
            # Read the entire contents of the file into a string
            file.write(json_data['content'])
            
    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
   
    return "yay"

if __name__ == "__main__":
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=directory_to_watch, recursive=False)

    # Start the observer to begin monitoring for file changes.
    observer.start()
    run("localhost", 8080)