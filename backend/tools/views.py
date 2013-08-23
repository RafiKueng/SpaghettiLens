
# general django imports
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# my django stuff
from ModellerApp.models import LensData, ModellingResult

#general python imports
import csv


def index(request):
  return HttpResponse('index page')









def ResultDataTable(request):
  """
  Returns a html Table with all the data from the database for each Result.
  expects input in form of get parameters, but should accept different variants
   
  ResultDataTable?[i|id|rid]=1,2,4-6
  ResultDataTable?[i|id|rid]=1;2;3;4;5
  ResultDataTable?1,2,3,4,5
  ResultDataTable?1;2;3;4;5
  
  &type=[*html|csv]         output type
  &jsonstr=[*false|true]    include the json string
  &only_final=[*true|false] only send models with final tag
  
  the ordering can only be guaranteed if using , as separator
  """
  print request.GET
  ids = []
  possible_types = ['html', 'csv']
  type='html' #default
  jsonstr = False
  only_final = True
  
  def expandStrToList(str):
    """ expands a string to a list of ints: '1,4-6,9' -> [1,4,5,6,9] """
    l = str.split(',')
    ln=[]
    for ll in l:
      if '-' in ll:
        ll = ll.split('-')
        a, b = [int(_) for _ in ll] # raises value error if not 2 elements or not int castable
        ll = range(a,b+1)
      else:
        ll = [int(ll)] #cast to int and make list
      ln.extend(ll)
    return ln
        
  class GETArgumentError(Exception):
    pass
  
  try:
    for key, val in request.GET.items():
      try:
        if key=='type' and val in possible_types:
          type = val
        elif key=='jsonstr':
          jsonstr = val in ['True', 'true', 'yes', 'y', 't', 1]
        elif key=='only_final':
          only_final = val in ['True', 'true', 'yes', 'y', 't', 1]
        elif val=='':
          ids.extend(expandStrToList(key))
        elif key in ['id', 'rid', 'i']:
          ids.extend(expandStrToList(key))
      except ValueError: # happens if wrongly formatted list of ids
        raise GETArgumentError
    if len(ids)==0:
      raise GETArgumentError

  except GETArgumentError:
    txt  = '<p>Error: You did not provide any ids or a wrong list of ids...</p>'
    txt += '<p>usage:<br><code>.../tools/ResultDataTable?[id=]1,2,4-6,9[&type=[*html|csv]][&jsonstr=[*false|true]][&only_final=[false|*true]]</code></p>'
    txt += '<p>legend:<br>'
    txt += '<code>[..]</code> optional part<br>'
    txt += '<code>[*a|b]</code> choose a or b, *a is default if omitted<br>'
    txt += 'supports lists separated with "," ranges with "-", includes the last one</p>'
    txt += '<p>arguments:<br>'
    txt += '<code>&type=[*html|csv]</code> returns an html table (inside browser), or an table file (excel)<br>'
    txt += '<code>&jsonstr=[*false|true]</code> include the basic unformatted output from spaghetti lens<br>'
    txt += '<code>&only_final</code> include only results (when working with ranges) that were marked as final (by clicking on save)</p>'
    txt += 'for example:<br>'
    txt += '<code>.../tools/ResultDataTable?1,3-5,9</code> basic usage, returns html table with results 1,3,4,5,9 omits the json string<br>'
    txt += '<code>.../tools/ResultDataTable?1,2,3&type=csv</code> returns csv / excel table<br>'
    return HttpResponseNotFound(txt)

  data = []
  
  for n, id in enumerate(ids):
    try:
      res = ModellingResult.objects.get(id=id)
    except ModellingResult.DoesNotExist:
      continue
    if only_final and not res.is_final_result:
      continue
    
    d = [
      ('result_id', id),
      ('model_id', res.lens_data_obj.pk),
      ('model_name' , res.lens_data_obj.name),
      ('datasource' , res.lens_data_obj.datasource),
      ('is_final' , res.is_final_result),
      ('created' , res.created.isoformat(' ') if res.created else ''),
      ('user' , res.created_by_str),
      ('parent' , res.parent_result.pk if res.parent_result else ''),
      ('rendered' , res.rendered_last.isoformat(' ') if res.rendered_last else ''),
      ('last_accessed' , res.last_accessed.isoformat(' ') if res.last_accessed else ''),
      ('n_models' , res.n_models),
      ('pixrad' , res.pixrad),
      ('hubbletime' , res.hubbletime),
      ('steepness_min' , res.steepness_min),
      ('steepness_max' , res.steepness_max),
      ('smooth_val' , res.smooth_val),
      ('smooth_include_central' , res.smooth_include_central),
      ('local_gradient' , res.local_gradient),
      ('is_symm' , res.is_symm),
      ('maprad' , res.maprad),
      ('shear' , res.shear),
      ('redshift_lens' , res.redshift_lens),
      ('redshift_source' , res.redshift_source),
      ('n_sources' , res.n_sources),
      ('n_images' , res.n_images)
    ]
    if jsonstr:
      d.append(('json_str', res.json_str))
      
    dd = []
    for key, val in d:
      dd.append(val)
    data.append(dd)
  
  if len(data)==0:
    return HttpResponseNotFound('None of the provided ids has been found (check the only_final criteria)')
    
  header = []
  for key, val in d:
    header.append(key)  
  
  if type=='csv':
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    writer = csv.writer(response)
    writer.writerow(header)
    for row in data:
      writer.writerow(row)
    return response

  elif type=='html':
    context = {
      'header': header,
      'data': data
    }
    return render(request, 'ResultDataTable.html', context)
  
  else:
    return HttpResponseNotFound()












