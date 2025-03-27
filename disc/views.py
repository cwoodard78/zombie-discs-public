from rest_framework.viewsets import ModelViewSet
# from .models import MyModel
# from .serializers import MyModelSerializer
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from .models import Disc, DiscMatch
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import DiscForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# For APIs
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Disc, User, Reward
from .serializers import DiscSerializer, RecentDiscSerializer, DiscMapSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from django.forms.models import model_to_dict
from .filters import DiscFilter
from django.core.serializers import serialize

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

# class DiscMapAPIView(APIView):
#     """API view to fetch disc data for the map."""

#     def get(self, request):
#         discs = Disc.objects.exclude(latitude__isnull=True, longitude__isnull=True)
#         serializer = DiscMapSerializer(discs, many=True)
#         return Response(serializer.data)

class DiscMapAPIView(ListAPIView):
    serializer_class = DiscMapSerializer

    def get_queryset(self):
        # Exclude discs with latitude and longitude both equal to 0
        return Disc.objects.exclude(latitude=0, longitude=0)

from django_filters.views import FilterView
from .filters import DiscFilter

class DiscSearchView(FilterView):
    model = Disc
    template_name = 'disc/disc_search.html'
    filterset_class = DiscFilter

def disc_search_view(request):
    """
    Renders the search page with filters and a map displaying the results.
    """
    # Exclude discs with invalid coordinates
    queryset = Disc.objects.exclude(latitude=0, longitude=0)
    # Apply filters
    filter_set = DiscFilter(request.GET, queryset=queryset)

    # Serialize filtered results
    serializer = DiscMapSerializer(filter_set.qs, many=True)

    # Pass serialized data and filter to the context
    context = {
        'filter': filter_set,
        'discs_data': json.dumps(serializer.data),  # Convert to JSON for JavaScript
    }

    return render(request, 'disc/disc_search.html', context)

# def search_discs(request):
#     filter = DiscFilter(request.GET, queryset=Disc.objects.all())
#     discs = filter.qs
#     discs_data = [model_to_dict(disc, fields=['id', 'color', 'type', 'status', 'manufacturer', 'latitude', 'longitude', 'notes']) for disc in discs]
#     return render(request, 'disc/search.html', {'filter': filter, 'discs_data': discs_data})

def disc_map_view(request):
    """View for displaying all discs on a map."""
    return render(request, 'disc/disc_map.html')
    
@login_required
def map_view(request):
    return render(request, 'disc/map.html')

@login_required
def submit_disc(request):
    if request.method == "POST":
        form = DiscForm(request.POST, request.FILES)
        reward_amount = request.POST.get("reward")  

        if form.is_valid():
            disc = form.save(commit=False)  # Don't save yet
            disc.user = request.user  # Assign the authenticated user
            form.save()

            # Create a Reward entry if reward is provided and valid
            if reward_amount:
                try:
                    reward_value = float(reward_amount)
                    if reward_value > 0:
                        Reward.objects.create(disc=disc, amount=reward_value)
                except ValueError:
                    pass

            return redirect('disc_detail', disc_id=disc.id)
        else:
            return JsonResponse({"errors": form.errors}, status=400)

    # For GET requests, render the form
    form = DiscForm()
    return render(request, "disc/submit_disc.html", {"form": form})

@login_required
def disc_detail(request, disc_id):
    disc = get_object_or_404(Disc, id=disc_id)
    from_user_disc_list = request.GET.get("from_user_disc_list", "false").lower() == "true"
    return render(request, "disc/disc_detail.html", {"disc": disc, "from_user_disc_list": from_user_disc_list})

from inbox.models import Message  # Import Message model

@login_required
def disc_detail_view(request, disc_id):
    disc = get_object_or_404(Disc, id=disc_id)
    if disc.status == 'lost':
        matches = DiscMatch.objects.filter(lost_disc=disc).select_related('found_disc')
    else:
        matches = DiscMatch.objects.filter(found_disc=disc).select_related('lost_disc')

    # Get messages related to this disc
    messages = Message.objects.filter(disc=disc).select_related('sender', 'receiver').order_by('-timestamp')

    # # Debugging: Print matches to the console
    # print(f"Disc: {disc}")
    # print(f"Matches: {matches}")
    # for match in matches:
    #     print(f"Lost Disc ID: {match.lost_disc.id}, Found Disc ID: {match.found_disc.id}, Score: {match.score}")

    return render(request, "disc/disc_detail.html", {
        "disc": disc,
        "matches": matches,
        "messages": messages,
    }
    )


# @login_required
# def user_disc_list(request):
#     discs = Disc.objects.filter(user=request.user)
#     return render(request, "disc/user_disc_list.html", {"discs": discs})

@login_required
def user_disc_list(request):
    discs = Disc.objects.filter(user=request.user)

    # Add match counts to each disc
    for disc in discs:
        if disc.status == 'lost':
            disc.match_count = DiscMatch.objects.filter(lost_disc=disc).count()
        elif disc.status == 'found':
            disc.match_count = DiscMatch.objects.filter(found_disc=disc).count()
        else:
            disc.match_count = 0

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
