from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import run_code, get_interpreter



def index(request):
    return render(request, 'hongik/index.html')


def editor(request):
    return render(request, 'hongik/editor.html', {'code': '', 'result': ''})


@api_view(['POST'])
def execute_batch(request):
    code = request.data.get['code', '']
    result = run_code(code)
    return Response({'result': result})

def execute_interactive(request):
    if request.method == "POST":
        code_line = request.POST.get('code_line', '')
        session_id = request.session.session_key
        interpreter = get_interpreter(session_id)
        result = interpreter.execute(code_line)
        return JsonResponse({'result': result})

def docs(request):
    return render(request, 'hongik/docs.html')
