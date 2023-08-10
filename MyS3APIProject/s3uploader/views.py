from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FileUploadSerializer
import boto3
import requests
import mimetypes


class S3Uploader(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            name = url.split('/')[-1]
            s3_bucket = 'shravanm683'
            s3_key = name
            filename = name

            response = requests.get(url)
            if response.status_code == 200:
                s3_client = boto3.client('s3')
                content_type = self.get_content_type(filename)
                s3_client.put_object(Bucket=s3_bucket, Key=s3_key, Body=response.content, ContentType=content_type)
                return Response({"message": "File uploaded successfully to S3."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Failed to download the file from the URL."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_content_type(self, filename):
        content_type, _ = mimetypes.guess_type(filename)
        return content_type or 'application/octet-stream'

from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def upload_data(request):
    # Your logic for handling the POST request goes here
    # Process the uploaded data and return an appropriate response
    return Response({"message": "Data uploaded successfully."})
