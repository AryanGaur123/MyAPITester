from django.db import models
import json

# Create your models here.

class APIRequest(models.Model):
    METHOD_CHOICES = (
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    )
    
    url = models.URLField(max_length=500)
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)
    headers = models.JSONField(default=dict, blank=True)
    request_body = models.JSONField(default=dict, blank=True, null=True)
    response_status = models.IntegerField(null=True, blank=True)
    response_headers = models.JSONField(default=dict, blank=True)
    response_body = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.method} {self.url} - {self.response_status}"
    
    def set_headers(self, headers_dict):
        self.headers = headers_dict
    
    def set_request_body(self, body):
        if body:
            try:
                # Try to parse as JSON if it's a string
                if isinstance(body, str):
                    self.request_body = json.loads(body)
                else:
                    self.request_body = body
            except json.JSONDecodeError:
                # If it's not valid JSON, store as a string
                self.request_body = {"raw": body}
        else:
            self.request_body = None
    
    def set_response_data(self, status, headers, body):
        self.response_status = status
        self.response_headers = dict(headers)
        
        if body:
            try:
                if isinstance(body, str):
                    self.response_body = json.loads(body)
                else:
                    self.response_body = body
            except json.JSONDecodeError:
                self.response_body = {"raw": body}
        else:
            self.response_body = None
