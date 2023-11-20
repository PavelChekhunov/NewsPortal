from django_filters import FilterSet, ModelMultipleChoiceFilter, CharFilter, DateFilter
from .models import Post, Category
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class PostFilter(FilterSet):
    title = CharFilter(
        label='Заголовок',
        lookup_expr='icontains'
    )

    datetime_created = DateFilter(
        label="Дата создания",
        widget=DateInput(
            attrs={
                'class': 'datepicker'
            }
        ),
        lookup_expr='gt'
    )

    category = ModelMultipleChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Категория',
    )

    class Meta:
        model = Post
        fields = {
        }
