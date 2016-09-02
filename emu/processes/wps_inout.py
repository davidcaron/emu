from pywps import Process
from pywps import LiteralInput, LiteralOutput
from pywps import BoundingBoxInput, BoundingBoxOutput
from pywps import ComplexInput, ComplexOutput
from pywps import Format, FORMATS

import logging
LOGGER = logging.getLogger("PYWPS")


class InOut(Process):
    """
    This process defines several types of literal type of in- and outputs.

    TODO: add literal input with value range[(0,100)] ... see pywps doc
    """

    def __init__(self):
        inputs = [
            LiteralInput('string', 'String', data_type='string',
                         abstract='Enter a simple string.',
                         default="This is just a string"),
            LiteralInput('int', 'Integer', data_type='integer',
                         abstract='Enter an integer number.',
                         default="7"),
            LiteralInput('float', 'Float', data_type='float',
                         abstract='Enter a float number.',
                         default="3.14"),
            # TODO: boolean default is not displayed in phoenix
            LiteralInput('boolean', 'Boolean', data_type='boolean',
                         abstract='Make your choice :)',
                         default='1'),
            LiteralInput('time', 'Time', data_type='time',
                         abstract='Enter a time like 2016-09-02.',
                         default='2016-09-02'),
            LiteralInput('string_choice', 'String Choice', data_type='string',
                         abstract='Choose one item form list.',
                         allowed_values=['one', 'two', 'three'],
                         default='two'),
            LiteralInput('string_multiple_choice', 'String Multiple Choice',
                         abstract='Choose one or two items from list.',
                         data_type='string',
                         allowed_values=['one', 'two', 'three', 'four'],
                         min_occurs=1, max_occurs=2,
                         default='three'),
            # BoundingBoxInput('bbox', 'Bounding Box', ['epsg:4326', 'epsg:3035']),
            ComplexInput('text', 'Text',
                         abstract='Enter a URL pointing to a text document (optional)',
                         min_occurs=0,
                         supported_formats=[Format('text/plain')])


        ]
        outputs = [
            LiteralOutput('string', 'String', data_type='string'),
            LiteralOutput('int', 'Integer', data_type='integer'),
            LiteralOutput('float', 'Float', data_type='float'),
            LiteralOutput('boolean', 'Boolean', data_type='boolean'),
            LiteralOutput('time', 'Time', data_type='time'),
            LiteralOutput('string_choice', 'String Choice',
                          data_type='string'),
            LiteralOutput('string_multiple_choice', 'String Multiple Choice',
                          data_type='string'),
            # BoundingBoxOutput('bbox', 'Boudning Box', ['epsg:4326']),
            ComplexOutput('text', 'Text',
                          as_reference=True,
                          supported_formats=[Format('text/plain')]),
        ]

        super(InOut, self).__init__(
            self._handler,
            identifier="inout",
            title="InOut",
            version="1.0",
            abstract="Testing all WPS input and output parameters.",
            inputs=inputs,
            outputs=outputs,
            status_supported=True,
            store_supported=True
            )

    def _handler(self, request, response):
        response.outputs['string'].data = request.inputs['string'][0].data
        response.outputs['int'].data = request.inputs['int'][0].data
        response.outputs['float'].data = request.inputs['float'][0].data
        response.outputs['boolean'].data = request.inputs['boolean'][0].data
        response.outputs['time'].data = request.inputs['time'][0].data
        response.outputs['string_choice'].data = \
            request.inputs['string_choice'][0].data
        response.outputs['string_multiple_choice'].data = ', '.join(
            [inpt.data for inpt in request.inputs['string_multiple_choice']])
        # TODO: bbox is not working
        # response.outputs['bbox'].data = request.inputs['bbox'][0].data
        # TODO: how to copy file?
        if 'text' in request.inputs:
            response.outputs['text'].output_format = FORMATS.TEXT
            response.outputs['text'].file = request.inputs['text'][0].file
        return response
