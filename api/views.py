from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from .models import ShellModel
from .serializers import ShellSerializer
from rest_framework.permissions import IsAuthenticated

import docker

client = docker.from_env()


# Create your views here.

class Shells(generics.GenericAPIView):
    serializer_class = ShellSerializer
    permission_classes = [IsAuthenticated]

    # def create_container(**kwargs):

    #     client.containers.run(
    #         image=kwargs.get('image_name', 'lechiennn/test-butterfly:3.0'),
    #         name=kwargs.get('container_name', 'test'),
    #         hostname=kwargs.get('hostname','cloudshell'),
    #         ports=kwargs.get('port', {57575:57575}),
    #         detach=kwargs.get('detach', True),
    #         mem_limit=kwargs.get('mem_limit','1g'),
    #         auto_remove=kwargs.get('auto_remove', True), 
    #     )

    def get_volume(self, id: str):
        if id not in client.volumes.list():
            volume = client.volumes.create(id)
        else:
            volume = client.volumes.get(id)
        return volume

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            volume = self.get_volume(request.data['userID'])
            
            client.containers.run(
                image='lechiennn/test-butterfly:3.0',
                command=f'--max-session={request.data.get("max-session",4)}',
                name=request.data['userID'],
                hostname=request.data.get('hostname','cloudshell'),
                ports={57575:request.data['port']},
                volumes={volume.name:{'bind': '/home/demo', 'mode': 'rw'}},
                detach=True,
                mem_limit=request.data.get('mem_limit', '1g'),
                auto_remove=True, 
            )
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ShellDetail(generics.GenericAPIView):
    serializer_class = ShellSerializer


    def delete(self, request, id):
        try:
            instance = ShellModel.objects.filter(userID=id)
            container = client.containers.get(id)
            container.stop()
            instance.delete()
            return Response({"status": "success"}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "fail", "message": f'no such container {id}'}, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    client.containers.run(
        image='lechiennn/test-butterfly:3.0',
        name='test-api',
        hostname='cloudshell',
        ports={57575:57575},
        detach=True,
        mem_limit='1g',
        auto_remove=True, 
        )
    return HttpResponse("Hello, world!")