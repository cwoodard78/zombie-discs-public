import json

from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.utils.timezone import now
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Sum  # For matching
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from .filters import DiscFilter

from .models import Disc, DiscMatch, User, Reward
from inbox.models import Message
from .forms import DiscForm
from .filters import DiscFilter
from .serializers import DiscSerializer, RecentDiscSerializer, DiscMapSerializer

# For APIs
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

#API VIEWS
class DiscListCreateAPIView(ListCreateAPIView):
    """
    API endpoint to list all discs or create a new one.
    """
    queryset = Disc.objects.all()
    serializer_class = DiscSerializer

class DiscDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a single disc.
    """
    queryset = Disc.objects.all()
    serializer_class = DiscSerializer

class RecentDiscsAPIView(ListAPIView):
    """
    API endpoint to fetch the 10 most recently created discs.
    """
    serializer_class = RecentDiscSerializer

    def get_queryset(self):
        # Get the most recent discs (limit to 10)
        return Disc.objects.order_by('-created_at')[:10]

class StatsAPIView(APIView):
    """
    API endpoint to fetch summary statistics for the dashboard.
    """
    def get(self, request):
        total_lost = Disc.objects.filter(status='lost', state='active').count()
        total_found = Disc.objects.filter(status='found', state='active').count()
        total_resolved = Disc.objects.filter(state='returned').count()
        total_rewards = Reward.objects.aggregate(total=Sum('amount'))['total'] or 0
        total_users = User.objects.count()
        return Response({
            'total_lost': total_lost,
            'total_found': total_found,
            'total_users': total_users,
            'total_rewards': float(total_rewards),
            'total_resolved': total_resolved,
        })

class DiscMapAPIView(ListAPIView):
    """
    API endpoint for retrieving all discs with valid GPS coordinates for map display.
    """
    serializer_class = DiscMapSerializer

    def get_queryset(self):
        # Exclude discs with latitude and longitude both equal to 0
        return Disc.objects.exclude(latitude=0, longitude=0)

class DiscSearchView(FilterView):
    """
    Renders the disc search page with filtering and map support.
    """
    model = Disc
    template_name = 'disc/disc_search.html'
    filterset_class = DiscFilter

    def get_queryset(self):
        # Only return active discs (e.g., not archived or returned)
        qs = super().get_queryset()
        return qs.filter(state='active')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filtered queryset with valid lat/lng
        filtered_qs = self.object_list.exclude(latitude=0, longitude=0)

        # Serialize results
        serializer = DiscMapSerializer(filtered_qs, many=True)
        # Add JSON data for map
        context['discs_data'] = json.dumps(serializer.data, cls=DjangoJSONEncoder)

        return context

# CORE TEMPLATE VIEWS
# Remove Google API for public hosting
# def disc_map_view(request):
#     """
#     View for displaying all discs on a map (public and private).
#     This is the Google API proof of concept and can be removed after demo.
#     """
#     return render(request, 'disc/disc_map.html')

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
def disc_detail_view(request, disc_id):
    """
    Display the detail page for a single disc, including matches and related messages.
    """
    disc = get_object_or_404(Disc, id=disc_id)
    # Match complements depend on whether lost or found
    if disc.status == 'lost':
        matches = DiscMatch.objects.filter(lost_disc=disc).select_related('found_disc')
    else:
        matches = DiscMatch.objects.filter(found_disc=disc).select_related('lost_disc')

    # Get messages related to this disc
    messages = Message.objects.filter(disc=disc).select_related('sender', 'receiver').order_by('-timestamp')

    return render(request, "disc/disc_detail.html", {
        "disc": disc,
        "matches": matches,
        "messages": messages,
    })

@login_required
def user_disc_list(request):
    """
    Show a list of the user's active discs with new match indicators.
    """
    discs = Disc.objects.filter(user=request.user, state='active')
    last_login = request.user.last_login or now()

    new_matches_count = 0
    match_flags = {}  # Map of disc.id: true for has_new_match

    for disc in discs:
        # Lost vs Found queryset
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

@login_required
def edit_disc(request, disc_id):
    """
    Allow owner of a disc to edit details.
    """
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
    """
    Allow owner to delete a disc with confirmation.
    """
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
    """
    Send a default message to the owner of a matched disc to initiate contact.
    """
    your_disc = get_object_or_404(Disc, id=disc_id)
    matched_disc = get_object_or_404(Disc, id=matched_disc_id)

    # Determine recipient
    recipient = matched_disc.user
    sender = request.user

    # Generate system match message
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
    """
    Allow owner to mark a disc as 'returned'.
    """
    disc = get_object_or_404(Disc, id=disc_id, user=request.user)
    disc.state = 'returned'
    disc.save()
    return redirect('user_disc_list')

@login_required
def user_disc_archive(request):
    """
    View for listing a user's archived and returned discs.
    """
    archived_discs = Disc.objects.filter(
        user=request.user,
        state__in=["archived", "returned"]
    ).order_by("-created_at")

    return render(request, "disc/user_disc_archive.html", {
        "archived_discs": archived_discs
    })

@login_required
def reactivate_disc(request, disc_id):
    """
    Reactivate a previously archived or returned disc.
    """
    disc = get_object_or_404(Disc, id=disc_id, user=request.user)
    if request.method == 'POST':
        disc.state = 'active'
        disc.save()
        return redirect('user_disc_list')