import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as tk


def create_country_codes():
    '''Create country_codes vocab and tags, if they don't exist already.

    Note that you could also create the vocab and tags using CKAN's API,
    and once they are created you can edit them (e.g. to add and remove
    possible dataset country code values) using the API.

    '''
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'country_codes'}
        tk.get_action('vocabulary_show')(context, data)
        logging.info("Example genre vocabulary already exists, skipping.")
    except tk.ObjectNotFound:
        logging.info("Creating vocab 'country_codes'")
        data = {'name': 'country_codes'}
        vocab = tk.get_action('vocabulary_create')(context, data)
        for tag in (u'uk', u'ie', u'de', u'fr', u'et'):
            logging.info(
                    "Adding tag {0} to vocab 'country_codes'".format(tag))
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            tk.get_action('tag_create')(context, data)


def country_codes():
    '''Return the list of country codes from the country codes vocabulary.'''
    create_country_codes()
    try:
        country_codes = tk.get_action('tag_list')(
                data_dict={'vocabulary_id': 'country_codes'})
        return country_codes
    except tk.ObjectNotFound:
        return None

def create_coverage_codes():
    '''Create coverage_codes vocab and tags, if they don't exist already.

    Note that you could also create the vocab and tags using CKAN's API,
    and once they are created you can edit them (e.g. to add and remove
    possible dataset country code values) using the API.

    '''
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'coverage_codes'}
        tk.get_action('vocabulary_show')(context, data)
        logging.info("Example genre vocabulary already exists, skipping.")
    except tk.ObjectNotFound:
        logging.info("Creating vocab 'coverage_codes'")
        data = {'name': 'coverage_codes'}
        vocab = tk.get_action('vocabulary_create')(context, data)
        for tag in (u'Global', u'Regional', u'Country', u'study Sites_extend', u'Any Other extend'):
            logging.info(
                    "Adding tag {0} to vocab 'coverage_codes'".format(tag))
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            tk.get_action('tag_create')(context, data)


def coverage_codes():
    '''Return the list of country codes from the country codes vocabulary.'''
    create_coverage_codes()
    try:
        coverage_codes = tk.get_action('tag_list')(
                data_dict={'vocabulary_id': 'coverage_codes'})
        return coverage_codes
    except tk.ObjectNotFound:
        return None

def create_time_freqs():
    '''Create coverage_codes vocab and tags, if they don't exist already.

    Note that you could also create the vocab and tags using CKAN's API,
    and once they are created you can edit them (e.g. to add and remove
    possible dataset country code values) using the API.

    '''
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'time_freqs'}
        tk.get_action('vocabulary_show')(context, data)
        logging.info("Example genre vocabulary already exists, skipping.")
    except tk.ObjectNotFound:
        logging.info("Creating vocab 'time_freqs'")
        data = {'name': 'time_freqs'}
        vocab = tk.get_action('vocabulary_create')(context, data)
        for tag in (u'yearly', u'quarterly', u'monthly', u'daily', u'hourly', u'periodical', u'aperiodical'):
            logging.info(
                    "Adding tag {0} to vocab 'time_freqs'".format(tag))
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            tk.get_action('tag_create')(context, data)


def time_freqs():
    '''Return the list of country codes from the country codes vocabulary.'''
    create_time_freqs()
    try:
        time_freqs = tk.get_action('tag_list')(
                data_dict={'vocabulary_id': 'time_freqs'})
        return time_freqs
    except tk.ObjectNotFound:
        return None

class ExampleIDatasetFormPlugin(plugins.SingletonPlugin,
        tk.DefaultDatasetForm):
    '''An example IDatasetForm CKAN plugin.

    Uses a tag vocabulary to add a custom metadata field to datasets.

    '''
    plugins.implements(plugins.IConfigurer, inherit=False)
    plugins.implements(plugins.IDatasetForm, inherit=False)
    plugins.implements(plugins.ITemplateHelpers, inherit=False)

    # These record how many times methods that this plugin's methods are
    # called, for testing purposes.
    num_times_new_template_called = 0
    num_times_read_template_called = 0
    num_times_edit_template_called = 0
    num_times_comments_template_called = 0
    num_times_search_template_called = 0
    num_times_history_template_called = 0
    num_times_package_form_called = 0
    num_times_check_data_dict_called = 0
    num_times_setup_template_variables_called = 0

    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')

    def get_helpers(self):
        return {'country_codes': country_codes, 'coverage_codes': coverage_codes, 'time_freqs': time_freqs}

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def _modify_package_schema(self, schema):
        # Add our custom country_code metadata field to the schema.
        schema.update({
                'country_code': [tk.get_validator('ignore_missing'),
                    tk.get_converter('convert_to_tags')('country_codes')]
                })
        schema.update({
                'coverage_code': [tk.get_validator('ignore_missing'),
                    tk.get_converter('convert_to_tags')('coverage_codes')]
                })
        # Add our custom_test metadata field to the schema, this one will use
        # convert_to_extras instead of convert_to_tags.
#        schema.update({
#                'publisher': [tk.get_validator('ignore_missing'),
#                    tk.get_converter('convert_to_extras')]
#                })
#	schema.update({
#                'pub_date': [tk.get_validator('ignore_missing'),
#                    tk.get_converter('convert_to_extras')]
#                })
#	schema.update({
#                'time_start': [tk.get_validator('ignore_missing'),
#                    tk.get_converter('convert_to_extras')]
#                })
#	schema.update({
#                'time_end': [tk.get_validator('ignore_missing'),
#                    tk.get_converter('convert_to_extras')]
#                })
#	schema.update({
#                'time_freq': [tk.get_validator('ignore_missing'),
#                    tk.get_converter('convert_to_tags')('time_freqs')]
#                })
        schema.update({
                'citation': [tk.get_validator('ignore_missing'),
                    tk.get_converter('convert_to_extras')]
                })        
	return schema

    def create_package_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(ExampleIDatasetFormPlugin, self).show_package_schema()

        # Don't show vocab tags mixed in with normal 'free' tags
        # (e.g. on dataset pages, or on the search page)
        schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))

        # Add our custom country_code metadata field to the schema.
        schema.update({
            'country_code': [
                tk.get_converter('convert_from_tags')('country_codes'),
                tk.get_validator('ignore_missing')]
            })

        # Add our custom coverage_code field to the dataset schema.
        schema.update({
            'coverage_code': [
		tk.get_converter('convert_from_tags')('coverage_codes'),
                tk.get_validator('ignore_missing')]
            })

#        schema.update({
#                'publisher': [tk.get_converter('convert_from_extras'),
#                tk.get_validator('ignore_missing')]
#                })
#        schema.update({
#                'pub_date': [tk.get_converter('convert_from_extras'),
#                tk.get_validator('ignore_missing')]
#                })
#        schema.update({
#                'time_start': [tk.get_converter('convert_from_extras'),
#                tk.get_validator('ignore_missing')]
#                })
#        schema.update({
#                'time_end': [tk.get_converter('convert_from_extras'),
#                tk.get_validator('ignore_missing')]
#                })
#        schema.update({
#                'time_freq': [ 
#		tk.get_converter('convert_from_tags')('time_freqs'),
#                tk.get_validator('ignore_missing')]
#                })
        schema.update({
            'citation': [tk.get_converter('convert_from_extras'),
                tk.get_validator('ignore_missing')]
            })
        return schema

    # These methods just record how many times they're called, for testing
    # purposes.
    # TODO: It might be better to test that custom templates returned by
    # these methods are actually used, not just that the methods get
    # called.

    def setup_template_variables(self, context, data_dict):
        ExampleIDatasetFormPlugin.num_times_setup_template_variables_called += 1
        return super(ExampleIDatasetFormPlugin, self).setup_template_variables(
                context, data_dict)

    def new_template(self):
        ExampleIDatasetFormPlugin.num_times_new_template_called += 1
        return super(ExampleIDatasetFormPlugin, self).new_template()

    def read_template(self):
        ExampleIDatasetFormPlugin.num_times_read_template_called += 1
        return super(ExampleIDatasetFormPlugin, self).read_template()

    def edit_template(self):
        ExampleIDatasetFormPlugin.num_times_edit_template_called += 1
        return super(ExampleIDatasetFormPlugin, self).edit_template()

    def comments_template(self):
        ExampleIDatasetFormPlugin.num_times_comments_template_called += 1
        return super(ExampleIDatasetFormPlugin, self).comments_template()

    def search_template(self):
        ExampleIDatasetFormPlugin.num_times_search_template_called += 1
        return super(ExampleIDatasetFormPlugin, self).search_template()

    def history_template(self):
        ExampleIDatasetFormPlugin.num_times_history_template_called += 1
        return super(ExampleIDatasetFormPlugin, self).history_template()

    def package_form(self):
        ExampleIDatasetFormPlugin.num_times_package_form_called += 1
        return super(ExampleIDatasetFormPlugin, self).package_form()

    # check_data_dict() is deprecated, this method is only here to test that
    # legacy support for the deprecated method works.
    def check_data_dict(self, data_dict, schema=None):
        ExampleIDatasetFormPlugin.num_times_check_data_dict_called += 1
