import jmespath
import json
import requests
# from OSMPythonTools.__info__ import pkgName, pkgVersion, pkgUrl

## COPR CLASS

class COPR:
  _scheme = None
  __initialized = False

  ## INITIALIZE

  @staticmethod
  def _initialize():
    # only initialize if this has not yet been done
    if COPR.__initialized:
      return
    COPR.__initialized = True
    # load scheme
    with open('../copr.common/scheme.json', 'r') as file:
      COPR._scheme = json.load(file)
    # load files
    for key, url in COPR._scheme['urls']['files'].items():
      setattr(COPR, key, requests.get(COPR._scheme['urls']['endpoint'] + '/' + url).json())
    # init info functions
    for key, value in COPR._info.items():
      setattr(COPR, key, (lambda v: (lambda: v))(value))
    # init base function
    for key, value in COPR._scheme['functions'].items():
      setattr(COPR, key, (lambda v: (lambda: COPR.__baseFunction(v)))(value))
    # init elements
    for elementType in COPR._scheme['elementTypes']:
      # init element functions
      if 'query' in elementType:
        # the next line looks overly complicated but basically defines
        # COPR.{name}s = lambda **kwargs: COPR.__elements(elementType, **kwargs)
        # However, the wrong value would be passed on to the lambda function if it were not chained in another lambda function.
        setattr(COPR, elementType['functionName'] if 'functionName' in elementType else elementType['name'] + 's', (lambda et: (lambda **kwargs: COPR.__elements(et, **kwargs)))(elementType))
      # init element classes
      classname = COPR._classnameForElement(elementType)
      baseclassname = elementType['baseclass'] if 'baseclass' in elementType else 'element'
      globals()[classname] = type(classname, (COPR._classForName(baseclassname),), {})
      # save parameters to the element classes
      currentClass = COPR._classForElement(elementType)
      currentClass._parameters = elementType['parameters']
      while baseclassname != 'element':
        ets = [et for et in COPR._scheme['elementTypes'] if et['name'] == baseclassname]
        if len(ets) == 0:
          break
        et = ets[0]
        baseclassname = et['baseclass'] if 'baseclass' in et else 'element'
        if 'parameters' in et:
          currentClass._parameters = {**currentClass._parameters, **et['parameters']}

  ## CLASS HANDLING

  @staticmethod
  def _classForElement(elementType):
    return globals()[COPR._classnameForElement(elementType)]
  @staticmethod
  def _classForName(name):
    return globals()[COPR._classnameForName(name)]
  @staticmethod
  def _classnameForElement(elementType):
    return COPR._classnameForName(elementType['name'])
  @staticmethod
  def _classnameForName(name):
    return 'COPR' + name[0].upper() + name[1:]
  
  ## QUERYING

  @staticmethod
  def _query(query, _d=None, **kwargs):
    # normalize list of queries
    query = COPR.__normalizeQuery(query)
    queries = list(reversed(query['queries'])) if 'queries' in query else [query]
    # loop through the queries
    last = None
    results = None
    while len(queries):
      q = queries.pop()
      # build the query
      compiledQuery = COPR.__buildSingleQuery(q, {'__last': last}, **kwargs)
      # execute the query
      results = jmespath.search(compiledQuery, _d if _d and ('global' not in q or not q['global']) else COPR._data)
      last = results
    # create corresponding objects if requested
    def packIntoObject(x):
      if not isinstance(query, dict) or 'class' not in query:
        return x
      name = query['class']
      if name in COPR._scheme['macros']['classes']:
        name = COPR._scheme['macros']['classes'][name]
      if isinstance(name, dict):
        if x['class'] not in name:
          return x
        name = name[x['class']]
      return COPR._classForName(name)(x, COPR._info)
    return [packIntoObject(result) for result in results] if isinstance(results, list) else packIntoObject(results)
  @staticmethod
  def __validParametersForQuery(query):
    parameters = []
    # collect all valid parameters for the query
    if 'parameter' in query:
      parameters.append(query['parameter'])
    elif 'query' in query:
      if isinstance(query['query'], list):
        for q in query['query']:
          parameters += COPR.__validParametersForQuery(q)
      else:
        parameters += COPR.__validParametersForQuery(query['query'])
    elif 'queries' in query:
      for q in query['queries']:
        parameters += COPR.__validParametersForQuery(q)
    return parameters
  @staticmethod
  def __normalizeQuery(query, extend={}):
    # make a dict if query is a string or a list
    if isinstance(query, str) or isinstance(query, list):
      query = {'query': query}
    return {**query, **extend}
  @staticmethod
  def __buildSingleQuery(qs, meta={}, **kwargs):
    # test for unused parameters
    validParameters = COPR.__validParametersForQuery(qs)
    invalidParameters = [key for key in kwargs if key not in validParameters]
    if len(invalidParameters) > 0:
      print('WARNING: Some parameters have not been used ({parameters})'.format(parameters=', '.join(invalidParameters)))
    # return the query
    return ''.join(COPR.__buildSingleQueryArray(qs, **kwargs)).format(**dict((k, json.dumps(v)) for k, v in meta.items()))
  @staticmethod
  def __buildSingleQueryArray(qs, **kwargs):
    query = []
    # append string
    if isinstance(qs, str):
      return [qs]
    # expand list
    if isinstance(qs, list):
      for q in qs:
        query += COPR.__buildSingleQueryArray(q, **kwargs)
      return query
    # use macros in object
    if 'macro' in qs and qs['macro'] in COPR._scheme['macros']['queries']:
      qs = {**COPR._scheme['macros']['queries'][qs['macro']], **qs}
    # append object
    if 'concat' in qs and 'query' in qs:
      qs2 = COPR.__buildSingleQueryArray(qs['query'], **kwargs)
      if len(qs2) > 0:
        query.append((qs['prefix'] if 'prefix' in qs else '') + (' ' + qs['concat'] + ' ').join(qs2) + (qs['suffix'] if 'suffix' in qs else ''))
      return query
    # use parameter if it is also provided as a keyword
    if 'parameter' in qs and qs['parameter'] in kwargs:
      parameter = qs['parameter']
      if 'removeParameterPrefix' in qs:
        parameter = parameter.lstrip(qs['removeParameterPrefix'])
      if 'removeParameterPostfix' in qs:
        parameter = parameter.rstrip(qs['removeParameterPostfix'])
      if 'startParameterLower' in qs and qs['startParameterLower'] is True:
        parameter = parameter[0].lower() + parameter[1:]
      key = qs['key'] if 'key' in qs else qs['parameter']
      value = json.dumps(kwargs[key])
      not_value = '' if kwargs[key] else '!'
      query.append(qs['query'].format(parameter=parameter, value=value, not_value=not_value))
    # use query if no parameter is included
    elif 'query' in qs and 'parameter' not in qs:
      query += COPR.__buildSingleQueryArray(qs['query'], **kwargs)
    return query

  ## FUNCTIONS

  @staticmethod
  def __elements(elementType, **kwargs):
    return COPR._query(COPR.__normalizeQuery(elementType['query'], extend={'class': elementType['name']}), **kwargs)
  @staticmethod
  def __baseFunction(resultDescription):
    if resultDescription['resultType'] == 'dict':
      result = {}
      for key, query in resultDescription['query'].items():
        result[key] = COPR._query(query)
      return result
    elif resultDescription['resultType'] == 'string':
      return COPR._query(resultDescription['query'])

## BASE CLASS

class COPRElement:
  def __init__(self, d, info):
    self._d = d
    self._info = info
  def howToCite(self):
    return self._info['howToCite']
  def __getParameter(self, name):
    # if the parameter was not defined, raise an exception
    if name not in self._parameters:
      raise Exception('AttributeError: \'{classname}\' object has no attribute \'{name}\''.format(classname=type(self).__name__, name=name))
    # query the parameter
    query = self._parameters[name]
    return COPR._query(query, _d=self._d)
  def __getattr__(self, name):
    return lambda: self.__getParameter(name)

## INITIALIZE

COPR._initialize()
