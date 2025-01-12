from rest_framework.viewsets import ModelViewSet
from .models import MyModel
# from .serializers import MyModelSerializer
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from .models import Disc
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import DiscForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# # For Serializer
# from .serializers import StatsSerializer
# from rest_framework.views import APIView
# from rest_framework.response import Response

# # class MyModelViewSet(ModelViewSet):
# #     queryset = MyModel.objects.all()
# #     serializer_class = MyModelSerializer

# class StatsAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         total_lost = Disc.objects.filter(status='lost').count()
#         total_found = Disc.objects.filter(status='found').count()
#         data = {'total_lost': total_lost, 'total_found': total_found}
#         serializer = StatsSerializer(data)
#         return Response(serializer.data)

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Disc, User
from .serializers import DiscSerializer, RecentDiscSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class DiscListCreateAPIView(ListCreateAPIView):
    queryset = Disc.objects.all()
    serializer_class = DiscSerializer

class DiscDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Disc.objects.all()
    serializer_class = DiscSerializer

class RecentDiscsAPIView(ListAPIView):
    serializer_class = RecentDiscSerializer

    def get_queryset(self):
        # Get the most recent discs (limit to 10)
        return Disc.objects.order_by('-created_at')[:10]

class StatsAPIView(APIView):
    def get(self, request):
        total_lost = Disc.objects.filter(status='lost').count()
        total_found = Disc.objects.filter(status='found').count()
        total_users = User.objects.count()
        return Response({
            'total_lost': total_lost,
            'total_found': total_found,
            'total_users': total_users,
        })
    
@login_required
def map_view(request):
    return render(request, 'disc/map.html')

@login_required
def submit_disc(request):
    if request.method == "POST":
        form = DiscForm(request.POST, request.FILES)
        if form.is_valid():
            disc = form.save(commit=False)  # Don't save yet
            disc.user = request.user  # Assign the authenticated user
            form.save()
            return redirect('disc_detail', disc_id=disc.id)
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

@login_required
def edit_disc(request, disc_id):
    disc = get_object_or_404(Disc, id=disc_id)

    # Ensure only the owner can edit
    if disc.user != request.user:
        return HttpResponseForbidden("You do not have permission to edit this disc.")

    if request.method == "POST":
        form = DiscForm(request.POST, request.FILES, instance=disc)
        if form.is_valid():
            form.save()
            return redirect("disc_detail", disc_id=disc.id)
    else:
        form = DiscForm(instance=disc)

    return render(request, "disc/edit_disc.html", {"form": form, "disc": disc})

@login_required
def delete_disc(request, disc_id):
    disc = get_object_or_404(Disc, id=disc_id)

    # Ensure the logged-in user is the owner
    if disc.user != request.user:
        messages.error(request, "You are not authorized to delete this disc.")
        return redirect('user_disc_list')

    # Delete the disc
    if request.method == "POST":
        disc.delete()
        messages.success(request, "Disc deleted successfully.")
        return redirect('user_disc_list')

    # Confirmation page
    return render(request, 'disc/delete_disc_confirm.html', {'disc': disc})