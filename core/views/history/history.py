from django.views.generic import ListView,View
from django.db.models import Q

from django.urls import reverse_lazy

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.shortcuts import get_object_or_404, redirect,render
from django.http import HttpResponseForbidden,HttpResponseRedirect

from core.models import Historial

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class ListHistory(LoginRequiredMixin,ListView):
    model = Historial
    template_name = 'Historial.html'
    paginate_by= 5
    context_object_name = 'palabras'
    login_url = '/'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        word = self.request.GET.get('palabra')

        query = Q(user=user)
        if word:
            query &= Q(word__icontains=word)
        
        return queryset.filter(query).order_by('id')

class ClearHistory(LoginRequiredMixin, View):
    template_name = 'clean_historial.html'
    success_url = reverse_lazy('core:historial')
    login_url = '/'

    def get(self, request, *args, **kwargs):
        context = {
            'option': 'Eliminar historial',
            'description': '¿Esta seguro de eliminar el historial?',
            'back_url': self.success_url,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_history = Historial.objects.filter(user=request.user)
        user_history.delete()
        return HttpResponseRedirect(self.success_url)


@login_required
def delete_history(request, pk):
    word = get_object_or_404(Historial, pk=pk)

    if word.user != request.user:
        return HttpResponseForbidden()

    word.delete()
    return redirect('core:historial')

@login_required
def save_word(request):
    if request.method == 'POST':
        try:
            user= request.user
            data = json.loads(request.body)
            word = data.get('word', None)
            new_word = Historial(user=user, word=word)
            new_word.save()
            return JsonResponse({'message': 'Palabra guardada correctamente.'}, status=200)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return redirect('core:inicio')
    