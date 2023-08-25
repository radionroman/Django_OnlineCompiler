import tempfile
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Folder, File

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Folder, File


class FolderModelTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.folder = Folder.objects.create(
            name='Test Folder',
            owner=self.user
        )
        self.subfolder = Folder.objects.create(
            name='Subfolder',
            parent_folder=self.folder,
            owner=self.user
        )
        self.subfile = File.objects.create(
            name='Test SubFile',
            owner=self.user,
            parent_folder=self.subfolder
        )
    
    def test_folder_creation(self):
        self.assertEqual(self.folder.name, 'Test Folder')
        self.assertEqual(self.folder.owner, self.user)
        self.assertTrue(self.folder.is_available)

    def test_get_subfolders(self):
        subfolder = Folder.objects.create(
            name='Subfolder',
            parent_folder=self.folder,
            owner=self.user
        )
        subfolder_2 = Folder.objects.create(
            name='Subfolder 2',
            parent_folder=self.folder,
            owner=self.user
        )
        subfolders = self.folder.get_subfolders
        self.assertIn(subfolder, subfolders)
        self.assertIn(subfolder_2, subfolders)

    def test_get_subfiles(self):
        file = File.objects.create(
            name='Test File',
            owner=self.user,
            parent_folder=self.folder
        )
        files = self.folder.get_subfiles
        self.assertIn(file, files)

    def test_set_unavailable(self):
    
        self.folder.set_unavailable
        print("Subfile " + self.subfile.name + " " + str(self.subfile.is_available))
        self.assertEqual(self.folder.is_available, False)
        #self.assertEqual(self.subfolder.is_available, False)
        #self.assertEqual(self.subfile.is_available, False)
     
        

class FileModelTestCase(TestCase):
    @classmethod
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.folder = Folder.objects.create(
            name='Test Folder',
            owner=self.user
        )
        self.file = File.objects.create(
            name='Test File',
            owner=self.user,
            parent_folder=self.folder
        )
    
    def test_file_creation(self):
        self.assertEqual(self.file.name, 'Test File')
        self.assertEqual(self.file.owner, self.user)
        self.assertTrue(self.file.is_available)

    def test_file_upload(self):
        file_path = 'abi.c'
        with open(file_path, 'rb') as file_data:
            self.file.file.save('abi.c', file_data)
        
        self.assertTrue(self.file.file)
           

    def test_set_unavailable(self):
        self.file.set_unavailable
        self.assertFalse(self.file.is_available)


import json
from django.test import Client, TestCase


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.save()

    def test_add_folder(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_folder'), {'name': 'test_folder', 'parent_folder': '""'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Folder.objects.count(), 1)
        self.assertEqual(Folder.objects.get().name, 'test_folder')

    def test_add_file(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('add_file'), {'name': 'test_file', 'description': 'test_description', 'owner': self.user.id, 'is_available': True, 'parent_folder': '""'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(File.objects.count(), 1)
        self.assertEqual(File.objects.get().name, 'test_file')    

    def test_delete_folder(self):
        self.client.login(username='testuser', password='12345')
        folder = Folder.objects.create(name='test_folder', owner=self.user)
        response = self.client.post(reverse('delete_folder'), {'folder_id': folder.id})
        self.assertEqual(response.status_code, 200)

    def test_delete_file(self):
        self.client.login(username='testuser', password='12345')
        file = File.objects.create(name='test_file', owner=self.user)
        response = self.client.post(reverse('delete_file'), {'file_id': file.id})
        self.assertEqual(response.status_code, 200)

    def test_read_file(self):
        self.client.login(username='testuser', password='12345')
        file = File.objects.create(name='test_file', owner=self.user, file=SimpleUploadedFile('test_file.txt', b'abc'))
        response = self.client.post(reverse('read_file'), {'file_id': file.id})
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.content, None)    

    def test_login_view(self):

        # Test valid login
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['user'], 'testuser')

        # Test invalid login
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.content)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Username or password is incorrect')

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])


    def test_recompile_view_fail(self):
        self.client.login(username='testuser', password='12345')
        file = File.objects.create(name='test_file', owner=self.user, file=SimpleUploadedFile('test_file.c', b'abc'))
        response = self.client.post(reverse('recompile'), {'file_id': file.id, 'standard': '--std-c99', 'options': ['-c'], 'procesor': '-mz80', 'options_processor': []})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['success'])


    def test_recompile_view_success(self):
        self.client.login(username='testuser', password='12345')
        # Create a SimpleUploadedFile with the content of a "Hello World" C program
        file_content = b'#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}'
        file = File.objects.create(name='test_file', owner=self.user, file=SimpleUploadedFile('test_file.c', file_content))

        response = self.client.post(reverse('recompile'), {'file_id': file.id, 'standard': '--std-c99', 'options': ['-c'], 'procesor': '-mz80', 'options_processor': []})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
   




# def recompile(request):
#     if request.method == 'POST':
#         file_id = request.POST.get('file_id')
#         standard = request.POST.get('standard')
#         options = request.POST.getlist('options')
#         processor = request.POST.get('procesor')
#         options_processor = request.POST.getlist('options_processor')
#         file = File.objects.get(id=file_id)
#         with file.file.open('r') as file:
#             content = file.read()
#             arguments = ['sdcc', '-S', standard]
#             arguments += options
#             arguments += [processor]
#             arguments += options_processor
#             arguments += [file.name]

#             print(arguments)
            
#             result = subprocess.run(arguments, capture_output=True)
#             errors = result.stderr.decode('utf-8')
#             if result.returncode != 0:
#                 response = JsonResponse({'success': False, 'message': errparser(errors)})
#                 response.status_code = 401
#                 return response

#             try:
#                 asm_file_name = file.name.replace('.c', '.asm')
#                 with open(asm_file_name, 'r') as asm_file:
#                     asm_content = asm_file.read()
#             except Exception as e:
#                 asm_content = "Compilation failed."
#                 response = JsonResponse({'success': False, 'message': "An error occurred:" + str(e) + "Probably file did not compile properly."})
#                 response.status_code = 401
#                 return response

#     else:
#         content = ''
#         asm_content = ''
#     asm_content = parser(asm_content)

#     response = JsonResponse({'success': True, 'message': get_folder_list(request), 'content': cparser(content), 'asm_content': asm_content})
#     response.status_code = 200
#     return response


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return JsonResponse({'success': True, 'message': get_folder_list(request), 'user': request.user.username, 'status_code': 200})
#         else:
#             # Handle invalid login credentials
            
#             return JsonResponse({'success': False, 'message': 'Username or password is incorrect', 'status_code': 401})
#     else:
#         return JsonResponse({'success': False, 'message': 'Invalid request method', 'status_code': 401})

# def logout_view(request):
#     logout(request)
#     return JsonResponse({'success': True, 'message': get_folder_list(request)})

        