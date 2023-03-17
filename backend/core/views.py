from json import JSONDecodeError

from rest_framework import status, views
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .serializer import ContactSerializer


class ContactAPIView(views.APIView):
    serializer_class = ContactSerializer
    json_parser = JSONParser()

    def get_serializer_context(self):
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request):
        try:
            data = ContactAPIView.json_parser.parse(request)
            serializer = ContactSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return Response(
                {
                    "result": "error",
                    "message": "JSON decoding error.",
                    "status": status.HTTP_400_BAD_REQUEST,
                }
            )
