from rest_framework import serializers
from Movie.models import Movies
from rest_framework.exceptions import ValidationError
from datetime import datetime

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'

    def validate(self,attrs):
        if self.instance is None:
            title = attrs.get('title')
            director = attrs.get('director')
            genre= attrs.get('genre')
            release_date = attrs.get('release_date')
            if not title:
                raise serializers.ValidationError("title field is required.")
            if len(title) > 255:
                raise serializers.ValidationError("title cannot exceed 255 characters.")

            if not director:
                raise serializers.ValidationError("director field is required.")
            if len(director) > 100:
                raise serializers.ValidationError("director name cannot exceed 100 characters.")

            if not genre:
                raise serializers.ValidationError("genre field is required.")
            if len(genre) >= 100:
                raise serializers.ValidationError("genre cannot exceed 100 characters.")

            if not release_date:
                raise serializers.ValidationError("release_date field is required.")
            try:
                datetime.strptime(str(release_date), '%Y-%m-%d')
            except ValueError:
                raise serializers.ValidationError("Invalid release date format. Use 'YYYY-MM-DD'.")
            
            return attrs
        else:
            fields = ['title', 'director', 'genre', 'release_date']
            for field in fields:
                if field in attrs:
                    value = attrs[field]
                    if field == 'title':
                        # if not value:
                        #     raise ValidationError("title field is required.")
                        if len(value) > 255:
                            raise ValidationError("title cannot exceed 255 characters.")
                    elif field == 'director':
                        # if not value:
                        #     raise ValidationError("irector field is required.")
                        if len(value) > 100:
                            raise ValidationError("director name cannot exceed 100 characters.")
                    elif field == 'genre':
                        # if not value:
                        #     raise ValidationError("Genre field is required.")
                        if len(value) > 100:
                            raise ValidationError("genre cannot exceed 100 characters.")
                    elif field == 'release_date':
                        # if not value:
                        #     raise ValidationError("Release date field is required.")
                        try:
                            datetime.strptime(str(value), '%Y-%m-%d')
                        except ValueError:
                            raise ValidationError("Invalid release date format. Use 'YYYY-MM-DD'.")
            return attrs