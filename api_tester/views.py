from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.cache import cache
import requests
import json
import redis

from .forms import APIRequestForm
from .models import APIRequest

def index(request):
    """
    Main view for the API tester form and results display
    """
    form = APIRequestForm()
    api_response = None
    error_message = None
    
    # Get the last request from cache if available
    cached_response = cache.get('last_api_response')
    
    if request.method == 'POST':
        form = APIRequestForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            method = form.cleaned_data['method']
            headers = form.cleaned_data['headers']
            body = form.cleaned_data['body']
            
            try:
                # Make the API request
                if method == 'GET':
                    response = requests.get(url, headers=headers)
                elif method == 'POST':
                    response = requests.post(url, headers=headers, json=json.loads(body) if body else None)
                elif method == 'PUT':
                    response = requests.put(url, headers=headers, json=json.loads(body) if body else None)
                elif method == 'DELETE':
                    response = requests.delete(url, headers=headers, json=json.loads(body) if body else None)
                
                # Try to parse response as JSON
                try:
                    response_body = response.json()
                except ValueError:
                    response_body = response.text
                
                # Create API response object
                api_response = {
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'body': response_body,
                    'time': response.elapsed.total_seconds()
                }
                
                # Save to cache
                cache.set('last_api_response', api_response, timeout=3600)  # Cache for 1 hour
                
                # Save to database
                api_request = APIRequest(
                    url=url,
                    method=method
                )
                api_request.set_headers(headers)
                api_request.set_request_body(body)
                api_request.set_response_data(
                    response.status_code,
                    response.headers,
                    response_body
                )
                api_request.save()
                
            except requests.exceptions.RequestException as e:
                error_message = f"Error making request: {str(e)}"
            except json.JSONDecodeError:
                error_message = "Invalid JSON in request body"
    
    # If we have a cached response and no new response, use the cached one
    if not api_response and cached_response:
        api_response = cached_response
    
    # Get recent API requests for history
    recent_requests = APIRequest.objects.all()[:10]
    
    context = {
        'form': form,
        'api_response': api_response,
        'error_message': error_message,
        'recent_requests': recent_requests
    }
    
    return render(request, 'api_tester/index.html', context)

def request_detail(request, request_id):
    """
    View for displaying details of a specific API request
    """
    try:
        api_request = APIRequest.objects.get(id=request_id)
        
        # Format the response for display
        api_response = {
            'status_code': api_request.response_status,
            'headers': api_request.response_headers,
            'body': api_request.response_body,
        }
        
        context = {
            'api_request': api_request,
            'api_response': api_response,
        }
        
        return render(request, 'api_tester/detail.html', context)
        
    except APIRequest.DoesNotExist:
        return redirect('index')

def clear_history(request):
    """
    View for clearing the API request history
    """
    if request.method == 'POST':
        APIRequest.objects.all().delete()
        cache.delete('last_api_response')
    
    return redirect('index')
