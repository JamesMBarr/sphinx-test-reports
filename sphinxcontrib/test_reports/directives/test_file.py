import hashlib
from docutils import nodes
from docutils.parsers.rst import directives

from sphinxcontrib.test_reports.directives import TestCommonDirective
import sphinxcontrib.test_reports.directives.test_suite
from sphinxcontrib.test_reports.exceptions import TestReportIncompleteConfiguration

from sphinxcontrib.needs.api import add_need


class TestFile(nodes.General, nodes.Element):
    pass


class TestFileDirective(TestCommonDirective):
    """
    Directive for showing test results.
    """
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    option_spec = {'id': directives.unchanged_required,
                   'status': directives.unchanged_required,
                   'tags': directives.unchanged_required,
                   'links': directives.unchanged_required,
                   'collapse': directives.unchanged_required,
                   'file': directives.unchanged_required,
                   'auto_suites': directives.flag,
                   'auto_cases': directives.flag,
                   }

    final_argument_whitespace = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self):
        self.prepare_basic_options()
        self.load_test_file()

        suites = len(self.results)
        cases = sum([int(x['tests']) for x in self.results])

        passed = sum([x['passed'] for x in self.results])
        skipped = sum([x['skips'] for x in self.results])
        errors = sum([x['errors'] for x in self.results])
        failed = sum([x['failures'] for x in self.results])

        main_section = []
        docname = self.state.document.settings.env.docname
        main_section += add_need(self.env.app, self.state, docname, self.lineno,
                                 need_type="testfile", title=self.test_name, id=self.test_id,
                                 content=self.test_content, links=self.test_links, tags=self.test_tags,
                                 status=self.test_status, collapse=self.collapse,
                                 file=self.test_file_given, suites=suites, cases=cases,
                                 passed=passed, skipped=skipped, failed=failed, errors=errors)

        if 'auto_cases' in self.options.keys() and 'auto_suites' not in self.options.keys():
            raise TestReportIncompleteConfiguration('option auto_cases must be used together with '
                                                    'auto_suites for test-file directives.')


        if 'auto_suites' in self.options.keys():
            for suite in self.results:
                suite_id = self.test_id
                suite_id += '_' + hashlib.sha1(suite['name'].encode("UTF-8")).hexdigest().upper()[:3]

                options = self.options
                options['suite'] = suite['name']
                options['id'] = suite_id

                if 'links' not in self.options:
                    options['links'] = self.test_id
                elif self.test_id not in options['links']:
                    options['links'] = options['links'] + ';' + self.test_id

                arguments = [suite['name']]
                suite_directive = sphinxcontrib.test_reports.directives.test_suite.TestSuiteDirective(
                    'test-suite', arguments, options,
                    self.content, self.lineno,
                    self.content_offset, self.block_text, self.state,
                    self.state_machine)

                main_section += suite_directive.run()

        return main_section