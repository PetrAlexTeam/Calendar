{% extends "Calendar/base.html" %}
{% load static %}

{% block title %} Главная {% endblock %}

{% block body %}

      <div class="">
        <img class="my_background-image" src="{% static 'img/calendar-background.jpg' %}" id ="my_back" data-image-width="600" data-image-height="398">
      </div>
{% endblock %}
