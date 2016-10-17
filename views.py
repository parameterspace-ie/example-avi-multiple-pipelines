"""
GAVIP Example AVIS: Multiple Pipeline AVI

All Django view functions
"""

from collections import defaultdict
from itertools import chain
import json
import time
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.views.decorators.http import require_http_methods
from django.utils import formats

from avi.forms import GacsIgslAnalysisJobForm, NoisySpectraJobForm
from avi.models import GacsIgslAnalysisJob, NoisySpectraJob

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_default_context():
    return {'gacsform': GacsIgslAnalysisJobForm(),
            'spectraform' : NoisySpectraJobForm()}


@require_http_methods(["GET"])
def index(request):
    """
    There are multiple pipelines in this AVI.
    By default, the index view contains the form where the user can specify the Run Ulysses parameters
    for the corresponding pipeline.
    
    We send a dictionary called a context, which contains 
    'millis' and 'standalone' variables.
    """
    context = get_default_context()
    context.update({
        "millis": int(round(time.time() * 1000)),
        "show_welcome": request.session.get('show_welcome', True)
    })
    request.session['show_welcome'] = False
    
    return render(request, 'avi/index.html', context=context)


@require_http_methods(["POST"])
def run_ulysses(request):
    """
    Starts the Ulysses pipeline

    TODO - minor issue in rendering for invalid forms
    """
    logger.info('request.POST: %s', str(request.POST))

    form = NoisySpectraJobForm(request.POST)
        
    if form.is_valid():
        job_model = form.save()
        logger.info('Ulysses pipeline job has been successfully created')
    else:
        logger.error('Ulysses input parameters form is invalid')

    return redirect('%s#job-tab' % resolve_url('avi:index'))


@require_http_methods(["POST"])
def run_gacsigsl(request):
    """
    Starts the GACS-dev IGSL pipeline
    
    TODO - minor issue in rendering for invalid forms
    """
    logger.info('request.POST: %s', str(request.POST))

    form = GacsIgslAnalysisJobForm(request.POST)
    if form.is_valid():
        form.save()
        logger.info('IGSL pipeline job has been successfully created')
    else:
        logger.error('IGSL input parameters form is invalid')

    return redirect('%s#job-tab' % resolve_url('avi:index'))



@require_http_methods(["GET"])
def job_result(request, job_id):
    job = AviJobRequest.objects.get(job_id=job_id)
    file_path = job.request.result_path
    context = get_default_context()
    with open(file_path, 'r') as out_file:
        context.update(json.load(out_file))
    logger.info('Returning context: %s' % context)
    return render(request, 'avi/job_result.html', context=context)


@require_http_methods(["GET"])
def help_documentation(request):
    """
    Render AVI Help Documentation
    """
    return render(request, 'avi/help.html', context={})

