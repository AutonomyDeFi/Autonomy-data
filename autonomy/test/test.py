import autonomy as a

class Test(a.Block):

    @classmethod
    def test_write(cls):
        obj = 'test'
        a.put('test', obj)
        assert a.get('test') == obj
        a.rm('test')
        assert a.get('test') == {}

    @classmethod
    def test(cls):
        test_fns = [fn for fn in cls.functions() if fn.startswith('test_')]
        for fn in test_fns:
            a.print(f'Running {fn}')
            getattr(cls, fn)()
        return {'status': 'success', 'msg': 'All tests passed.', 'tests': test_fns}


