#!/bin/bash
cd ~/Workspace/django_virtual_environments/pygrdtvenv
source bin/activate
celery -A pygrdt worker -l info
