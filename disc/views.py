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
from django.db.models import Q  # For matching
from django.utils.timezone import now

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
from django.core.serializers.json import DjangoJSONEncoder

class DiscSearchView(FilterView):
    model = Disc
    template_name = 'disc/disc_search.html'
    filterset_class = DiscFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filtered queryset with valid lat/lng
        filtered_qs = self.object_list.exclude(latitude=0, longitude=0)

        # Serialize results
        serializer = DiscMapSerializer(filtered_qs, many=True)

        # Add JSON data for map
        context['discs_data'] = json.dumps(serializer.data, cls=DjangoJSONEncoder)

        return context
    
# import logging
# from django.http import HttpResponse

# def disc_search_view(request):
#     """
#     Renders the search page with filters and a map displaying the results.
#     """
#     # # Exclude discs with invalid coordinates
#     # queryset = Disc.objects.exclude(latitude=0, longitude=0)
#     # # Apply filters
#     # filter_set = DiscFilter(request.GET, queryset=queryset)

#     # # Serialize filtered results
#     # serializer = DiscMapSerializer(filter_set.qs, many=True)

#     # logger = logging.getLogger(__name__)
#     # logger.debug('Serialized disc data: %s', serializer.data)

#     # print("Filter count:", filter_set.qs.count())
#     # print("Serialized:", serializer.data)

#     # # Pass serialized data and filter to the context
#     # context = {
#     #     'filter': filter_set,
#     #     'discs_data': json.dumps(serializer.data, cls=DjangoJSONEncoder),  # Convert to JSON for JavaScript
#     # }

#     queryset = Disc.objects.exclude(latitude=0, longitude=0)
#     serializer = DiscMapSerializer(queryset, many=True)

#     print("Total Discs:", Disc.objects.count())
#     print("Valid Lat/Lng:", Disc.objects.exclude(latitude=0, longitude=0).count())

#     return HttpResponse(json.dumps(serializer.data, cls=DjangoJSONEncoder), content_type="application/json")

#     return render(request, 'disc/disc_search.html', context)

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

@login_required
def user_disc_list(request):
    discs = Disc.objects.filter(user=request.user)
    # lost_discs = Disc.objects.filter(user=request.user, status="lost", state="active")
    # found_discs = Disc.objects.filter(user=request.user, status="found", state="active")

    last_login = request.user.last_login or now()

    new_matches_count = 0
    match_flags = {}  # disc.id: has_new_match

    for disc in discs:
        if disc.status == 'lost':
            matches = DiscMatch.objects.filter(lost_disc=disc)
        elif disc.status == 'found':
            matches = DiscMatch.objects.filter(found_disc=disc)
        else:
            matches = DiscMatch.objects.none()

        disc.match_count = matches.count()
        has_new = matches.filter(created_at__gt=last_login).exists()
        match_flags[disc.id] = has_new

        if has_new:
            new_matches_count += 1

    # Filter from already annotated discs
    lost_discs = [disc for disc in discs if disc.status == "lost" and disc.state == "active"]
    found_discs = [disc for disc in discs if disc.status == "found" and disc.state == "active"]

    return render(request, "disc/user_disc_list.html", {
        "discs": discs,
        "lost_discs": lost_discs,
        "found_discs": found_discs,
        "new_matches_count": new_matches_count,
        "match_flags": match_flags
    })

# @login_required
# def user_disc_list(request):
#     all_discs = Disc.objects.filter(user=request.user)

#     # Filter by status/state
#     lost_discs = all_discs.filter(status='lost')
#     found_discs = all_discs.filter(status='found')
#     returned_discs = all_discs.filter(state='returned')
#     archived_discs = all_discs.filter(state='archived')

#     last_login = request.user.last_login or now()
#     new_matches_count = 0
#     match_flags = {}

#     for disc in all_discs:
#         if disc.status == 'lost':
#             matches = DiscMatch.objects.filter(lost_disc=disc)
#         elif disc.status == 'found':
#             matches = DiscMatch.objects.filter(found_disc=disc)
#         else:
#             matches = DiscMatch.objects.none()

#         disc.match_count = matches.count()
#         has_new = matches.filter(created_at__gt=last_login).exists()
#         match_flags[disc.id] = has_new
#         if has_new:
#             new_matches_count += 1

#     return render(request, "disc/user_disc_list.html", {
#         "lost_discs": lost_discs,
#         "found_discs": found_discs,
#         "returned_discs": returned_discs,
#         "archived_discs": archived_discs,
#         "new_matches_count": new_matches_count,
#         "match_flags": match_flags,
#     })


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

@login_required
def send_match_message(request, disc_id, matched_disc_id):
    your_disc = get_object_or_404(Disc, id=disc_id)
    matched_disc = get_object_or_404(Disc, id=matched_disc_id)

    # Determine recipient
    recipient = matched_disc.user
    sender = request.user

    content = f"It's a match! I think your disc ({matched_disc.color} {matched_disc.mold_name}) matches mine. Let's connect!"

    Message.objects.create(
        sender=sender,
        receiver=recipient,
        disc=matched_disc,
        content=content
    )

    return redirect('disc_detail', disc_id=disc_id)

@login_required
def mark_disc_returned(request, disc_id):
    disc = get_object_or_404(Disc, id=disc_id, user=request.user)
    disc.state = 'returned'
    disc.save()
    return redirect('user_disc_list')

@login_required
def user_disc_archive(request):
    archived_discs = Disc.objects.filter(
        user=request.user,
        state__in=["archived", "returned"]
    ).order_by("-created_at")

    return render(request, "disc/user_disc_archive.html", {
        "archived_discs": archived_discs
    })

@login_required
def reactivate_disc(request, disc_id):
    disc = get_object_or_404(Disc, id=disc_id, user=request.user)
    if request.method == 'POST':
        disc.state = 'active'
        disc.save()
        return redirect('user_disc_list')