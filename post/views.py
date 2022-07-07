from django.shortcuts import render, HttpResponse, Http404


# Create your views here.
def home(request):
    print(request.method)
    return render(request, 'posts/base.html')


def post(request, post_id: int):
    print("POST")
    print(post_id)
    if request.method == 'GET':
        print("param: ", request.GET)
    query_to_bd = (request.GET.get('prise_min'), request.GET.get('prise_max'))
    return render(request, 'posts/post.html', {'content': request.GET})


def post_with_two(request, other: int, post_id: int):
    print(post_id)
    if request.method == 'GET':
        print("param: ", request.GET)
    query_to_bd = (request.GET.get('prise_min'), request.GET.get('prise_max'))
    return render(request, 'posts/post.html', {'content': request.GET})


def post_str(request, post_id: str):
    print(post_id)
    post_content = request.headers
    return render(request, 'posts/post.html', {'content': post_content})


# return render(request, 'posts/post.html')


def about(request):
    return render(request, 'posts/about.html', {'content': '<h1>hello</h1>'})
    # return HttpResponse('<h1>hello</h1>', status=404)


def create_post(request):
    pass
