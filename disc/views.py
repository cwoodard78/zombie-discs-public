from rest_framework.viewsets import ModelViewSet
from .models import MyModel
from .serializers import MyModelSerializer
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from .models import Disc
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import DiscForm
from django.contrib.auth.decorators import login_required

class MyModelViewSet(ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

@login_required
def map_view(request):
    return render(request, 'disc/map.html')

@login_required
def submit_disc(request):
    if request.method == "POST":
        form = DiscForm(request.POST)
        if form.is_valid():
            disc = form.save(commit=False)  # Don't save yet
            disc.user = request.user  # Assign the authenticated user
            form.save()
            return redirect('disc_detail', disc_id=disc.id)
            # return JsonResponse({"message": "Disc entry submitted successfully!"})
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    # For GET requests, render the form
    form = DiscForm()
    # return render(request, "disc/submit_disc.html", {"form": form})
    return render(request, "disc/submit_disc.html", {"form": form})

@login_required
def disc_detail(request, disc_id):
    disc = get_object_or_404(Disc, id=disc_id)
    from_user_disc_list = request.GET.get("from_user_disc_list", "false").lower() == "true"
    return render(request, "disc/disc_detail.html", {"disc": disc, "from_user_disc_list": from_user_disc_list})

@login_required
def user_disc_list(request):
    discs = Disc.objects.filter(user=request.user)
    return render(request, "disc/user_disc_list.html", {"discs": discs})