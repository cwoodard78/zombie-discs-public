from rest_framework.viewsets import ModelViewSet
from .models import MyModel
from .serializers import MyModelSerializer
from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from .models import Disc
from django.views.decorators.csrf import csrf_exempt
import json

class MyModelViewSet(ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

def map_view(request):
    return render(request, "map.html")

def submit_disc(request):
    if request.method == "POST":
        status = request.POST.get("type")
        color = request.POST.get("color")
        notes = request.POST.get("notes")
        coordinates = request.POST.get("coordinates")

        if coordinates:
            latitude, longitude = map(float, coordinates.split(','))

            # Save the data to the database
            disc = Disc.objects.create(
                status=status,
                color=color,
                notes=notes,
                latitude=latitude,
                longitude=longitude
            )

            return JsonResponse({"message": "Disc entry submitted successfully!"})
        return JsonResponse({"error": "Coordinates missing!"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def save_coordinates(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            # For now, just log the coordinates
            print(f"Coordinates received: {latitude}, {longitude}")
            return JsonResponse({"message": "Coordinates saved successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)

def disc_list(request):
    discs = Disc.objects.all()
    return render(request, "disc_list.html", {"discs": discs})