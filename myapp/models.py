from django.db import models
import hashlib
import uuid
from .helpers.formater import format_as_gpt_print

class Conversation(models.Model):
    guid = models.CharField(max_length=16, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=60, default=None)
    
    def save(self, *args, **kwargs):
        if not self.guid:
            # Generate a unique hash for the guid field
            self.guid = hashlib.sha1(uuid.uuid4().bytes).hexdigest()[:16]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    file_id = models.CharField(max_length=50, blank=False, null=True)
    agent = models.CharField(max_length=100, null=False, blank=False) 

    def __str__(self):
        return f"{self.conversation.title} - Message {self.pk}"
    
    def getQuestion(self):
        return format_as_gpt_print(self.question)
    
    def getAnswer(self):
        return format_as_gpt_print(self.answer)
    