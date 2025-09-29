#!/usr/bin/env python
import re
import sys
import json
import logging
import itertools
import argparse
import requests
from lxml import etree

logging.basicConfig()
logger = logging.getLogger('http-post-form-login')
logger.setLevel(logging.INFO)


def main(args=None):
    ''' main '''
    args = parse_args(args or sys.argv[1:])
    logger.setLevel(args.log_level)
    logger.debug(str(args))
    form = json.loads(args.form) if (args.form is not None) else json_load(args.form_file)
    logger.debug(str(form))
    session = requests.Session()
    forms = parse_form_file_lookups(form)
    for form in generate_combinations(forms):
        logger.debug('TRYING %s', form)
        response = session.get(args.url, timeout=100)
        response.raise_for_status()
        # print(response.text)
        data = parse_form_xpath_lookups(form, response.text)
        logger.debug('TRYING#2 %s', data)
        response = session.post(args.url, data=data, timeout=100)
        if not response.ok:
            logger.warning("POST HTTP ERROR: %s failed [status_code=%s]", args.url, response.status_code)
            sys.exit(1)
        if args.fail_test:
            if re.search(args.fail_test, response.text):
                logger.debug("fail-test=true: %s", json.dumps(data))
            else:
                print(f"SUCCESS (fail-test=false): {json.dumps(data)}")
                sys.exit()
        if args.success_test:
            if re.search(args.success_test, response.text):
                print(f"SUCCESS (success-test=true): {json.dumps(data)}")
                sys.exit()
            else:
                logger.debug("success-test=false: %s", json.dumps(data))

def generate_combinations(obj):
    array_keys = {key: value for key, value in obj.items() if isinstance(value, list)}
    other_keys = {key: value for key, value in obj.items() if not isinstance(value, list)}
    array_combinations = itertools.product(*array_keys.values())
    for combination in array_combinations:
        updated_obj = other_keys.copy()
        for i, (key, value) in enumerate(array_keys.items()):
            updated_obj[key] = combination[i]
        yield updated_obj


def parse_form_file_lookups(form):
    _form = {}
    for k,v in form.items():
        if k[0] == '$':
            with open(v, 'r', encoding='utf8') as f:
                words = [s.strip() for s in f.read().split('\n')]
                _form[k[1:]] = words
        else:
            _form[k] = v
    return _form


def parse_form_xpath_lookups(form, response_text):
    tree = etree.HTML(response_text)
    _form = {}
    for k,v in form.items():
        if k[0] == '@':
            _form[k[1:]] = tree.xpath(v)[0]
        else:
            _form[k] = v
    return _form



def json_load(filename: str):
    with open(filename, 'r', encoding='utf8') as f:
        return json.load(f)

def parse_args(args: list[str]):
    ''' Parse args. '''

    parser = argparse.ArgumentParser(
        description='Post login form.',
    )
    parser.add_argument('url', type=str,
                    help='url')
    form = parser.add_mutually_exclusive_group(required=True)
    form.add_argument('--form', type=str)
    form.add_argument('--form-file', type=str)
    test = parser.add_mutually_exclusive_group(required=True)
    test.add_argument('--fail-test', type=str, help="Failure page regex")
    test.add_argument('--success-test', type=str, help="Success page regex")
    parser.add_argument('--headers',
        action='store',
        type=str,
    )
    parser.add_argument('--log-level', action='store', default='INFO', type=str, help='set log level')
    return parser.parse_args(args)


if __name__ == '__main__':
    main()
