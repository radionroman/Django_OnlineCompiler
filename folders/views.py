import subprocess

from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login, logout
from .models import User, File,  Folder
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import AddFolderForm, AddFileForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from io import BytesIO
import re

def cparser(content):
    lines = content.split('\n')
    content = ""
    i = 1
    for line in lines:
        content += "<code id=" + str(i) + ">" + line + "</code>" + '\n'
        i += 1
    return mark_safe(content)

def errparser(content):
    lines = content.split('\n')
    content = ""
    
    for line in lines:
        line1 = line[1:]
        match = re.search(r'\d+(?=:)', line1)
        if match:
            content += "<p class=\"error\" data-line-id=" + str(match.group(0)) + ">" + line + "</p>" + '\n'
        else:
            content += "<p>" + line + "</p>" + '\n'

    return mark_safe(content)


def parser(content):
    div_title_added = 0
    div_section_added = 0
    lines = content.split('\n')
    answer = "<button id=\"showAllButton\"> ShowAll </button>"
    answer += "<button id=\"hideAllButton\"> HideAll </button>"
    i = 0
    for line in lines:
        if (line != ";--------------------------------------------------------"):
            if (len(line) > 0 and line[0] == ';'):
                if (div_section_added > 0):
                    answer+="</h6> </div>"
                    div_section_added = 0

                line1 = line[1:]
                match = re.search(r'(?<=:)\d+(?=:)', line1)
                if match and (div_title_added == 0):
                    i = int(match.group(0))
                    answer += "<div class=\"title\" data-line-id=" + str(i) + "> <b>"
                    print(i)
                elif (div_title_added == 0):
                    i = -1
                    answer += "<div class=\"title\" data-line-id=" + str(i) + "> <b>"
               

                answer += line1

                div_title_added += 1
            elif (len(line) > 0):
                if (div_title_added > 0):
                    answer += "</b></div>"
                    div_title_added = 0

                if (div_section_added == 0):
                    answer += "<div class=\"section\"> <h6>"

                answer += line
                div_section_added += 1

    if (div_title_added > 0):
        answer += "</b></div>"
    elif (div_section_added > 0):
        answer += " </h6> </div>"

    safe_answer = mark_safe(answer)

    return safe_answer







def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = JsonResponse({'success': True, 'message': get_folder_list(request), 'user': request.user.username})
            response.status_code = 200
            return response
        else:
            # Handle invalid login credentials
            response = JsonResponse({'success': False, 'message': 'Username or password is incorrect'})
            response.status_code = 401
            return response
    else:
        response = JsonResponse({'success': False, 'message': 'Invalid request method'})
        response.status_code = 401
        return response
        
def logout_view(request):
    logout(request)
    response = JsonResponse({'success': True, 'message': get_folder_list(request)})
    response.status_code = 200
    return response


def recompile(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        standard = request.POST.get('standard')
        options = request.POST.getlist('options')
        processor = request.POST.get('procesor')
        options_processor = request.POST.getlist('options_processor')
        file = File.objects.get(id=file_id)
        with file.file.open('r') as file:
            content = file.read()
            arguments = ['sdcc', '-S', standard]
            arguments += options
            arguments += [processor]
            arguments += options_processor
            arguments += [file.name]

            print(arguments)
            
            result = subprocess.run(arguments, capture_output=True)
            errors = result.stderr.decode('utf-8')
            if result.returncode != 0:
                response = JsonResponse({'success': False, 'message': errparser(errors)})
                print(errors)
                response.status_code = 200
                return response

            try:
                asm_file_name = file.name.replace('.c', '.asm')
                with open(asm_file_name, 'r') as asm_file:
                    asm_content = asm_file.read()
            except Exception as e:
                asm_content = "Compilation failed."
                response = JsonResponse({'success': False, 'message': "An error occurred:" + str(e) + "Probably file did not compile properly."})
                response.status_code = 200
                return response

    else:
        content = ''
        asm_content = ''
    asm_content = parser(asm_content)

    response = JsonResponse({'success': True, 'message': get_folder_list(request), 'content': cparser(content), 'asm_content': asm_content})
    response.status_code = 200
    return response



def read_file(request):
    try:
        file_id = request.POST['file_id']
        file = File.objects.get(id=file_id)
        file_content = ''
        if(file.is_available):
            with file.file.open('r') as f:
                file_content = f.read()
                asm_name = f.name.replace('.c', '.asm')
            print("AJAX OPEN FILE: " + str(file_id))
    except File.DoesNotExist:
        response = JsonResponse({'success': False, 'message': 'File not found.'})
        response.status_code = 401
        return response
        
    except Exception as e:
        response = JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'})
        response.status_code = 401
        return response
    asm_content = "No File Compiled"
    try:
        print(asm_name)
        my_asm = open(asm_name, 'r')
        asm_content = my_asm.read()
        
    except Exception as e:
        cos = 0
    response = JsonResponse({'success': True, 'file_content': cparser(file_content), 'asm_name': asm_name, 'asm_content': parser(asm_content), 'file_name': file.name})
    response.status_code = 200
    return response


def save_file(request):
    if request.method == 'POST':
        file_name = request.POST.get('file_name')
        content = request.POST.get('content')
        f = open(file_name, 'w')
        f.write(content)
        f.close()

    return redirect('../')


def add_folder(request, parent_folder_id=None):
    if request.method == 'POST':
        new_folder = Folder()
        new_folder.name = request.POST.get('name')
        print(request.POST.get('parent_folder_id'))
        if request.POST.get('parent_folder_id') != "" and request.POST.get('parent_folder_id') != None:
            new_folder.parent_folder = Folder.objects.get(id=request.POST.get('parent_folder_id'))
        else :
            new_folder.parent_folder = None    
        new_folder.owner = request.user
        new_folder.save()
        # Process the form data
        # Retrieve the form data using request.POST.get('<field_name>')
        # Perform any validation or save data to the database
        
        # Return a JSON response indicating success
        response = JsonResponse({'success': True, 'message': get_folder_list(request), 'status_code': 200})
        response.status_code = 200
        return response

    # Return a JSON response indicating an error if the request method is not POST
    response = JsonResponse({'success': False, 'message': 'Invalid request method', 'status_code': 401})
    response.status_code = 401
    return response


def add_file(request, parent_folder_id=None):
    if request.method == 'POST':
        new_file = File()
        new_file.name = request.POST.get('name')
        new_file.description = request.POST.get('description')
        new_file.owner = request.user
        new_file.is_available = True
        parent_folder_id = request.POST.get('parent_folder_id')
        print(parent_folder_id)
        if parent_folder_id != "" and parent_folder_id != None:
            new_file.parent_folder = Folder.objects.get(id=parent_folder_id)
        new_file.file = request.FILES.get('file')

        new_file.save()
        # Process the form data
        # Retrieve the form data using request.POST.get('<field_name>')
        # Perform any validation or save data to the database
        
        # Return a JSON response indicating success
        response = JsonResponse({'success': True, 'message': get_folder_list(request), 'status_code': 200})
        response.status_code = 200
        return response

    # Return a JSON response indicating an error if the request method is not 
    response = JsonResponse({'success': False, 'message': 'Invalid request method', 'status_code': 401})
    response.status_code = 401
    return response



def get_files_list(request,folder_id=None):
    root_files = File.objects.filter(parent_folder=folder_id)
    file_list = ""
    for file in root_files:
        if file.is_available and request.user == file.owner:
            file_list += "<li style=\"display:inline-block\">" + file.name 
            file_list += "<button class=\"deleteFileButton\" data-entry-id=" + str(file.id) + ">Delete</button>"
            file_list += "<button style=\"display:inline-block\" class=\"openFileButton\" data-entry-id=" + str(file.id) +  " >open</button>"
            
            file_list += "</li>"
    return file_list    


def get_folder_list(request,folder_id=None):
    root_folders = Folder.objects.filter(parent_folder=folder_id)
    folder_list = ""
    if request.user.is_authenticated and folder_id == None:
        folder_list += "<b>Pliki</b> <button class=\"addButton\" data-entry-id=\"\" data-toggle=\"modal\" data-target=\"#addFolderModal\">Add</button> <br>"
    elif not request.user.is_authenticated and folder_id == None:
        folder_list += "<b>Zaloguj sie</b> <br>"
    for folder in root_folders:
        if folder.is_available and request.user == folder.owner:    
            folder_list += "<li style=\"display:inline-block\">" + folder.name 
            folder_list += "<button class=\"deleteButton\" data-entry-id=\"" + str(folder.id) + "\">Delete</button>"
            folder_list += "<button class=\"addButton\" data-entry-id=\""+ str(folder.id) + "\" data-toggle=\"modal\" data-target=\"#addFolderModal\">Add</button>"
            folder_list += "</li>"

            folder_list += "<ul>"
            folder_list += get_folder_list(request, folder)
            folder_list += get_files_list(request,folder)
            folder_list += "</ul>"
            #folder_list.append("<li style=\"display:inline-block\">" + "folder" + "</li>")
    return folder_list


def index(request):
    root_folders = Folder.objects.filter(parent_folder=None)
    folder_list = get_folder_list(request=request)

    folder_list = mark_safe(folder_list)

    if request.method == 'POST':
        # Read the content of the selected file
        file_name = request.POST.get('fil')
        with open(f'{file_name}', 'r') as file:
            content = file.read()
    else:
        content = ''

    return render(request, 'folders/front.html', {'folder_list': folder_list, 'content': content, 'name': request.user})


def delete_file_helper(file_id):
    file = File.objects.get(id=file_id)
    file.is_available = False
    file.available_date = timezone.now()
    file.save()


def delete_file(request):
    
    file_id = request.POST['file_id']
    file = File.objects.get(id=file_id)
    if(file.is_available):
        print("AJAX DELETE FILE: " + str(file_id))
        delete_file_helper(file_id)
        response = JsonResponse({'success': True, 'message': get_folder_list(request=request), 'status_code': 200})
        response.status_code = 200
        return response
    raise HttpResponseServerError("File is not available")


def delete_folder_helper(folder_id):
    folder = Folder.objects.get(id=folder_id)
    folder.is_available = False
    folder.available_date = timezone.now()
    folder.save()
    children_folders = Folder.objects.filter(parent_folder_id=folder_id)
    children_files = File.objects.filter(parent_folder_id=folder_id)
    for child in children_files:
        delete_file_helper(child.id)
    for child in children_folders:
        delete_folder_helper(child.id)


def delete_folder(request):
    folder_id = request.POST['folder_id']
    folder = Folder.objects.get(id=folder_id)
    if(folder.is_available):
        print("AJAX DELETE FOLDER: " + str(folder_id))
        delete_folder_helper(folder_id)
        response = JsonResponse({'success': True, 'message': get_folder_list(request=request), 'status_code': 200})
        response.status_code = 200
        return response
    raise HttpResponseServerError("Folder is not available")
  

    

