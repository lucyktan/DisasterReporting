from django.shortcuts import render
from django.http import HttpResponseRedirect

from forms import DisasterForm

def get_form(request):
    if request.method == 'POST':
        form = DisasterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/results/')
    else:
        form = DisasterForm()

    return render(request, 'form.html', {'form': form})

def show_results(request):
    return render(request, 'results.html')