
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'tags', views.TagViewSet, basename='tag')
router.register(r'question', views.QuestionViewSet, basename='question')
router.register(r'document', views.DocumentViewSet, basename='document')
router.register(r'textpair', views.TextPairViewSet, basename='textpair')
router.register(r'action/question', views.ActionQuestionViewSet, basename='action_question')
router.register(r'action/document', views.ActionDocumentViewSet, basename='action_document')
router.register(r'action/textpair', views.ActionTextPairViewSet, basename='action_textpair')

urlpatterns = [
    path('',include(router.urls)),
    path('data/', views.CompositeView.as_view(), name='data-list'),
    # path('tags/', views.TagList.as_view(), name='tag-list'),
    # path('tags/<int:pk>/', views.TagDetail.as_view(), name='tag-detail'),
    # path('', views.ProjectList.as_view(), name='project-list'),
    # path('<int:pk>/', views.ProjectDetail.as_view(), name='project-detail'),
]