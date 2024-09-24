from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import *
# Create your views here.
import os
from PIL import Image


def convert_to_png(image):
    
    cr2 = Image.open(os.path.join('media', str(image.file)))
    
    return cr2



# def import_photos(request):

#     form = PhotoForm(request.POST, request.FILES)
    
#     if request.method == "POST":
        
#         print(form.is_valid())

#         if form.is_valid():
#             name = form.cleaned_data['file']
#             print("name : ",name)

#             extension = str(name).split('.')[-1]

#             if extension.lower() == 'cr2':
                
#                 form.save()
#                 return HttpResponseRedirect("convert")
    
#     form = PhotoForm()

#     context = {"form" : form}

#     url = "convertor/import_photos.html"

#     return render(request, url, context)




def import_photos(request):

    form = PhotoForm(request.POST, request.FILES)
    
    if request.method == "POST":
        
        print(form.is_valid())

        if form.is_valid():
            name = form.cleaned_data['file']
            print("name : ",name)

            extension = str(name).split('.')[-1]

            if extension.lower() == 'cr2':
                
                form.save()
                return HttpResponseRedirect("convert")
    
    form = ImagesForm()

    context = {"form" : form}

    url = "convertor/import_photos.html"

    return render(request, url, context)



def convert(request):
    
    images = list(Photo.objects.filter(new=True))
    print("file 0 : ", images[0].file)
    for image in images:
        print('image : ', image)
        png = convert_to_png(image)

        name = str(image.file).split('/')[-1]
        name = name[:-3] + 'png'
        
        new_path = os.path.join("media", str(image.file).split("/")[0], "png", name)
        print(new_path)
        png.save(new_path)
        image.delete()
        del(png)
        os.remove(os.path.join("media", str(image.file)))
        

    return HttpResponseRedirect('/download')



import os
import zipfile
from django.http import HttpResponse
from django.conf import settings
from io import BytesIO

def download_zip(request):
    # Chemin vers le dossier contenant les fichiers que tu veux zipper
    folder_path = 'media/images/png'

    # Crée un fichier en mémoire
    zip_buffer = BytesIO()

    # Création de l'archive ZIP
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # Chemin absolu du fichier
                file_path = os.path.join(root, file)
                # Chemin relatif à partir du dossier compressé pour garder l'arborescence
                relative_path = os.path.relpath(file_path, folder_path)
                # Ajout du fichier au ZIP
                zip_file.write(file_path, relative_path)

    # Positionner le pointeur au début du fichier
    zip_buffer.seek(0)

    # Préparer la réponse HTTP pour télécharger le fichier ZIP
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=fichiers_compresses.zip'

    for file in os.listdir(folder_path):
        os.remove(os.path.join(folder_path, file))


    return response

    
