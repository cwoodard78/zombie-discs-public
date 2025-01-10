from rest_framework.viewsets import ModelViewSet
from .models import MyModel
from .serializers import MyModelSerializer
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from .models import Disc
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import DiscForm

class MyModelViewSet(ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

def map_view(request):
    return render(request, 'disc/map.html')

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

def disc_detail(request, disc_id):
    disc = get_object_or_404(Disc, id=disc_id)
    return render(request, "disc/disc_detail.html", {"disc": disc})

# # THIS WORKS
# def submit_disc(request):
#     if request.method == "POST":
#         # Extract the form data from the request
#         status = request.POST.get("type")  # 'type' matches the radio button name
#         color = request.POST.get("color")
#         notes = request.POST.get("notes")
#         coordinates = request.POST.get("coordinates")  # Single field for lat,lng

#         # Check for coordinates and split them into latitude and longitude
#         if coordinates:
#             try:
#                 latitude, longitude = map(float, coordinates.split(','))  # Parse coordinates
#             except ValueError:
#                 return JsonResponse({"error": "Invalid coordinates format!"}, status=400)

#             # Create the Disc object and save it to the database
#             disc = Disc.objects.create(
#                 status=status,
#                 color=color,
#                 notes=notes,
#                 latitude=latitude,
#                 longitude=longitude
#             )

#             # Return a success response
#             return JsonResponse({"message": "Disc entry submitted successfully!"})
        
#         # Handle missing coordinates
#         return JsonResponse({"error": "Coordinates are missing!"}, status=400)

#     # Handle non-POST requests
#     return JsonResponse({"error": "Invalid request method!"}, status=400)