from rest_framework import serializers
from .models import Project, Tag, Document, Question, Text_pair, Action_Document, Action_Question, Action_TextPair

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "subject", "description", "category", "created_at", "size" ,"author" ]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name","project"]

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id","content","type_label", "project"]

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id","question","answer","type_label", "project"]

class TextPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text_pair
        fields = ["id","paragraph_1","paragraph_2","type_label", "project"]

class ActionDocumentSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many = True)
    class Meta:
        model = Action_Document
        fields = ["id","document","author", "project","tag"]

    def create(self, validated_data):
        tags_data = validated_data.pop('tag')
        project_data = validated_data.pop('project')
        data = Action_Document.objects.create(project=project_data, **validated_data)

        for tag_data in tags_data:
            tag = Tag.objects.get(name=tag_data['name'], project=project_data)
            data.tag.add(tag)
        
        return data
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tag')
        project_data = validated_data.pop('project')
        instance = super().update(instance, validated_data)
        instance.tag.clear()

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'], project=project_data)
            instance.tag.add(tag)

        return instance

class ActionQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action_Question
        fields = ["id","question","author", "project","tag"]

class ActionTextPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action_TextPair
        fields = ["id","text_pair","author", "project","tag"]
    # tags = TagSerializer(many = True)
    # def create(self, validated_data):
    #     # Get the tags data
    #     tags_data = validated_data.pop('tags')
    #     # Get the project data
    #     project_data = validated_data.pop('project')
    #     # Create the data instance
    #     data = Data.objects.create(**validated_data)
    #     # Create new tags or get existing ones
    #     for tag_data in tags_data:
    #         tag = Tag.objects.get(name=tag_data['name'], project=project_data)
    #         # Add the tags to the data instance
    #         data.tags.add(tag)
    #     # Return the data instance
    #     return data
    
    # def update(self, instance, validated_data):
    #     # Get the tags data
    #     tags_data = validated_data.pop('tags')
    #     # Get the project data
    #     project_data = validated_data.pop('project')
    #     # Update the other fields
    #     instance = super().update(instance, validated_data)
    #     # Clear the existing tags
    #     instance.tags.clear()
    #     # Create new tags or get existing ones
    #     for tag_data in tags_data:
    #         tag = Tag.objects.get(name=tag_data['name'], project=project_data)
    #         # Add the tags to the instance
    #         instance.tags.add(tag)
    #     # Return the updated instance
    #     return instance