from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from sistema_monitoreo_app.api.serializers import (MedicionSerializer,
                                          MedicionMinMaxDatesSerializer)
from sistema_monitoreo_app.models import Medicion

from ontoParser import get_list_of_rules

# class MedicionCreateAPIView(ListCreateAPIView):
#     queryset = Medicion.objects.all()
#     serializer_class = MedicionSerializer


class MedicionListAPIView(ListAPIView):
    # View used to get all the Mediciones data current stored in the DB in json format
    # Used: True
    queryset = Medicion.objects.all()
    serializer_class = MedicionSerializer


class MedicionMinMaxDates(APIView):
    # View used to get the min date and max date of the all Mediciones stored in DB
    # Used: True
    def get(self, request):
        dates = Medicion.objects.values("date")  # Get a dictionary of all date fields
        dates = MedicionMinMaxDatesSerializer(dates, many=True).data  # Parse django format to json format
        results = [{"min": dates[0]['date']},
                   {"max": dates[-1]['date']}]
        return Response(results)


class Predict(APIView):
    # Used: False
    def get(self, request):
        queryset = Medicion.objects.all()
        return Response({'profiles': queryset})

    # def post(self, request, pk):
    #     medicion = get_object_or_404(Medicion, pk=pk)
    #     serializer = MedicionSerializer(medicion, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        print(request.data)
        predictions = []
        model_file = os.path.join(settings.MODEL_ROOT, 'model_random_forrest.sav')
        model = joblib.load(model_file)
        try:
            result = model.predict(pd.DataFrame(request.data, index=[0]))
            predictions.append(result[0])
        except Exception as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)
        print(predictions)
        return Response(predictions, status=status.HTTP_200_OK)


class ReglasView(APIView):
    # Used: False
    def get(self, request):
        data = get_list_of_rules()
        results = ReglaSerializer(data, many=True).data
        return Response(results)