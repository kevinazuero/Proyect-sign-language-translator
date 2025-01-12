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


class list_historial(LoginRequiredMixin,ListView):
    model = Historial
    template_name = 'Historial.html'
    paginate_by= 5
    context_object_name = 'palabras'
    login_url = '/'

    def get_queryset(self):
        queryset = super().get_queryset()
        usuario = self.request.user  
        palabra = self.request.GET.get('palabra')

        query = Q(user=usuario)
        if palabra:
            query &= Q(word__icontains=palabra)
        
        return queryset.filter(query).order_by('id')
        
@login_required
def historial_delete(request, pk):
    palabra = get_object_or_404(Historial, pk=pk)

    if palabra.user != request.user:
        return HttpResponseForbidden()

    palabra.delete()
    return redirect('core:historial')

class clear_historial(LoginRequiredMixin, View):
    template_name = 'clean_historial.html'
    success_url = reverse_lazy('core:historial')
    login_url = '/'

    def get(self, request, *args, **kwargs):
        context = {
            'grabar': 'Eliminar historial',
            'description': '¿Esta seguro de eliminar el historial?',
            'back_url': self.success_url,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_historial = Historial.objects.filter(user=request.user)
        user_historial.delete()
        return HttpResponseRedirect(self.success_url)
    

@login_required
def save_word(request):
    if request.method == 'POST':
        try:
            
            user= request.user
            
            data = json.loads(request.body)
            
            word = data.get('word', None)
                        
            nueva_palabra = Historial(user=user, word=word)
            nueva_palabra.save()
            
            return JsonResponse({'message': 'Palabra guardada correctamente.'}, status=200)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return redirect('core:inicio')
    