from django.shortcuts import render

def administrator_view(request):
    return render(request, 'administrator.html')