from django.urls import path


from .views import index, add_folder, add_file, read_file, recompile, delete_folder, delete_file, save_file, login_view, logout_view
urlpatterns = [

    path('', index, name='front'),
    path('add_folder/', add_folder, name='add_folder'),
    path('add_file/', add_file, name='add_file'),
    path('delete_folder/', delete_folder, name='delete_folder'),
    path('delete_file/', delete_file, name='delete_file'),
    path('open_file/', read_file, name='read_file'),
    path('recompile/', recompile, name='recompile'),
    path('save_file/', save_file, name='save_file'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]