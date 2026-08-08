OK_FORMAT = True

test = {   'name': 'q1',
    'points': None,
    'suites': [   {   'cases': [   {   'code': '>>> def test_low_primes(sieve):\n'
                                               '...     assert sieve(1) == set()\n'
                                               '...     assert sieve(2) == {2}\n'
                                               '...     assert sieve(3) == {2, 3}\n'
                                               '>>> test_low_primes(sieve)\n',
                                       'hidden': False,
                                       'locked': False}],
                      'scored': True,
                      'setup': '',
                      'teardown': '',
                      'type': 'doctest'}]}
