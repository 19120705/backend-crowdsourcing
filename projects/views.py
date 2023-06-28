from rest_framework import viewsets, status

from .models import *
from .serializers import *

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status

# Create your views here.


class RegisterViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                serializer.initial_data['username'],
                serializer.initial_data['email'],
            )
            user.set_password(serializer.initial_data['password'])
            user.save()
            return Response({'status': 'User created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh',
    ]
    return Response(routes)



@permission_classes([IsAuthenticated])
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(active = True)
    serializer_class = ProjectSerializer


@permission_classes([IsAuthenticated])
class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    def get_queryset(self):
        project = self.request.query_params.get('project')
        if project:
            return Tag.objects.filter(project=project)
        return Tag.objects.all()
        

@permission_classes([IsAuthenticated])
class QuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    def get_queryset(self):
        project = self.request.query_params.get('project')
        if project:
            return Question.objects.filter(project=project)
        else:
            return Question.objects.all()

@permission_classes([IsAuthenticated])
class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    def get_queryset(self):
        project = self.request.query_params.get('project')
        if project:
            return Document.objects.filter(project=project)
        else:
            return Document.objects.all()
        
@permission_classes([IsAuthenticated])
class TextPairViewSet(viewsets.ModelViewSet):
    serializer_class = TextPairSerializer
    def get_queryset(self):
        project = self.request.query_params.get('project')
        if project:
            return Text_pair.objects.filter(project=project)
        else:
            return Text_pair.objects.all()

@permission_classes([IsAuthenticated])
class ActionDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = ActionDocumentSerializer
    def get_queryset(self):
        project = self.request.query_params.get('project')
        if project:
            return Action_Document.objects.filter(project=project)
        else:
            return Action_Document.objects.all()

@permission_classes([IsAuthenticated])
class ActionQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = ActionQuestionSerializer
    def get_queryset(self):
        project = self.request.query_params.get('project')
        if project:
            return Action_Question.objects.filter(project=project)
        else:
            return Action_Question.objects.all()

@permission_classes([IsAuthenticated])
class ActionTextPairViewSet(viewsets.ModelViewSet):
    serializer_class = ActionTextPairSerializer
    def get_queryset(self):
        project = self.request.query_params.get('project')
        if project:
            return Action_TextPair.objects.filter(project=project)
        else:
            return Action_TextPair.objects.all()


@permission_classes([IsAuthenticated])
# See all data(document, question, text_pair) in any project
class CompositeView(APIView):
    def get(self, request):
        project = request.query_params.get('project')

        projectModel = Project.objects.get(pk=project)
        project_serializer = ProjectSerializer(projectModel)

        tags = Tag.objects.filter(project=project)
        tags_serializer = TagSerializer(tags, many=True)

        documents = Document.objects.filter(project=project)
        document_serializer = DocumentSerializer(documents, many=True)

        questions = Question.objects.filter(project=project)
        question_serializer = QuestionSerializer(questions, many=True)

        text_pairs = Text_pair.objects.filter(project=project)
        text_pair_serializer = TextPairSerializer(text_pairs, many=True)

        data = {
                "detail":project_serializer.data,
                "tags": tags_serializer.data,
                "documents": document_serializer.data,
                "questions": question_serializer.data,
                "text_pairs": text_pair_serializer.data,
        }

        return Response(data)



        

# class DataViewSet(viewsets.ModelViewSet):
#     serializer_class = DataSerializer
#     def get_queryset(self):
#         project = self.request.query_params.get('project')
#         return Data.objects.filter(project=project, active = True) # this is correct



# class ProjectList(APIView):
#     def get(self, request):
#         project = Project.objects.all()
#         serializer = ProjectSerializer(project, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class ProjectDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Project.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         project = self.get_object(pk)
#         serializer = ProjectSerializer(project)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         project = self.get_object(pk)
#         serializer = ProjectSerializer(project, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         project = self.get_object(pk)
#         serializer = ProjectSerializer(project, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         project = self.get_object(pk)
#         project.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)




# class TagList(APIView):
#     def get(self, request):
#         project = request.query_params.get('project')
#         tags = Tag.objects.filter(project=project)
#         serializer = TagSerializer(tags, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = TagSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class TagDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Tag.objects.get(pk=pk)
#         except Tag.DoesNotExist:
#             raise Http404

#     def get(self, request, pk):
#         tag = self.get_object(pk)
#         serializer = TagSerializer(tag)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         tag = self.get_object(pk)
#         serializer = TagSerializer(tag, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk):
#         tag = self.get_object(pk)
#         serializer = TagSerializer(tag, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         tag = self.get_object(pk)
#         tag.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)





















# class ProjectList(APIView):
#     """
#     List all Projects, or create a new Project.
#     """
#     def get(self, request, format=None):
#         projects = Project.objects.all()
#         serializer = ProjectSerializer(projects, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = ProjectSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class ProjectDetail(APIView):
#     """
#     Retrieve, update or delete a Project instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Project.objects.get(pk=pk)
#         except Project.DoesNotExist:
#             raise Http404

#     def get(self, request, pk, format=None):
#         project = self.get_object(pk)
#         serializer = ProjectSerializer(project)
#         return Response(serializer.data)

#     def put(self, request, pk, format=None):
#         project = self.get_object(pk)
#         serializer = ProjectSerializer(project, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, format=None):
#         project = self.get_object(pk)
#         project.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
