from django.shortcuts import render


def view_main(request):
    context = {}
    return render(request, 'index.html', context)